import sqlite3

# Function to create necessary tables
def create_tables():
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        # Create Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Feedback (
                CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
                Email VARCHAR(256),  
                Time DATETIME,  
                Comment TEXT,  
                Like INTEGER DEFAULT 0
            );
        ''')
        
        # Create table to track liked comments per user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS record_liked_comments (
                Email VARCHAR(256),  
                Liked_Comment_List VARCHAR(256) DEFAULT '0'  -- Liked comment list as comma-separated IDs
            );
        ''')
        
        # Create accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS account (
                email VARCHAR(256) PRIMARY KEY,
                password VARCHAR(256)
            );
        ''')

# Insert a new comment
def insert_comment(get_email, get_time, get_comment):
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Feedback (Email, Time, Comment, Like)
            VALUES (?, ?, ?, ?)
            """,
            (get_email, get_time, get_comment, 0)
        )
        conn.commit()

# Insert a new user account
def insert_account(email_input, password_input):
    with sqlite3.connect("Feedback.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO account (email, password)
            VALUES (?, ?)
            """,
            (email_input, password_input)
        )
        conn.commit()

# Ensure a user has a liked comment list entry (initially '0' if none exists)
def record_liked_comment_list(get_email):
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Liked_Comment_List FROM record_liked_comments 
            WHERE Email = ?
            """, 
            (get_email,)
        )
        rows = cursor.fetchone()

        if rows:
            # Return the liked comment list if it exists
            return rows[0]
        else:
            # Initialize the liked comment list to '0' (indicating no liked comments)
            liked_comment = "0"
            cursor.execute(
                """
                INSERT INTO record_liked_comments (Email, Liked_Comment_List)
                VALUES (?, ?)
                """,
                (get_email, liked_comment)
            )
            conn.commit()
            return liked_comment

# Fetch all feedback (returns all comments)
def fetch_feedback():
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Feedback")
        rows = cursor.fetchall()
        return rows

# Fetch the list of liked comments for a specific user
def fetch_record_liked_comments(get_email):
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Liked_Comment_List FROM record_liked_comments 
            WHERE Email = ?
            """, 
            (get_email,)
        )
        rows = cursor.fetchone()
        if rows:
            return rows[0]  # Return the liked comments list as a string (e.g., '1,2,3')
        else:
            return "0"  # Return '0' if no comments have been liked yet

def update_liked_comment(comment_id, email):
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        
        # Fetch the liked comment list for the user
        cursor.execute("SELECT Liked_Comment_List FROM record_liked_comments WHERE Email = ?", (email,))
        result = cursor.fetchone()
        
        if result is None:
            # If no record exists for the user, insert a new one with the current liked comment
            liked_comments = str(comment_id)  # Start a new list with this comment ID
            cursor.execute(
                "INSERT INTO record_liked_comments (Email, Liked_Comment_List) VALUES (?, ?)",
                (email, liked_comments)
            )
        else:
            # If the user has a record, update their liked comment list
            liked_comments = result[0]  # Get the current liked comments
            liked_comment_list = liked_comments.split(",") if liked_comments else []
            
            if str(comment_id) not in liked_comment_list:
                liked_comment_list.append(str(comment_id))
                updated_liked_comments = ",".join(liked_comment_list)
                
                cursor.execute(
                    "UPDATE record_liked_comments SET Liked_Comment_List = ? WHERE Email = ?",
                    (updated_liked_comments, email)
                )
            else:
                # The comment was already liked
                return "Already Liked"
        
        # Increment the like count in the Feedback table
        cursor.execute("UPDATE Feedback SET Like = Like + 1 WHERE CommentID = ?", (comment_id,))
        conn.commit()

def fetch_account(email, hashed_password):
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM account WHERE email = ? AND password = ?",
            (email, hashed_password)
        )
        return cursor.fetchone()

def fetch_account_by_email(email):
    with sqlite3.connect('Feedback.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM account WHERE email = ?",
            (email,)
        )
        return cursor.fetchone()

if __name__ == "__main__":
    # Example: Creating tables
    create_tables()
