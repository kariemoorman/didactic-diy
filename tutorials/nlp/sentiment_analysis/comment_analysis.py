import argparse
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

class CommentAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')
        self.derogatory_word_weights = {
                                        "hate": 0.8,
                                        "stupid": 0.6,
                                        "idiot": 0.7,
                                        "dumb": 0.1,
                                        # Add more words and weights
                                        }

    def calculate_derogatory_score(self, comment):
        normalized_score = 0
        total_weight = sum(self.derogatory_word_weights.values())
        words = word_tokenize(comment)
        words = [word for word in words if word.lower() not in self.stop_words]

        for word in words:
            if word.lower() in self.derogatory_word_weights:
                normalized_score += self.derogatory_word_weights[word.lower()]

        if total_weight > 0:
            normalized_score /= total_weight

        return normalized_score

    def nltk_analyzer(self, comment):
        words = word_tokenize(comment)
        words = [word for word in words if word.lower() not in self.stop_words]

        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(comment)['compound']

        emotion_words = ['happy', 'sad', 'angry', 'excited', 'fearful', 'hate']
        emotion_found = any(word in words for word in emotion_words)

        derogatory_phrases = self.derogatory_word_weights.keys()
        derogatory_found = any(phrase in comment.lower() for phrase in derogatory_phrases)
        derogatory_score = self.calculate_derogatory_score(comment)

        return sentiment_score, emotion_found, derogatory_found, derogatory_score

    def spacy_analyzer(self, comment):
        doc = self.nlp(comment)
        return {
            "Polarity": doc._.blob.polarity,
            "Subjectivity": doc._.blob.subjectivity,
            "Emotion_words": doc._.blob.sentiment_assessments.assessments
        }

    def analyze_comments(self, comments):
        for comment in comments:
            sentiment, has_emotion, is_derogatory, derogatory_score = self.nltk_analyzer(comment)
            spacy_analysis = self.spacy_analyzer(comment)
            print(f"\nComment: {comment}")
            print(f"Sentiment Score: {sentiment}")
            print(f"Has Emotion: {has_emotion}")
            print(f"Is Derogatory: {is_derogatory}")
            print(f"Derogatory Score: {derogatory_score:.2f}")
            for key, value in spacy_analysis.items():
                print(f"{key}: {value}")
            print("-" * 30)



def main(): 
    
    parser = argparse.ArgumentParser(description="Analyze comments for sentiment, emotion, and derogatory content.")
    parser.add_argument("-c", "--comments", nargs="+", help="List of comments to analyze")
    args = parser.parse_args()
    
    analyzer = CommentAnalyzer()
    analyzer.analyze_comments(args.comments)
    
if __name__ == "__main__":
    main()
    
    

# sample_comments = [
#     "Well at least this doesn't insinuate a specific comment is astroturfing...",
#     "My favorite part of 'Show HN' is when someone asks...",
#     "Sometimes adversarial comments seem to be motivated by commercial rather than technical reasons...",
#     "You're such an idiot!",
#     "I just do not agree with your point.",
#     "This is such a dumb thing to say.",
#     "I hate having to work every day.",
# ]


# Sample Output: 

# python comment_analysis.py -c "I hate having to work every day." "This is such a dumb thing to say."
    
# Comment: I hate having to work every day.
# Sentiment Score: -0.5719
# Has Emotion: True
# Is Derogatory: True
# Derogatory Score: 0.36
# Polarity: -0.8
# Subjectivity: 0.9
# Emotion_words: [(['hate'], -0.8, 0.9, None)]
# ------------------------------

# Comment: This is such a dumb thing to say.
# Sentiment Score: -0.5106
# Has Emotion: False
# Is Derogatory: True
# Derogatory Score: 0.05
# Polarity: -0.1875
# Subjectivity: 0.5
# Emotion_words: [(['such'], 0.0, 0.5, None), (['dumb'], -0.375, 0.5, None)]
# ------------------------------
