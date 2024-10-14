# Import necessary libraries
import pandas as pd
import gensim
from gensim import corpora
import pyLDAvis.gensim_models
import pyLDAvis
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords
nltk.download('stopwords')

# 1. Load the cleaned data
df = pd.read_excel('analysis/comments_with_filtered_sentiment.xlsx')

# 2. Tokenize the 'Cleaned_Comment' column and remove stopwords
# Assuming 'Cleaned_Comment' contains strings, split them into lists of words
stop_words = set(stopwords.words('english'))

df['Cleaned_Comment'] = df['Cleaned_Comment'].apply(lambda x: [word for word in x.split() if word.lower() not in stop_words])

# 3. Create a Dictionary and Corpus
# Create a dictionary from the Cleaned_Comment column
dictionary = corpora.Dictionary(df['Cleaned_Comment'])

# Filter out words that are too rare or too frequent
dictionary.filter_extremes(no_below=10, no_above=0.5)

# Create a corpus from the dictionary
corpus = [dictionary.doc2bow(comment) for comment in df['Cleaned_Comment']]

# 4. Build the LDA Model
# Set the number of topics
num_topics = 5

# Build the LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, 
                                            id2word=dictionary, 
                                            num_topics=num_topics, 
                                            random_state=100,
                                            update_every=1, 
                                            chunksize=100, 
                                            passes=10, 
                                            alpha='auto', 
                                            per_word_topics=True)

# Print the topics
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))

# 5. Visualize the Topics using pyLDAvis
# Prepare the visualization
lda_vis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

# Display the visualization in a notebook
pyLDAvis.display(lda_vis_data)

# 6. Visualize Word Clouds for Each Topic 
# Generate word clouds for each topic
for i in range(num_topics):
    plt.figure()
    plt.imshow(WordCloud(background_color='white').fit_words(dict(lda_model.show_topic(i, 200))))
    plt.axis('off')
    plt.title(f'Topic {i+1}')
    plt.show()


