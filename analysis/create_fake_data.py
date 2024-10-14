import sqlite3
from faker import Faker
import pandas as pd

# Load the Excel file into a DataFrame
example_df = pd.read_excel("analysis/example.xlsx")

# Convert the 'PublishedAt' column to datetime format
example_df['PublishedAt'] = pd.to_datetime(example_df['PublishedAt'], format='%Y-%m-%dT%H:%M:%SZ')
example_df['PublishedAt'] = example_df['PublishedAt'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Create a Faker instance
fake = Faker()

# Connect to the database
with sqlite3.connect('Feedback.db') as conn:
    cursor = conn.cursor()

    # Iterate over the DataFrame rows
    for index, row in example_df.iterrows():
        email = fake.email()  # Generate a fake email
        time = row['PublishedAt']  # Get the time for the current row
        comment = row['Comment']   # Get the comment for the current row
        like = row['Like']         # Get the like for the current row
        
        # Insert into the Feedback table
        cursor.execute('''
            INSERT INTO Feedback (Email, Time, Comment, Like)
            VALUES (?, ?, ?, ?);
        ''', (email, time, comment, like))

    # Commit the changes
    conn.commit()


