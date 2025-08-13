## **Plexsorter Database Design Document**

### **1\. Introduction**

This document outlines the relational database design for the Plexsorter website. It details the tables, their fields, constraints, relationships, and the data access methods required to support the website's functionality, including user management and the storage of Plex media information.

### **2\. Database Tables Design**

#### **2.1. Users Table**

| Field Name | Description | Constraints |
| ----- | ----- | ----- |
| `user_id` | Unique identifier for each user | Primary Key, Auto-incrementing, Not Null |
| `username` | Unique username chosen by the user for login | Varchar(50), Not Null, Unique |
| `password_hash` | Hashed and salted password for user authentication | Varchar(255), Not Null |
| `email` | User's email address (optional for recovery) | Varchar(100), Unique (Optional: Nullable) |
| `created_at` | Timestamp when the user account was created | Timestamp, Not Null, Default: CURRENT\_TIMESTAMP |
| `last_login` | Timestamp of the user's last successful login | Timestamp, Nullable |

**List of tests for verifying Users table:**

**Use Case Name:** Verify Users table creation and basic insertion  
 **Description:** Test if the Users table can be created and a valid user record can be inserted.  
 **Pre-conditions:** Database connection established.  
 **Test Steps:**

1. Execute SQL to create the Users table.

2. Execute SQL to insert a valid user record.  
    **Expected Result:**  
    Table created successfully, record inserted without errors.  
    **Actual Result:** (To be filled during testing)  
    **Status:** (To be filled during testing)  
    **Notes:** (To be filled during testing)  
    **Post-conditions:** Users table exists, one record present.

**Use Case Name:** Verify username uniqueness constraint  
 **Description:** Test if inserting a duplicate username fails.  
 **Pre-conditions:** Users table exists with 'testuser'.  
 **Test Steps:**

1. Execute SQL to insert a user with an existing username.

2. Ensure error occurs.  
    **Expected Result:**  
    SQL error due to unique constraint violation.  
    **Actual Result:** (To be filled during testing)  
    **Status:** (To be filled during testing)  
    **Notes:** (To be filled during testing)  
    **Post-conditions:** No new record added. Existing record unchanged.

#### **2.2. UserPlexLibraries Table**

| Field Name | Description | Constraints |
| ----- | ----- | ----- |
| `library_id` | Unique identifier for each user's Plex library connection | Primary Key, Auto-incrementing, Not Null |
| `user_id` | Foreign Key referencing the `user_id` in the Users table | Integer, Not Null, Foreign Key (references Users.user\_id) |
| `plex_server_url` | The URL of the user's Plex server | Varchar(255), Not Null |
| `plex_access_token` | The Plex access token for authenticating with the user's Plex server | Varchar(255), Not Null |
| `last_synced_at` | Timestamp of the last successful synchronization | Timestamp, Nullable |

**Relationships:**  
 One-to-Many: A User can have multiple UserPlexLibraries (e.g., if they connect to multiple Plex servers or have different access tokens). Each UserPlexLibrary belongs to exactly one User.

**List of tests for verifying UserPlexLibraries table:**

**Use Case Name:** Verify UserPlexLibraries table creation and foreign key constraint  
 **Description:** Test if the UserPlexLibraries table can be created and if the foreign key correctly links to the Users table.  
 **Pre-conditions:** Users table exists with at least one user record.  
 **Test Steps:**

1. Execute SQL to create the UserPlexLibraries table.

2. Execute SQL to insert a valid library record.

3. Attempt to insert a record with a non-existent `user_id`.  
    **Expected Result:**  
    Step 2 succeeds, Step 3 fails due to foreign key constraint violation.  
    **Actual Result:** (To be filled during testing)  
    **Status:** (To be filled during testing)  
    **Notes:** (To be filled during testing)  
    **Post-conditions:** One valid record in UserPlexLibraries. No invalid records added.

#### **2.3. UserMediaMetadata Table**

| Field Name | Description | Constraints |
| ----- | ----- | ----- |
| `media_id` | Unique identifier for each media item within the Plexsorter system | Primary Key, Auto-incrementing, Not Null |
| `library_id` | Foreign Key referencing the `library_id` in the UserPlexLibraries table | Integer, Not Null, Foreign Key (references UserPlexLibraries.library\_id) |
| `plex_media_key` | The unique key or identifier provided by the Plex API for this specific media item | Varchar(255), Not Null, Unique (combined with library\_id) |
| `title` | Title of the movie or TV show | Varchar(255), Not Null |
| `year` | Release year of the media | Integer, Nullable |
| `media_type` | Type of media (e.g., 'movie', 'episode', 'series') | Varchar(50), Not Null |
| `poster_url` | URL to the media's poster image | Varchar(500), Nullable |
| `description` | Short description or synopsis of the media | Text, Nullable |
| `last_updated_at` | Timestamp when this media record was last updated from the Plex API | Timestamp, Not Null, Default: CURRENT\_TIMESTAMP |

**Relationships:**  
 One-to-Many: A UserPlexLibrary can contain many UserMediaMetadata entries. Each UserMediaMetadata entry belongs to exactly one UserPlexLibrary.

**List of tests for verifying UserMediaMetadata table:**

**Use Case Name:** Verify UserMediaMetadata table creation and data insertion  
 **Description:** Test if the UserMediaMetadata table can be created and if media records can be inserted.  
 **Pre-conditions:** UserPlexLibraries table exists with at least one library record.  
 **Test Steps:**

1. Execute SQL to create the UserMediaMetadata table.

2. Execute SQL to insert a valid media record.  
    **Expected Result:**  
    Table created, record inserted successfully.  
    **Actual Result:** (To be filled during testing)  
    **Status:** (To be filled during testing)  
    **Notes:** (To be filled during testing)  
    **Post-conditions:** UserMediaMetadata table exists, one record present.

**Use Case Name:** Verify plex\_media\_key and library\_id uniqueness constraint  
 **Description:** Test if inserting a duplicate `plex_media_key` for the same `library_id` fails.  
 **Pre-conditions:** UserMediaMetadata table exists with media record.  
 **Test Steps:**

1. Attempt to insert a duplicate media record with the same `plex_media_key` and `library_id`.  
    **Expected Result:**  
    SQL error due to unique constraint violation.  
    **Actual Result:** (To be filled during testing)  
    **Status:** (To be filled during testing)  
    **Notes:** (To be filled during testing)  
    **Post-conditions:** No new record added. Existing record remains unchanged.

### **3\. Data Access Methods (Functions/Stored Procedures)**

These describe the primary ways your application will interact with the database. For a web application, these would typically be wrapped in an API layer.

#### **3.1. createUser**

| Name | Description | Parameters | Return Values |
| ----- | ----- | ----- | ----- |
| `createUser` | Registers a new user account in the system. | `p_username` (string): The desired username. | `user_id` (integer): The ID of the newly created user. |
|  |  | `p_password_hash` (string): The pre-hashed password. | `null` or error code if registration fails. |
|  |  | `p_email` (string, optional): The user's email address. |  |

**List of tests for verifying createUser access method:**

**Use Case Name:** Successful user registration  
 **Description:** Test if a new user can be successfully created with valid data.  
 **Pre-conditions:** Database is accessible. No user with 'newuser'.  
 **Test Steps:**

1. Call `createUser('newuser', 'hashedpasswordabc', 'new@example.com')`.  
    **Expected Result:**  
    Returns a valid `user_id`. Users table contains 'newuser'.  
    **Actual Result:** (To be filled during testing)  
    **Status:** (To be filled during testing)  
    **Notes:** (To be filled during testing)  
    **Post-conditions:** New user record exists.

**Use Case Name:** Duplicate username registration  
 **Description:** Test if `createUser` handles duplicate username attempts correctly.  
 **Pre-conditions:** User 'newuser' exists in the database.  
 **Test Steps:**

1. Call `createUser('newuser', 'anotherhash', 'another@example.com')`.  
    **Expected Result:**  
    Returns an error or null indicating a duplicate username.  
    **Actual Result:** (To be filled during testing)  
    **Status:** (To be filled during testing)  
    **Notes:** (To be filled during testing)  
    **Post-conditions:** No new user record is created.

## **4\. Pages Requiring Database Access**

This section describes which web pages will interact with the database and what information they will retrieve or modify.

### **4.1. Login Page**

**Database Information Accessed:**

* `Users` table: `username`, `password_hash`, `user_id`, `last_login`

**Access Methods Used:**

* `authenticateUser`: Verifies the username and password to authenticate the user.

**Tests for verifying page access:**

**Use Case Name:** Verify login with valid username and password  
 **Description:** Test the website's login functionality with correct credentials.  
 **Pre-conditions:** User with username "validuser" and a known password exists in the `Users` table.  
 **Test Steps:**

1. Navigate to `/login`.

2. Enter "validuser" in the username field.

3. Enter "correctpassword" in the password field.

4. Click the "Login" button.

**Expected Result:**  
User is redirected to the dashboard/home page. Database `last_login` for "validuser" is updated to the current time.

**Actual Result:** (To be filled during testing)  
 **Status:** (To be filled during testing)  
 **Notes:** (To be filled during testing)  
 **Post-conditions:** User is authenticated, and a session is established.

### **4.2. Registration Page**

**Database Information Accessed:**

* `Users` table: `username`, `password_hash`, `email`

**Access Methods Used:**

* `createUser`: Registers a new user by adding their details to the database.

**Tests for verifying page access:**

**Use Case Name:** Verify new user registration success  
 **Description:** Test if a new user can register successfully through the website.  
 **Pre-conditions:** No user with "newplexuser" exists in the `Users` table.  
 **Test Steps:**

1. Navigate to `/register`.

2. Fill in "newplexuser", a valid password, and an email.

3. Click "Register".

**Expected Result:**  
User is redirected to login/dashboard. The `Users` table contains the new user "newplexuser".

**Actual Result:** (To be filled during testing)  
 **Status:** (To be filled during testing)  
 **Notes:** (To be filled during testing)  
 **Post-conditions:** A new user record exists in the database.

### **4.3. Profile Settings Page**

**Database Information Accessed:**

* `Users` table: `username`, `email`

* `UserPlexLibraries` table: `plex_server_url`, `plex_access_token`, `last_synced_at`

**Access Methods Used:**

* `authenticateUser`: Verifies the current user is logged in.

* `getUserPlexLibraries`: Retrieves the user's Plex library details.

**Tests for verifying page access:**

**Use Case Name:** Display user profile and Plex library connections  
 **Description:** Test if the profile page correctly fetches and displays user details and linked Plex servers.  
 **Pre-conditions:** User is logged in. User has at least one entry in `UserPlexLibraries`.  
 **Test Steps:**

1. Navigate to `/profile`.

**Expected Result:**  
 Page displays the current username, email, and a list of connected Plex servers with their URLs and last sync times.

**Actual Result:** (To be filled during testing)  
 **Status:** (To be filled during testing)  
 **Notes:** (To be filled during testing)  
 **Post-conditions:** None.

### **4.4. User Dashboard / My Media Page**

**Database Information Accessed:**

* `UserPlexLibraries` table: `library_id` (used to filter media by library)

* `UserMediaMetadata` table: `title`, `year`, `media_type`, `poster_url`, `description`

**Access Methods Used:**

* `getUserMedia`: Retrieves media metadata from the user’s Plex library.

**Tests for verifying page access:**

**Use Case Name:** Display user's Plex media library  
 **Description:** Test if the dashboard page successfully retrieves and displays media from the user's cached Plex library.  
 **Pre-conditions:** User is logged in. User's `UserMediaMetadata` table has populated entries.  
 **Test Steps:**

1. Navigate to `/dashboard` or `/mymedia`.

**Expected Result:**  
 Page displays a grid/list of movies and TV shows belonging to the user's connected Plex libraries, with correct titles, years, and posters.

**Actual Result:** (To be filled during testing)  
 **Status:** (To be filled during testing)  
 **Notes:** (To be filled during testing)  
 **Post-conditions:** None.

