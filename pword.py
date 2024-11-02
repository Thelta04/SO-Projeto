### Grupo: SO-TI-18
### Aluno 1: Luís Lima (fc62214)
### Aluno 2: Gonçalo Seguro (fc62252)
### Aluno 3: Dinis Garcia (fc62269)


import sys, os, time
from multiprocessing import Process
import string


#Global Variables
punc ='''!.,;?'''
punc = '''!"#$%&'()*+,./:;<=>?@[]^_`{|}~-'''



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
        
    return linesArray
        
        
#Count the words 

def count_total(lines, search):
    """
    Count all occurrences of the word in the text, even if the word is repeated.

    Requires:
    lines is a list with the lines in the .txt that will be searched;
    search is a string form of the word to search for.

    Ensures:
    Print an int of all the occurrences of the word in the file.
    """
    counter = 0
    for line in lines:
        line = line.strip().lower()
        words = line.split()
        for word in words:
            if search.lower() in word:
                counter += 1

    print("Process " + str(os.getpid()) + ": Counted " + str(counter))


#Line Counter

def count_lines(lines, search):
    '''
    Count how many distinct lines contain the word.

    Requires:
    lines is a list with the lines in the .txt that will be searched;
    search is a string form of the word to search for.

    Ensures:
    Print an int of all the lines that contain the search word in the file.
    '''
    i = 0   
    counter = 0

    search = search.lower()

    #Format line to remove punctuation and lower all letters.
    for line in lines:
        line = line.strip().lower()
        line.translate(None, string.punctuation)
        #Verify if
        if search in line:
            counter += 1
    
    print("Process " + str(os.getpid()) + ": Counted " + str(counter))
    
    
#counts the number of times the word appears in isolation

def count_isolated(lines, search):
    '''
    Count the times the word appears in the file, bt only when it appears isolated
    (separated by spaces, punctuation, etc.), excluding cases where the word is part of another word.

    Requires:
    lines is a list with the lines in the .txt that will be searched;
    search is a str form of the word to search for.

    Ensures:
    Print an int of the number of times the search word appears in the file.
    '''
    counter = 0
    for line in lines:
        line = line.strip().lower()

        #Removes the punctuation
        for char in line:
            if char in string.punctuation:
                line = line.replace(char, "")

        words = line.split()
        for word in words:
            if search.lower() == word:
                counter += 1

    print("Process " + str(os.getpid()) + ": Counted: " + str(counter))


#Selects the operation and runs the process
def main(args):
    '''
    Main function that runs the program
    '''    

    print('Programa: pword.py')

    #Read arguments sent by .bash script
    operation = args[0]
    n_process = int(args[1])
    search_word = args[2]
    files = args[3]

    #Global Variables
    lines_list = filesToArray(files)
    processes = []
    start = 0
    
    #Define what function to execute
    if operation == "i":
        func = count_isolated

    elif operation == "c":
        func = count_total

    elif operation == "l":
        func = count_lines


    #Create and run processes
    remainder = len(lines_list) % n_process
    
    #Distribute work to processes evenly
    for i in range(n_process):
        chunk_size = len(lines_list) // n_process

        if remainder != 0:
            chunk_size + 1
            remainder -= 1

        chunk = lines_list[start : start + chunk_size]

        start += chunk_size

        processes.append(Process(target=func,args=(chunk, search_word)))
    
    for process in processes:
        process.start()

    for process in processes:
        process.join()
        

# if __name__ == "__main__":
#     main(sys.argv[1:])
    
lines_list = filesToArray("ficheiros_teste/file1.txt")
count_total(lines_list, "copy")