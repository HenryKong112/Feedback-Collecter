
# Feedback Collector App

## Overview

The **Feedback Collector App** is a simple feedback system that allows users to register, log in, submit feedback, and like comments. It is built using **Tkinter** for the user interface and **SQLite** as the database. This app allows users to:

- Register and log in with a valid email and password.
- Submit comments and feedback after logging in.
- View a list of all submitted feedback in a table (using a `Treeview` widget).
- "Like" comments from other users.
  
## Features

### Login and Registration

- **Login**: Users can log in by providing a valid email and password.
- **Registration**: Users can register with a new email and password (passwords are hashed for security).

### Feedback Submission

- After logging in, users can submit comments through a simple text entry field.
- Submitted comments are saved in the SQLite database with a timestamp.

### Feedback Management

- Users can view a table of feedback with the following columns: 
  - `CommentID`: Unique identifier for each comment.
  - `Email`: Email of the user who submitted the feedback.
  - `Time`: Timestamp when the feedback was submitted.
  - `Comment`: The user's feedback text.
  - `Like`: Number of likes on each comment.

### Liking Comments

- Logged-in users can select and "like" comments from other users.
- The app ensures users can only like each comment once.

## Files

- `main.py`: Contains the core logic for the Tkinter app, including login, registration, feedback submission, and displaying the feedback.
- `database.py`: Handles database operations such as creating tables, inserting users, comments, and managing "likes."

## Dependencies

- **Tkinter**: Provides the GUI framework for the application.
- **SQLite**: Used as the database to store user information, comments, and likes.
- **Pandas**: Used to display the feedback data in tabular form.
  
## Setup Instructions

### Prerequisites

- Python 3.12.4
- Tkinter (comes pre-installed with Python)
- Pandas (install using `pip install pandas`)

### Running the App

1. **Clone the repository** or download the code.
   
2. **Install the dependencies**:
   - If you don't have `pandas`, install it using:
     ```bash
     pip install pandas
     ```
   
3. **Run the app**:
   ```bash
   python main.py
   ```

### Database Setup

The database is automatically created when the app is run for the first time, using the `create_tables()` function in `database.py`. It contains three tables:

- `accounts`: Stores user accounts (`email`, `password`).
- `comments`: Stores feedback comments (`comment_id`, `email`, `timestamp`, `comment`, `likes`).
- `liked_comments`: Stores the email and comment ID of liked comments to ensure users can only like each comment once.

## Functions Overview

### Helper Functions

- `is_valid_email(email)`: Validates that the email is correctly formatted.
- `is_valid_password(password)`: Checks that the password is between 8 and 16 characters.
- `hash_password(password)`: Hashes passwords using SHA-256 for secure storage.

### Core Functions

- **Login/Register**:
  - `check_login()`: Verifies user credentials during login.
  - `check_register()`: Registers a new user after validation.
  
- **Feedback Submission**:
  - `submit_feedback()`: Allows users to submit feedback after logging in.
  
- **Comment Management**:
  - `refresh_treeview()`: Updates the display table of comments.
  - `like_comment()`: Allows users to like a comment (one like per comment per user).


---

Enjoy using the Feedback Collector App! Check the `analysis` folder for instructions on how to analyze the feedback.

