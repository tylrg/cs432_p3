from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def main():
	analyzer = SentimentIntensityAnalyzer()
	sentiment_dict = analyzer.polarity_scores("that is sooo lame")
	print(sentiment_dict)

main()