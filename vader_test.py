from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def main():
	analyzer = SentimentIntensityAnalyzer()
	sentiment_dict = analyzer.polarity_scores("Fuck that shit")
	print(sentiment_dict)

main()