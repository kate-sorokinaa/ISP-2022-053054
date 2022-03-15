import operator
import re


def read_file():
    file = open('text.txt', 'r')
    text = file.read()
    print("\nYour text: \n", text)
    file.close()
    return text


def get_sentences(text):
    text = text.lower().replace('\n', ' ').replace('?', '.').replace('!', '.').replace('...', '.')
    sentences = text.split('.')
    while "" in set(sentences):
        sentences.remove("")
    print("\nThe number of the sentences is ", len(sentences))

    all_words = []
    for s in sentences:
        words = count_words(s)
        for w in words:
            all_words.append(w)
    non_repeating_words = list(set(all_words))
    words_dictionary = dict.fromkeys(non_repeating_words, 0)
    for w in all_words:
        words_dictionary[w] += 1
    words_dictionary = dict(sorted(words_dictionary.items(), key=operator.itemgetter(1)))
    print('\n', words_dictionary)

    print("Average number of words per sentence is ", len(all_words) // len(sentences))
    most_common = 0
    med = None
    for i in set(words_dictionary.values()):
        med = list(words_dictionary.values()).count(i)
        if med > most_common:
            most_common = med
            med = i
    print("Median number of words in text is ", med, ". And ", most_common,
          "words met that number of times in the text")

    answer = input(
        "\nThe default value of the number and length of the words used most frequently are K = 10 and N = 4."
        "\nDo you want to change them? (y/n)")
    if answer == "y":
        n = int(input("Enter n: "))
        k = int(input("Enter k: "))
    else:
        n = 4
        k = 10

    i = 0
    while k > 0 and i <= len(list(words_dictionary.values())) - 1:
        i += 1
        check = list(words_dictionary.keys())[-i]
        if len(check) != n:
            continue
        else:
            print(list(words_dictionary.values())[-i], " - ", list(words_dictionary.keys())[-i])
            k -= 1
    return sentences


def count_words(sentence):
    words = re.split('; |, |: | ', sentence)
    while "" in set(words):
        words.remove("")
    return words


def main():
    text = read_file()
    get_sentences(text)


if __name__ == "__main__":
    main()
