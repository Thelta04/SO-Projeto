### Grupo: SO-TI-18
### Aluno 1: Luís Lima (fc62214)
### Aluno 2: Gonçalo Seguro (fc62252)
### Aluno 3: Dinis Garcia (fc62269)


import sys, os, time
from multiprocessing import Process


#Global Variables
punc ='''!.,;?'''
#punc = '''!"#$%&'()*+,./:;<=>?@[\\]^_`{|}~'''


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
            print("estou aqui")
            
        
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
        counter += line.count(search.lower())

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
        #Removes the pontuation
        for char in line:
            if char in punc:
                line = line.replace(char, "")
        
        i += 1
                    
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
    i = 0
    for line in lines:
        line = line.strip().lower()
        #Removes the pontuation
        for char in line:
            if char in punc:
                line = line.replace(char, "")
        lines[i] = line
        i += 1

    wordsList = [word.lower() for line in lines for word in line.split()]
    counter = 0
    search = search.lower()
    for word in wordsList:
        if word == search:
            counter +=1

    print("Process " + str(os.getpid()) + ": Counted " + str(counter))


#Divides the number of lines of the txt file for the number of processes

# def divide_work(lines, n_processes):
#     '''
#     Splits the list of lines into approximately equal chunks for each process.

#     Requires:
#     lines is a list of all lines from the files;
#     n_processes is a int with the number of processes.

#     Ensures:
#     Returns a list of lists, where each sublist is a chunk of lines to be assigned to one process.
#     '''
    
#     chunk_size = (len(lines) + n_processes - 1) // n_processes

#     for i in range(n_processes):
#         start_index = i * chunk_size
#         end_index = min(start_index + chunk_size, len(lines))
#         if start_index < end_index:
#             chunk = lines[start_index:end_index]
#             count_total(chunk)
            
#     return [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]


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
        print("started process")

    for process in processes:
        process.join()
        

if __name__ == "__main__":
    main(sys.argv[1:])
    
