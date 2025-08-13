import sys
from collections import defaultdict
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from plexapi.server import PlexServer
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from config import Config

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view
    
# try:
#     plex = PlexServer(Config.PLEX_BASEURL, Config.PLEX_TOKEN)
#     print("Successfully connected to Plex Media Server.")
# except Exception as e:
#     print(f"Error connecting to Plex Media Server: {e}")
#     plex = None

def get_user_plex():
    if 'user_id' not in session:
        return None
    user = User.query.get(session['user_id'])
    if not user or not user.plex_baseurl or not user.plex_token:
        flash("Plex credentials not found for your account.", "danger")
        return None
    try:
        plex = PlexServer(user.plex_baseurl, user.plex_token)
        return plex
    except Exception as e:
        flash(f"Error connecting to your Plex server: {e}", "danger")
        return None

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    plex = get_user_plex()
    user_count = User.query.count()
    movie_count = 0
    tv_show_count = 0
    active_sessions_count = 0

    if plex:
        try:
            movie_count = len(plex.library.section('Movies').all())
        except Exception:
            pass
        try:
            tv_show_count = len(plex.library.section('TV Shows').all())
        except Exception:
            pass
        try:
            active_sessions_count = len(plex.sessions())
        except Exception:
            pass
            
    return render_template('dashboard.html', 
                           title="Admin Dashboard",
                           user_count=user_count,
                           movie_count=movie_count,
                           tv_show_count=tv_show_count,
                           active_sessions_count=active_sessions_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['logged_in'] = True
            session['user_id'] = user.id # Store user ID in session
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html', title="Admin Login")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        plex_baseurl = request.form.get('plex_baseurl')
        plex_token = request.form.get('plex_token')

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template('register.html', title="Register")

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different one.", "danger")
            return render_template('register.html', title="Register")

        new_user = User(username=username)
        new_user.set_password(password)
        new_user.plex_baseurl = plex_baseurl
        new_user.plex_token = plex_token
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register")

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None) # Clear user ID from session
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/admin/users')
@login_required
def user_management():
    user = User.query.get(session['user_id'])
    if user and user.username == 'admin':
        users = User.query.all()
        return render_template('user_management.html', users=users, title="User Management")
    else:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user, title="My Profile")

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Handle password change
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)

        # Handle Plex URL and Token updates
        user.plex_baseurl = request.form.get('plex_baseurl')
        user.plex_token = request.form.get('plex_token')

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    return render_template('profile_edit.html', user=user, title="Edit Profile")

@app.route('/profile/delete', methods=['POST'])
@login_required
def profile_delete():
    user_id_to_delete = session.get('user_id')
    if not user_id_to_delete:
        flash("Could not find user to delete.", "danger")
        return redirect(url_for('dashboard'))
    
    user_to_delete = User.query.get(user_id_to_delete)
    if user_to_delete:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            
            # Log the user out after successful deletion
            session.pop('logged_in', None)
            session.pop('user_id', None)
            flash("Your account has been successfully deleted.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback() # Rollback on error
            flash(f"An error occurred during account deletion: {e}", "danger")
            return redirect(url_for('profile'))
            
    flash("Account not found.", "danger")
    return redirect(url_for('dashboard'))

@app.route('/content')
@login_required
def list_all_content():
    """
    Returns a list of all content (movies and TV shows) from Plex,
    with options for filtering and sorting.
    """
    plex = get_user_plex()
    if not plex:
        return render_template('content.html', content_list=[], title="All Content")

    # Get filter and sort parameters from URL query string
    genre_filter = request.args.get('genre')
    year_filter = request.args.get('year')
    rating_filter = request.args.get('rating')
    sort_by = request.args.get('sort_by', 'title')
    sort_order = request.args.get('sort_order', 'asc')

    all_content = []
    try:
        movies_section = plex.library.section('Movies')
        tv_shows_section = plex.library.section('TV Shows')
        all_items = movies_section.all() + tv_shows_section.all()

        # Get unique genres, years, and ratings for filter dropdowns
        all_genres = sorted(list(set(g.tag for item in all_items for g in item.genres)))
        all_years = sorted(list(set(item.year for item in all_items if item.year)))
        all_ratings = sorted(list(set(item.contentRating for item in all_items if item.contentRating)))

        # Filter content
        filtered_content = []
        for item in all_items:
            # Check genre filter
            if genre_filter and (not hasattr(item, 'genres') or genre_filter not in [g.tag for g in item.genres]):
                continue
            # Check year filter
            if year_filter and (not hasattr(item, 'year') or str(item.year) != year_filter):
                continue
            # Check rating filter
            if rating_filter and (not hasattr(item, 'contentRating') or item.contentRating != rating_filter):
                continue

            # Add to filtered list
            filtered_content.append({
                'type': item.type,
                'title': item.title,
                'year': item.year,
                'summary': item.summary,
                'genre_tags': [g.tag for g in getattr(item, 'genres', [])],
                'content_rating': getattr(item, 'contentRating', 'N/A')
            })

        # Sort content
        if sort_by in ['title', 'year', 'content_rating']:
            reverse = (sort_order == 'desc')
            filtered_content.sort(key=lambda x: x.get(sort_by) if x.get(sort_by) is not None else 0, reverse=reverse)
        
        # Pass filter and sort parameters back to the template to maintain state
        return render_template('content.html',
                               content_list=filtered_content,
                               genres=all_genres,
                               years=all_years,
                               ratings=all_ratings,
                               sort_by=sort_by,
                               sort_order=sort_order,
                               selected_genre=genre_filter,
                               selected_year=year_filter,
                               selected_rating=rating_filter,
                               title="All Content")

    except Exception as e:
        flash(f"Error fetching content: {e}", "danger")
        print(f"Error fetching content: {e}", file=sys.stderr)
        return render_template('content.html', content_list=[], title="All Content")

@app.route('/movies/search', methods=['GET', 'POST'])
@login_required
def search_movies():
    plex = get_user_plex()
    if not plex:
        return render_template('movie_search.html', search_results=[], search_term="", title="Search Movies")

    search_results = []
    search_term = ""
    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()
        if search_term:
            try:
                movies = plex.library.section('Movies').search(search_term)
                for movie in movies:
                    search_results.append({'title': movie.title, 'year': movie.year, 'summary': movie.summary})
                search_results.sort(key=lambda x: x['title'].lower())
                if not search_results:
                    flash(f"No movies found matching '{search_term}'.", "info")
            except Exception as e:
                flash(f"Error searching for movies: {e}", "danger")
                print(f"Error searching for movies: {e}", file=sys.stderr)
        else:
            flash("Please enter a search term.", "warning")

    return render_template('movie_search.html', search_results=search_results, search_term=search_term, title="Search Movies")

@app.route('/now_playing')
@login_required
def now_playing():
    plex = get_user_plex()
    if not plex:
        return render_template('now_playing.html', active_sessions=[], title="Now Playing")

    # This route is now a simple HTML renderer for the real-time update page.
    return render_template('now_playing.html', title="Now Playing")

@app.route('/api/now_playing_data')
@login_required
def get_now_playing_data():
    plex = get_user_plex()
    if not plex:
        return jsonify({"error": "Plex server not connected."}), 500

    active_sessions = []
    try:
        sessions = plex.sessions()
        for s in sessions:
            user_name = s.user.title if s.user else "Unknown User"
            player_name = s.player.title if s.player else "Unknown Player"
            content_title = s.title if s.title else "Unknown Content"
            media_type = s.type if hasattr(s, 'type') else 'N/A'

            view_offset = s.viewOffset / 1000 if hasattr(s, 'viewOffset') else 0
            duration = s.duration / 1000 if hasattr(s, 'duration') else 0

            progress_percent = 0
            if duration > 0:
                progress_percent = (view_offset / duration) * 100

            active_sessions.append({
                'user': user_name,
                'player': player_name,
                'content': content_title,
                'type': media_type,
                'progress': f"{progress_percent:.0f}%" if duration > 0 else "N/A",
                'state': s.state if hasattr(s, 'state') else 'N/A'
            })
        
    except Exception as e:
        print(f"Error fetching active sessions: {e}", file=sys.stderr)
        return jsonify({"error": f"Failed to fetch active sessions: {e}"}), 500

    return jsonify(active_sessions)

# --- D3.js Visualization Routes ---

@app.route('/visualizations/genre_distribution')
@login_required
def genre_distribution_page():
    return render_template('genre_distribution.html', title="Genre Distribution")

@app.route('/api/genre_distribution_data')
@login_required
def get_genre_distribution_data():
    plex = get_user_plex()
    if not plex:
        return jsonify({"error": "Plex server not connected."}), 500

    genre_counts = defaultdict(int)
    try:
        movies = plex.library.section('Movies').all()
        tv_shows = plex.library.section('TV Shows').all()

        for item in movies + tv_shows:
            if hasattr(item, 'genres'):
                for genre in item.genres:
                    genre_name = genre.tag
                    genre_counts[genre_name] += 1
    except Exception as e:
        print(f"Error fetching genre data: {e}", file=sys.stderr)
        return jsonify({"error": f"Failed to fetch genre data: {e}"}), 500

    data = [{"genre": genre, "count": count} for genre, count in genre_counts.items()]
    data.sort(key=lambda x: x['count'], reverse=True)

    return jsonify(data)

@app.route('/visualizations/playtime_trends')
@login_required
def playtime_trends_page():
    return render_template('playtime_trends.html', title="Playtime Trends")

@app.route('/api/playtime_trends_data')
@login_required
def get_playtime_trends_data():
    plex = get_user_plex()
    if not plex:
        return jsonify({"error": "Plex server not connected."}), 500

    content_view_counts = defaultdict(int)
    try:
        all_media_items = []
        sections = plex.library.sections() if plex else []
        for section in sections:
            if section.type in ['movie', 'show']:
                all_media_items.extend(section.all())
        
        for item in all_media_items:
            content_title = getattr(item, 'title', "N/A Content")
            view_count = getattr(item, 'viewCount', 0)

            if content_title != "N/A Content" and isinstance(view_count, int) and view_count > 0:
                if item.type == 'episode':
                    content_title = getattr(item.show(), 'title', "N/A Show Title")
                
                content_view_counts[content_title] += view_count
    except Exception as e:
        print(f"Error fetching playtime data: {e}", file=sys.stderr)
        return jsonify({"error": f"Failed to fetch playtime data: {e}"}), 500

    data = [{"show": show, "watch_count": count}
            for show, count in content_view_counts.items()]
    data.sort(key=lambda x: x['watch_count'], reverse=True)
    data = data[:20]

    return jsonify(data)
