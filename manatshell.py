import os
import subprocess
import shlex
import glob
#import Popen

class Job:
    def __init__(self, process, type):
        self.test = 1
        self.process = process
        self.pid = process.pid
        self.status = process.poll
        #self.children = []
        self.type = type
#    def add_child(self,child_job):
    #    self.children.append(child_job)
    def type():
        return "THIS IS A JOB OBJECT"

#what do you do if parent process finishes before the child process?
def clean_processes(running_processes):
    print(running_processes)
    #processes_to_remove = []
    for job in running_processes:
        for child_process in job.children:
            if job_children.process.poll != None:
                running_processes[job].remove(job_children.pid)
        if job.process.poll != None:
            print("FOUND FINISHED JOB")
            running_processes.remove(job)


def execute(command, processes):
    input_redirection = None
    output_redirection = None
    piping = False

    #clean_processes(processes)
    command_tokens = split_line(command)
    if "|" in command_tokens:
        piping = True
        commands_to_pipe = []
        command_tokens_copy = [x for x in command_tokens]
        print("COPY IS", command_tokens_copy)
        while "|" in command_tokens_copy:
            #print ("IN HERE")
            print("UPDATED COPY IS", command_tokens_copy)
            commands_to_pipe.append(command_tokens_copy[0:command_tokens_copy.index("|")])
            command_tokens_copy = command_tokens_copy[command_tokens_copy.index("|")+1:]
        commands_to_pipe.append([command_tokens_copy[0]])
        print(commands_to_pipe)
        #subfile for each of the things you want do

    if "<" in command_tokens:
        print("in the <")
        print(command_tokens)
        #look at all the fields associated. stdin and sdout.
        index_value = command_tokens.index("<")
        filename = command_tokens[index_value+1]
        command = command_tokens[0:index_value]
        print("COMMAND IS", command)
        print("FILE IS", filename)
        try:
            input_redirection = open(filename, "r")

        except:
            print("File was not successfully created")
            #continue

    if ">" in command_tokens:
        print("in the >")
        print(command_tokens)
        #look at all the fields associated. stdin and sdout.
        index_value = command_tokens.index(">")
        print(index_value)
        filename = command_tokens[index_value+1]
        command = command_tokens[0:index_value]
        print("COMMAND IS", command)
        print("FILE IS", filename)
        try:
            output_redirection = open(filename, "w")

        except:
            print("File was not successfully created")
            #continue

        '''
        index_value = command.index(">")
        file = command_tokens[2]
        command = command[0]
        try:
            output_redirection = open(file, 'r')
        except:
            print("File was not found")
            #continue
        '''

    if command_tokens[0] == "pwd":
        print(os.getcwd())

    if command_tokens[0] == "cd":
        print("PATH IS", (command_tokens[len(command_tokens)-1]))
        try:
            os.chdir(command_tokens[1])
            print(os.getcwd())
        except:
            print("please enter a valid path for where to go")

    if command_tokens[0] == "bg":
        pid = command_tokens[1]
        print(pid)
        for job in processes:
            if job.pid == pid:
                job.process.send_signal(signal.SIGSTOP)
                print("stop signal sent")
                job.process.send_signal(signal.SIGCONT)

    if command_tokens[0] == "jobs":
        #print(processes)
        for job in processes:
            if job.type == "background":
                print(job.pid)

    if command_tokens[0] == "fg":
        try:
            pid = command_tokens[1]
            print(pid)
            for job in processes:
                if job.pid == pid:
                    job.process.send_signal(signal.SIGCONT)
                    print("continue signal sent")
                    job.process.wait()
            #how do you run in the foreground, make it p.wait()?
        except:
            "please enter valid arguments"

    else:
        type = "foreground"
        if "&" in command_tokens:
            type = "background"
        sbp = subprocess.Popen(command_tokens, stdin=input_redirection, stdout=output_redirection)
        child_job = Job(sbp,type)
        #current_pid = os.getpid()
        #print(current_pid)
        processes.append(child_job)
        if type == "foreground":
            sbp.wait()

        '''
            if job.pid == current_pid:
                processes[current_pid].add_child(child_job)
                added = True
        if added == False:
            parent_job = Job(sbp,type)
            processes.append(parent_job)
        '''
        #print(processes[0])
        #print(processes[0].pid)
        #print(processes[0].test)
            #processes[current_pid] = child_job
    #include a clean which looks through the processes and see if the job is complete, then remove. Kill the node and remove from the tree.

    return processes

def split_line(command):
    return(shlex.split(command))


def main():
    running_processes = []

    while True:
        command = input("$ ")
        if command == "exit":
            print("Exiting shell")
            break
        elif command == "help":
            print("Manat's shell. A basic Python shell")
        else:
            running_processes = execute(command, running_processes)

#what is going on with type/attribute not found?
#how to handle the piping and the subcommands?
#where do I even do the globbing?
#thoughts on how to build the automated testing system?

if '__main__' == __name__:
    main()
