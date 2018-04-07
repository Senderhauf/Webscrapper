import collections
import glob, os
import scrapevisible
import json

scrapevisible.main()


# Stopwords
stopwords = set(line.strip() for line in open('stopwords.txt'))
#stopwords = stopwords.union(set(['mr','mrs','one','two','said']))

# Instantiate a dictionary, and for every word in the file, 
# Add to the dictionary if it doesn't exist. If it does, increase the count.
wordcount = {}


for file in glob.glob("*.txt"):

    # Read input file, note the encoding is specified here 
    # It may be different in your text file
    file = open(file, 'r')
    a= file.read()


    # To eliminate duplicates, remember to split by punctuation, and use case demiliters.
    for word in a.lower().split():
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("\"","")
        word = word.replace("!","")
        #word = word.replace("â€œ","")
        #word = word.replace("â€˜","")
        word = word.replace("*","")
        if word not in stopwords:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1

    # Close the file
    file.close()

# Print most common word
n_print = int(input("How many most common words to print: "))
print("\nOK. The {} most common words are as follows\n".format(n_print))
word_counter = collections.Counter(wordcount)
for word, count in word_counter.most_common(n_print):
    print(word, ": ", count)

#write data to json
with open('data.json', 'w+') as outfile:
    json.dump(wordcount, outfile, ensure_ascii=True, indent=4, sort_keys=True)


#clean up files in directory - delete all ".txt" files in current working directory
for file in glob.glob("*.txt"):
    if file != 'stopwords.txt':
        os.remove(file)