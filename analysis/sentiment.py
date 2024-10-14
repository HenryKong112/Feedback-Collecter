import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load data
df = pd.read_excel("analysis/comments_with_filtered_sentiment.xlsx")

# Ensure 'PublishedAt' is in datetime format
df['PublishedAt'] = pd.to_datetime(df['PublishedAt'])

# Extract date from 'PublishedAt' and create a new column for grouping
df['Date'] = df['PublishedAt'].dt.date

# Group by date and sentiment, then count the number of comments in each category
sentiment_trend = df.groupby(['Date', 'Sentiment']).size().unstack(fill_value=0)

# Set seaborn style
sns.set(style="whitegrid")

# Create a new figure
plt.figure(figsize=(12, 6))

# Plotting the sentiment trend over time
sentiment_trend.plot(kind='line', marker='o', ax=plt.gca())  # Use the current Axes

plt.title('Number of Comments by Sentiment Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Comments')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Sentiment')
plt.tight_layout()

# Show the plot
plt.show()



