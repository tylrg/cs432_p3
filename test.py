from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def main():
	analyzer = SentimentIntensityAnalyzer()
	sentiment_dict = analyzer.polarity_scores("I love everything and I am happy")
	print(sentiment_dict)



main()









