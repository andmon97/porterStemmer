from Porter import Porter
from nltk.stem import PorterStemmer


def main():
    myPorter = Porter()
    nltkPorter = PorterStemmer()

    vocabulary = []
    vocabularyNltk = []
    correctOutput = []

    # Read the files
    fileVocabulary = open('testVocabulary/vocabulary.txt', 'r')
    outputVocabulary = open('testVocabulary/output.txt', 'r')
    lines = fileVocabulary.readlines()
    linesOut = outputVocabulary.readlines()

    # read the words and put the stems in the lists
    for line in lines:
        vocabulary.append(myPorter.getStem(line))
        vocabularyNltk.append(nltkPorter.stem(line))

    # read the corrected stem from the file and put in the list
    for line in linesOut:
        correctOutput.append(line)

    # count corrected Stems by comparing with the items in the corrected list
    correctStems = 0
    for i in range(len(vocabulary)):
        if vocabulary[i] == correctOutput[i]:
            correctStems +=1

    stemAccuracy = correctStems / len(vocabulary)
    print("Accuracy of the implementation: ", stemAccuracy)

    # do the same with the nltk stemmer
    correctStems = 0
    for i in range(len(vocabulary)):
        if vocabularyNltk[i] == correctOutput[i]:
            correctStems += 1

    stemAccuracy = correctStems / len(vocabulary)
    print("Accuracy of the NLTK stemmer: ", stemAccuracy)



if __name__ == '__main__':
    main()