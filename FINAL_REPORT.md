# Project Title: Plexsorter
## Team members' names: Travis Hughes

> Project tracker link (Instructor can access): [Plexsorter](https://github.com/t-wrex-13/plexsorter)
> 
> Link to 5 minute video: a demo for a potential customer (could be same one you used in the presentation): [YouTube Video](https://youtu.be/JTWW2xACdg0?si=YzcPURz8IVqKR4nY)
>
> Version control repository link (make sure the instructor(s) have access): [Plexsorter](https://github.com/t-wrex-13/plexsorter)
>
> Include a Final Status Report and reflection for:
>
> - What you completed: I was able to complete a webpage that pulls all the content from someone's PLEX server, allows for the user to filter their collection based on genre, year, or rating. Users can also search their collection for a particular title, or they can access their Plex Admin Dashboard to see who is watching what content from the server. There is also a Dark Mode for the site, and users can edit their own profile and change their password, their PLEX URL, or their PLEX Token, or even delete their profile. I also used D3.js to implement some simple tales that show the breakdown of content count by genre and top 20 most watched items. While not the most useful metrics, I'm sure better graphs could be implemented in the future. On the Now Playing page, users can toggle how long the page refresh cycle is - 30, 60, or 120 seconds. This way, the information is always quasi-up-to-date. On the Movie Search screen, the site will do dynamic searching, using only the characters you have entered so far.
>
> - What you were in the middle of implementing: I was in the middle of implementing page sorting for the All Content screen, and I had tried (and failed) to implement a recommendation system, but I don't think I was calling the right places in the API. I'll have to look into this further
>
> - What you had planned for the future: For the future, I had planned on making content control (removing files) and server configuration a part of this. One other thing that doesn't exist but would need to on a real website is "Forgot My Password?" functionality, however, this would have required me to set up SMTP stuff, and there wasn't time for that. I considered making this an admin feature, but ultimately scrapped it. Don't forget your password!
>
> - Any known problems (bugs, issues): Right now, sort on the All Content page doesn't work - instead of directing the user back to the page with the table sorted, it just renders the JSON return. This is probably a simple fix, but I haven't had time to fix it. The other known issue (that wasn't an issue until I implemented user accounts) is that creating a user with dummy data can cause the Dashboard to load extremely slow, as the server is trying to connect to something that doesn't exist and you have to wait for the timeout. This could potentially be fixed by allowing users to not enter their server information on account creation, or by making the timeout shorter. Either way, this only happens with a dummy user. The dynamic searching can be a bit laggy and weird, sometimes requiring a page refresh.
>
> List your public hosting site and make sure that it is available: [Plexsorter](https://github.com/t-wrex-13/plexsorter)