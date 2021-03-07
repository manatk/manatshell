import os
import subprocess
import shlex
import glob
#import Popen

class Job():
    def __init__(self, process, type):
        self.process = process
        self.pid = process.pid
        self.status = process.poll
        self.children = []
        self.type = type
    def add_child(self,child_process):
        self.children.append(child_process)


'''
class jobs:
    def __init__(self, process, children):
        self.pid = process.pid
        self.status = process.status
        print(self.pid)
        print(self.status)
    def addNode(self,obj):
        self.children.append(obj)
'''


def execute(command, processes):
    command_tokens = split_line(command)
    if "|" in command_tokens:
        pass
    if "<" in command_tokens:
        #look at all the fields associated. stdin and sdout.
        index_value = command.index("<")
        #file_name = command[in]
        for i in range(0,len(command_tokens)):
            if command_tokens[i] == "<":
                index_value = i
    filename = "test"
    try:
        open(file_name, 'r')
    except:
        "NOT FOUND"


    print(command_tokens)
    #if command_tokens[0] == "ls":
        #print(os.listdir())
    if command_tokens[0] == "pwd":
        print(os.getcwd())
    if command_tokens[0] == "cd":
        try:
            os.chdir(command_tokens[1])
            print(os.getcwd())
        except:
            print("please enter a valid path for where to go")
    if command_tokens[0] == "bg":
        pid = command_tokens[1]
        for value in processes:
            print("THE VALUE IS", value)
            if value == pid:
                subprocess[pid].send_signal[signal.SIGCONT]
                print("signal sent")
                #job.process.wait()

    '''
    if command_tokens[0] == "fg":
        pid = command_tokens[1]
        for node in tree:
            if node.pid == pid:
                node.send_signal(signal.SIGCONT)
                sbp = subprocess.Popen(command_tokens[0], command_tokens[1])
                node.append(sbp)
                #figure out how to do the background vs. foreground stuff
    '''
    if command_tokens[0] == "jobs":
        #print(processes)
        #I don't think that this is going to work for a nested tree.. like if a subprocess launches a subprocess
        #Keep track of the running processes in some way - every time you launch a new process, add it to a list of running process. Every time
        #the process finishes, remove from the list of running processes. In a way that lets you visualize.
        for node in processes:
            print("PARENT:", processes[node].pid)
            #for i in processes[node].children:
                #print(i)
            for i in processes[node].children:
                if i.type == "background":
                    print("CHILDREN:", i.pid)
                else:
                    print("FOREGROUND JOB", i.pid)

            #print(processes[node].children.pid)
            #print(children)
    if command_tokens[0] == "fg":
        print("HERE")
        try:
            pid = command_tokens[1]
            print(pid)
            for value in processes:
                print("THE VALUE IS", value)
                if value == pid:
                    subprocess[pid].send_signal[signal.SIGCONT]
                    print("signal sent")
                    job.process.wait()
            #how do you run in the foreground, make it p.wait()?
        except:
            "please enter valid arguments"

    else:
        type = "background"
        sbp = subprocess.Popen(command_tokens)
        if "&" in command_tokens:
            type = "foreground"
        job = Job(sbp,type)
        current_pid = os.getpid()
        print(current_pid)
        if current_pid in processes:
            print("exists")
            processes[current_pid].add_child(job)
        else:
            #print("does not exist")
            processes[current_pid] = job
        #print(processes)
    #    print(processes[current_pid].children)

    #include a clean which looks through the processes and see if the job is complete, then remove. Kill the node and remove from the tree.

    return processes

    '''

        #print(tree)
        if tree.root == None:
            #just start with an empty list
            #os.something gets you the process ID

            #print(tree.root, ": TREE ROOT")
            job1 = Job(sbp)
            tree = Tree(job1)
            print("Tree root is", tree.root)

        else:
            print("In the else")
            job = Job(sbp)
            tree.add_child(job)
            for i in tree.children:
                print(i)

    return tree

    '''

    '''
    running_processes = []
    #running_processes.append()
    command_tokens = split_line(command)
    if command_tokens[0] == "ls" or command_tokens[0] == "pwd":
        process = job(subprocess.Popen(command_tokens))
        if job_tree.root == None:
            job_tree.root =
        print(process.children)
        print(process.status)
    '''






def split_line(command):
    #lexixng - breaking line of input into separate tokens - this all we are focusing on
    #parsing - taking tokens and building an abstract syntax string - classic compiler has to do both
    # shlex module will definitely help
    #how to handle the backslash escaping
    return(shlex.split(command))


def main():
    #job_tree = Tree(None)
    #print("HERE")
    processes = dict()
    while True:
        #print(job_tree == None)
        command = input("$ ")
        if command == "exit":
            print("Exiting shell")
            break
        elif command == "help":
            print("Manat's shell. A basic Python shell")
        else:
            #split_line(command)
            processes = execute(command, processes)

if '__main__' == __name__:
    main()
