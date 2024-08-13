import praw
from datetime import datetime, timedelta

# Reddit API setup
SECRET = ""
DEV = ""
APP = ""
APP_ID = ""

# Reddit API credentials
reddit = praw.Reddit(client_id=APP_ID,
                     client_secret=SECRET,
                     user_agent=DEV)

# Calculate the timestamp for 2 years ago
two_years_ago = datetime.now() - timedelta(days=2*365)

def get_top_posts_last_two_years(subreddit_name, top_limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = []

    for submission in subreddit.top(time_filter='all', limit=1000):  # Fetch top 1000 posts
        post_date = datetime.fromtimestamp(submission.created_utc)
        if post_date >= two_years_ago:
            top_posts.append((submission.score, submission.title, submission.selftext, post_date))

    # Sort the posts by score in descending order
    top_posts = sorted(top_posts, key=lambda x: x[0], reverse=True)

    # Return the top X posts
    return top_posts[:top_limit]

# Example usage for r/GameStop
top_posts_gamestop = get_top_posts_last_two_years('GameStop', top_limit=10000)

# Print the results
for score, title, selftext, date in top_posts_gamestop:
    print(f"Score: {score}, Date: {date}")
    print(f"Title: {title}")
    print(f"Text: {selftext[:100]}...")  # Print the first 100 characters of the post
    print("-" * 80)

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


# Combine title and text, remove special characters and URLs, convert to lowercase, and clean the text
def clean_text(title, selftext):
    # Combine title and body text
    combined_text = f"{title} {selftext}"

    # Remove URLs
    combined_text = re.sub(r'http\S+', '', combined_text)

    # Remove special characters, numbers, and punctuation
    combined_text = re.sub(r'[^A-Za-z\s]', '', combined_text)

    # Convert to lowercase
    combined_text = combined_text.lower()

    # Remove stopwords and lemmatize words
    cleaned_text = ' '.join(
        lemmatizer.lemmatize(word)
        for word in combined_text.split()
        if word not in stop_words
    )

    return cleaned_text


# Apply the cleaning function to your dataset
cleaned_posts = []
for score, title, selftext, date in top_posts_gamestop:
    cleaned_post = clean_text(title, selftext)
    cleaned_posts.append((score, cleaned_post, date))

# Convert to DataFrame for further analysis
import pandas as pd

df_cleaned_posts = pd.DataFrame(cleaned_posts, columns=['score', 'cleaned_text', 'date'])

# Specify the file path where you want to save the CSV file
file_path = 'cleaned_reddit_posts.csv'

# Save the DataFrame to CSV
df_cleaned_posts.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")