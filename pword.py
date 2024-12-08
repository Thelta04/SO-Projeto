### Grupo: SO-TI-18
### Aluno 1: Luís Lima (fc62214)
### Aluno 2: Gonçalo Seguro (fc62252)
### Aluno 3: Dinis Garcia (fc62269)

import re
import sys, os, time
from multiprocessing import Process, Value, Queue, Lock, Array
import signal 
import datetime

processedLines = Value("i", 0) #How many lines have been counted for
interrupted = Value("b", False) #Flag that indicates if the program has been interrupe
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


#Makes the parcial results

def set_parcial_results(start_time, mode, numLines, numFiles, array = None, log_file = ""):
    """
    Logs or prints the partial results of the word counting process.

    Requires: 'start_time' is the timestamp when the program started.
    'mode' is the counting mode ('c', 'i', or 'l').
    'numLines' is a list of line counts for each file.
    'numFiles' is the total number of files being processed.
    'array' is an array of partial results for each process (modes 'i' and 'l').
    'log_file' is the file path for logging results. If empty, results are printed to stdout.

    Ensures: Outputs the results in the format: [timestamp] [elapsed_time] [count_atm] [processedFiles] [remainingFiles]
    """
    global processedLines
    global counter
    
    #Current timestamp and elapsed time since start
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%d/%m/%Y-%H:%M:%S")
    elapsed_time = round((time.time() - start_time) * 1000000)

    count_atm = 0  # Initialize the count accumulator

    if mode == "c":
        count_atm = counter.value

    else:
        for counter in array:
            count_atm += counter
    
    lock.acquire() # Acquire the lock to ensure process-safe access

    processedFiles = 0

    # Determine the number of files fully processed
    for lastLine in numLines:
        if processedLines.value >= lastLine:
            processedFiles += 1

    lock.release() # Release the lock after accessing shared data

    result = f"{timestamp} {elapsed_time} {count_atm} {processedFiles} {numFiles - processedFiles}"

    # Output the result to the log file or stdout
    if log_file != "":
        with open(log_file, 'a') as file:
            file.write(result + "\n")
    else:
        print(result)

    temp = numFiles - processedFiles #Calculates how many files are still pending to be fully processed
    #Stops the signal from repeating once all the files have been processed
    if temp == 0: 
        signal.setitimer(signal.ITIMER_REAL, 0)


#Signal stop

def signal_handler(sig, frame):
    """
    Handles the SIGINT signal (Ctrl+C) to interrupt the program.

    Requires: 'sig' is the number (int), typically SIGINT.
    'frame' is the current stack frame (frame object).

    Ensures: The global variable 'interrupted' to 'True', signaling processes to stop.
    Prints the message indicating the program is terminating.
    """
    global interrupted
    print("\nInterrupt received (Ctrl+C). Finalizing processes...")
    interrupted.value = True 


#Count all the occurances 

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
        else:
            print("Interrupted Process")
            break
  
        # Updates shared variables
        
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

            #adds all the sets of each son into a specific inside of the array
            counter_array[index_counter] = len(results)
            processedLines.value += 1

            lock.release()#closes it
        else:
            print("Interrupted Process")
            break
        
    #puts the sets into the queue
    queue.put(results, block=False)
    
    
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
            print("Interrupted Process")
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


    queue.put(counter) #Adds to the created queue how many times the word was found inside of this block of text
    
    
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
    
    #Define what function to execute and initialize the needed shared memories
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

    #Initialize ALARM signal to rn partial results
    def alarm_handler(signum, frame):
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
            
    #Start everything
    for process in processes:
        process.start()

    #Clean queue so that it doesn't jam processes
    final = 0
    # Wait for all processes to complete
    while any(p.is_alive() for p in processes):
        if operation == "l": # If counting lines containing the word
            final += len(q.get())
        time.sleep(0.1) # Avoid busy-waiting; sleep briefly between checks

    if operation == "l":
        totalCount= 0
        for count in counter_array:
            totalCount += count
        print("Total of lines counted:", totalCount)  

    elif operation == "i":
        totalCount= 0
        for count in counter_array:
            totalCount += count
        print("Total of isolated words counted:", totalCount)

    else: # Default mode ('c'), total word count mode
        print("Total of words counted:", str(counter.value))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main(sys.argv[1:])