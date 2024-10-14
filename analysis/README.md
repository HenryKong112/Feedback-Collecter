
# 📊 Feedback Analysis Project

This project processes user feedback comments and performs various analyses such as data cleaning, sentiment analysis, trend visualization, and topic modeling. Below is a step-by-step guide on what each file does and how everything ties together.

## 📁 Files

### 1. **`create_fake_data.py`: Data Ingestion and SQLite Database Insertion**
This script loads data from an Excel file, generates fake emails, and inserts the data into an SQLite database.

- 📥 **Input**: `example.xlsx` (contains columns like `PublishedAt`, `Comment`, and `Like`)
- 🔧 **Operations**:
  - Converts the `PublishedAt` column to a standardized datetime format.
  - Generates fake emails using the `Faker` library.
  - Inserts email, comment, and like data into a `Feedback.db` SQLite database.
- 📦 **Database**: `Feedback.db` (SQLite)

### 2. **`clean_comment.py`: Data Cleaning, Filtering, and Sentiment Analysis**
This script cleans, filters, and analyzes sentiment from user comments.

- 📥 **Input**: `example.xlsx` (same Excel file from `create_fake_data.py`)
- 🔧 **Operations**:
  - 🧹 Cleans comments by removing URLs, special characters (except emojis), and extra spaces.
  - 🌐 Filters out non-English comments.
  - ✂️ Tokenizes and truncates long comments using a DistilBERT tokenizer.
  - 🎭 Performs sentiment analysis on the cleaned comments using a pre-trained DistilBERT sentiment model.
- 📤 **Output**: `comments_with_filtered_sentiment.xlsx` (with added sentiment labels and scores).

### 3. **`sentiment.py`: Sentiment Trend Visualization**
This script visualizes the sentiment trends over time.

- 📥 **Input**: `comments_with_filtered_sentiment.xlsx`
- 📊 **Operations**:
  - Converts `PublishedAt` to datetime format and extracts the date.
  - Groups comments by date and sentiment and counts occurrences.
  - 📈 Plots a line graph showing the number of comments by sentiment (positive/negative) over time.
- 📤 **Output**: A line plot displaying sentiment trends.

### 4. **`topic_modelling.py`: Topic Modeling and Word Cloud Generation**
This script uses Latent Dirichlet Allocation (LDA) for topic modeling on the cleaned comments.

- 📥 **Input**: `comments_with_filtered_sentiment.xlsx`
- 🔧 **Operations**:
  - Tokenizes comments and removes stopwords.
  - Creates a dictionary and corpus for LDA topic modeling.
  - 💬 Performs topic modeling to identify common themes in the feedback.
  - 🖼️ Generates interactive visualizations for the topics using `pyLDAvis`.
  - ☁️ Creates word clouds for each identified topic.
- 📤 **Output**: Visualizations of topics and word clouds.

## 🛠️ Setup

1. **Install Required Libraries:**
   ```bash
   pip install pandas faker sqlite3 langdetect emoji transformers matplotlib seaborn nltk gensim pyLDAvis wordcloud
   ```
2. **Download NLTK Stopwords:**
   ```bash
   python -m nltk.downloader stopwords
   ```

## 🔍 How to Run
### 1. Data Ingestion: 
Run `create_fake_data.py` to insert the cleaned data into the SQLite database.

### 2. Sentiment Analysis: 
Run `clean_comment.py` to clean the comments and perform sentiment analysis. The results will be saved as comments_with_filtered_sentiment.xlsx.

### 3. Trend Visualization: 
Run `sentiment.py` to generate a line plot showing sentiment trends over time.

### 4. Topic Modeling:
Run `topic_modelling.py` to perform LDA topic modeling and view word clouds for each topic.

## 🎨 Visual Outputs
- **Sentiment Trend:** 

Line plot showing positive/negative comment trends over time.
- **Topic Model:** 

Interactive visualization of topics with words contributing to each.

- **Word Clouds:** 

Word clouds for each topic, visualizing the most frequent words.