import re
import pandas as pd
from langdetect import detect, LangDetectException
import emoji
from transformers import pipeline, AutoTokenizer

# Load the tokenizer to handle tokenization and truncation of lengthy comments
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Function to clean, filter, and truncate comments
def clean_and_filter_comment(comment):
    # Skip the comment if it's not a string (e.g., NaN or a float)
    if not isinstance(comment, str):
        return None
    
    try:
        # Detect the language and only keep English comments
        if detect(comment) != 'en':
            return None  # Skip non-English comments
        
    except LangDetectException:
        # If language detection fails, skip the comment
        return None
    
    # Remove URLs from the comment
    comment = re.sub(r"http\S+|www\S+|https\S+", '', comment, flags=re.MULTILINE)
    
    # Remove special characters but keep emojis (emoji range U+1F600 to U+1F64F)
    comment = re.sub(r"[^A-Za-z\s\U0001F600-\U0001F64F]+", '', comment)
    
    # Remove extra spaces and trim the comment
    comment = comment.strip()
    
    # Convert the comment to lowercase
    comment = comment.lower()
    
    # Tokenize and truncate the comment to 512 tokens if it's too long
    tokens = tokenizer(comment, truncation=True, max_length=512, return_tensors='pt')
    
    # Reconstruct the truncated comment from tokens
    truncated_comment = tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)
    
    return truncated_comment

# Load the Excel file containing comments
df = pd.read_excel("analysis/example.xlsx")

# Apply the cleaning and filtering function to each comment in the dataset
df["Cleaned_Comment"] = df["Comment"].apply(clean_and_filter_comment)

# Drop rows where comments are None (i.e., non-English or invalid comments)
df = df.dropna(subset=["Cleaned_Comment"])

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Run sentiment analysis on the cleaned comments
cleaned_comments = df["Cleaned_Comment"].tolist()
results = sentiment_analyzer(cleaned_comments)

# Add sentiment labels and scores to the DataFrame
df["Sentiment"] = [result['label'] for result in results]
df["Score"] = [result['score'] for result in results]

# Save the DataFrame with the sentiment analysis results to a new Excel file
df.to_excel("analysis/comments_with_filtered_sentiment.xlsx", index=False)

# Print the first few rows of the DataFrame to verify the results
print(df.head())










