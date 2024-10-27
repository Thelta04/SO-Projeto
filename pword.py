### Grupo: SO-TI-18
### Aluno 1: Luís Lima (fc62214)
### Aluno 2: Gonçalo Seguro (fc62252)
### Aluno 3: Dinis Garcia (fc62269)

import sys, os, time
from multiprocessing import Process

#Global Variables
punc = '''!"#$%&'()*+,./:;<=>?@[\\]^_`{|}~'''

#Open file and convert it to a list of all lines, without punctuation or symbols.
def filesToArray(*files):
    '''
    Copies the contents from one or multiple .txt files to a list, removing all punctuation and symbols.

    Requires:
    file is a .txt file, containing the text contents to analyze.

    Ensures:
    Returns a list with all the lines of the file without punctuation or symbols.
    '''
    linesArray = []
    for file in files:
            
        with open(file, "r", encoding="utf-8") as f:
            linesArray += f.readlines()
            i = 0
            for line in linesArray:
                line = line.strip()
                # for char in line:
                #     if char in punc:
                #         line = line.replace(char, "")
                linesArray[i] = line
                i += 1
        
    return linesArray
        
                    
#['Olá eu sou o Max e era o rei', 'Mas o sombra veio e sem nada fiquei', 'Podem ajudar-me', 'Sou o Max btw']
#Sou o Max, btw. -> [linha1, linha2, "Sou o Max btw"]

#Count the words 

def countWordsTotal(lines):
    """
    Count the total words of the lines in the txt file

    Requires:
    A list with the words of txt file

    Ensures:
    The total count of the words in that txt file
    """
    words_total = 0
    for line in lines:
        words = line.split()
        words_total += len(words)
    return words_total


#Line Counter

# def lineCounter(lines):
#     '''
#     conta linhas crl
#     '''
#     return len(lines)
        
def ArgumentsChecker(args):# ISTO ESTA A FUNCIONAR(ate prova contraria :P) MAS PROVALVELMENTE POMOS ITSTO SO NO MAIN POIS USA OS ARGS QUE RECEBE DO SYS
    """
    """
    #options of -m mode
    c = True
    l = False
    i = False

    #options of -p mode
    n = 0

    #options of -w mode
    word = ''

    files = []

    for x in args:
        if x == "-m":
            if args[args.index(x) + 1] == "c":
                c = True
            elif args[args.index(x) + 1] == "l":
                l = True
                c = False
            elif args[args.index(x) + 1] == "i":
                i = True
                c = False
        elif x == '-p':
            n = int(args[args.index(x) + 1])
        elif x == "-w":
            word = args[args.index(x) + 1]
        elif ".txt" in x:
            files.append(x)


def searchWordCount(lines, search):
    wordsList = [word.lower() for line in lines for word in line.split()]
    counter = 0
    search = search.lower()
    for word in wordsList:
        if word == search:
            counter +=1
    return counter

#Criar processos

file = "ficheiros_teste/file4.txt"
lines = filesToArray(file)
totalWords = countWordsTotal(lines)
totalSearch = searchWordCount(lines,"Douglas")
print(lines)
print(totalWords)
print(len(lines))
print(totalSearch)

def main(args):
    
    print('Programa: pword.py')
    lines = filesToArray(file)
    
    operation = args[0]
    file = args[1]

    if operation == "i":
        counter = searchWordCount(file)
        print(counter)

    elif operation == "c":
        totalWords = countWordsTotal(lines)
        print(f'Total número de palavras: {totalWords}')

    elif operation == "l":
        print("Número de linhas: ", len(lines))

    else:
        print("Operação não reconhecida pelo programa. Use '-c', '-l' ou '-i'")


# if __name__ == "__main__":
#     main(sys.argv[1:])
