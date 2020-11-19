first = "I want to try out to see if the tokenization actually works!"
second = "I think that this will definitely work"
third = "Wow this is great!"

concat = first + " " + second + " " + third
print(concat)
 
def count_by_word(tweets_concat):
    word_counts = dict()
    words = tweets_concat.split()

    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)


print(count_by_word(concat))
