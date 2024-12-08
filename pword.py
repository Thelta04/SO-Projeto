### Grupo: SO-TI-18
### Aluno 1: Luís Lima (fc62214)
### Aluno 2: Gonçalo Seguro (fc62252)
### Aluno 3: Dinis Garcia (fc62269)

import re
import sys, os, time
from multiprocessing import Process, Value, Queue, Lock, Array
import signal 
import datetime

processedLines = Value("i", 0)
interrupted = Value("b", False)
lock = Lock() #initializes the lock that will be used throughtout the program

#Open file and convert it to a list of all lines.

def filesToArray(files):
    '''
    Copies the contents from one or multiple .txt files to a list, removing all punctuation and symbols.

    Requires:
    file is a .txt file, containing the text contents to analyze.

    Ensures:
    A list with all the lines of the file without punctuation or symbols.
    '''
    fileNumLines = []
    linesArray = []
    for file in files: 
        with open(file, "r", encoding="utf-8") as f:
            linesArray += f.readlines()
        fileNumLines.append(len(linesArray))

    return linesArray, fileNumLines


def set_parcial_results(start_time, mode, numLines, numFiles, array = None, log_file = ""):
    """

    """
    global processedLines
    global counter

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%d/%m/%Y-%H:%M:%S")
    elapsed_time = round((time.time() - start_time) * 1000000)

    count_atm = 0

    if mode == "c":
        count_atm = counter.value

    else:
        for counter in array:
            count_atm += counter
    
    lock.acquire()

    processedFiles = 0

    for lastLine in numLines:
        if processedLines.value >= lastLine:
            processedFiles += 1

    lock.release()

    result = f"{timestamp} {elapsed_time} {count_atm} {processedFiles} {numFiles - processedFiles}"

    if log_file != "":
        with open(log_file, 'a') as file:
            file.write(result + "\n")
    else:
        print(result)

#Signal stop

def signal_handler(sig, frame):
    """
    
    """
    global interrupted
    print("\nInterrupção recebida (Ctrl+C). Finalizando processos...")
    with lock:
        interrupted.value = True 


def count_total(lines, search):
    """
    Count all occurrences of the word in the text, even if the word is repeated.

    Requires:
    lines is a list with the lines in the .txt that will be searched;
    search is a string form of the word to search for.

    Ensures:
    Print an int of all the occurrences of the word in the file.
    """
    global processedLines
    global lock
    global counter

    for line in lines:
        if not interrupted.value:
            line = line.strip().lower()
  

        lock.acquire() #Enters the critical section 

        counter.value += line.count(search.lower())
        processedLines.value += 1
    
        lock.release()
            
#Line Counter

def count_lines(lines, search, queue, index_counter, counter_array):
    '''
    Searches every line that has the word that needs to be searched
    and adds them into a set, 

    Requires:
    lines is a list with the lines in the .txt that will be searched;
    search is a string form of the word to search for.

    Ensures:
    A set() with all the lines that have the word in inside of it.
    '''
    global processedLines
    global lock

    results = set()
    
    for line in lines:
        if not interrupted.value:
            line = line.strip().lower()
            if search in line:
                results.add(line)

                
            lock.acquire()#opens the critical section

            #puts the sets into the queue
            queue.put(results)
            #adds all the sets of each son into a specific inside of the array
            counter_array[index_counter] = len(results)
            processedLines.value += 1

            lock.release()#closes it
    
    lock.acquire()#opens the critical section
        
    #puts the sets into the queue
    queue.put(results)

    lock.release()#closes it
    
#counts the number of times the word appears in isolation

def count_isolated(lines, search, queue, index_counter, counter_array):
    '''
    Count the times the word appears in the file, bt only when it appears isolated
    (separated by spaces, punctuation, etc.), excluding cases where the word is part of another word.

    Requires:
    lines is a list with the lines in the .txt that will be searched;
    search is a str form of the word to search for.

    Ensures:
    Print an int of the number of times the search word appears in the file, also says the pid of the process
    and the time it took to get the result.
    '''
    global processedLines
    global lock

    counter = 0
    #Create a word pattern to seach using regex. escape() remove special characters
    #and only consideres words that are surrounded by boundaries (\b) - Case insesitive
    pattern = r'\b' + re.escape(search.lower()) + r'\b'
    
    for line in lines:
        if interrupted.value:
            break
        #Convert line to lowercase for case-insensitivity
        line = line.lower()

        #Count occurrences of the word using regex
        counter += len(re.findall(pattern, line))

        #Enters the critical section --------
        lock.acquire()

        counter_array[index_counter] = counter
        processedLines.value += 1
        
        lock.release()
        #exits the lock --------

    #Enters the critical section --------
    lock.acquire()

    queue.put(counter)#Adds to the created queue how many times the word was found inside of this block of text
    
    lock.release()
    #exits the lock --------


def worker(lines, search, func, args):
 """
 Worker process: executes a counting function.
 """
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # Ignorar SIGINT nos filhos
    func(lines, search, *args)



def gather_queue(queue, lock):
    """
    This function gather all the values that were put on a queue, as a FIFO method, and 
    makes it that the father adds them all.  ISTO FAZ REFERENCIA A 1 PONTO DO 2.1 DPS DISCUTIR 
    SE FAZ SENTIDO FAZER UMA FUNCAO FORA DAS OUTRAS OU NAO <<<<<<<<< 
    """

#Selects the operation and runs the process

def main(args):
    '''
    Main function that runs the program

    '''    

    print('Programa: pword.py\n')

    global counter

    start_time = time.time()  # Marcar o início da execução

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    #Read arguments sent by .bash script
    operation = args[0]
    n_process = int(args[1])
    interval = int(args[2])
    log_file = args[3]
    search_word = args[4]
    files = args[5:]

    #Global Variables
    lines_list, numLines = filesToArray(files)
    processes = []
    start = 0
    
    #Define what function to execute
    if operation == "i":
        q = Queue()
        counter_array = Array("i", n_process)
        func = count_isolated

    elif operation == "c":
        func = count_total
        counter = Value("i", 0)
        counter_array = None

    elif operation == "l":
        q = Queue()
        counter_array = Array("i", n_process)
        func = count_lines

    def alarm_handler(signum, frame):
        print(log_file)
        set_parcial_results(start_time, operation, numLines, len(numLines), counter_array, log_file)

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.setitimer(signal.ITIMER_REAL, interval, interval)

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
        if (func == count_isolated or func == count_lines):
            processes.append(Process(target=func,args=(chunk, search_word, q, i, counter_array)))
        else:
            processes.append(Process(target=func,args=(chunk, search_word)))  
            
    for process in processes:
        process.start()

    for process in processes:
        process.join()
    
    print("COUNTED:", str(counter.value))

if __name__ == "__main__":
    main(sys.argv[1:])