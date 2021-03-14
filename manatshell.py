import os
import subprocess
import shlex
import glob

class Job:
    def __init__(self, process, type):
        self.process = process
        self.pid = process.pid
        self.status = process.poll
        self.type = type
    def type():
        return "THIS IS A JOB OBJECT"

#what do you do if parent process finishes before the child process?
def clean_processes(running_processes):
    print(running_processes)
    for job in running_processes:
        if job.process.poll != None:
            print("FOUND FINISHED JOB")
            running_processes.remove(job)

def launch_sbp(command_tokens, processes, input_redirection, output_redirection):
    type = "foreground"
    if "&" in command_tokens:
        type = "background"
    sbp = subprocess.Popen(split_commands_to_pipe[0], stdin=input_redirection, stdout=output_redirection)
    child_job = Job(sbp,type)
    processes.append(child_job)
    return processes
    if type == "foreground":
        sbp.wait()

def launch_piping(split_commands_to_pipe, processes,input_redirection,output_redirection):
    type = "foreground"
    if "&" in split_commands_to_pipe:
        type = "background"
    first_sbp = subprocess.Popen(split_commands_to_pipe[0], stdout=subprocess.PIPE)
    first_job = Job(first_sbp, type)
    processes.append(first_job)
    parent = first_sbp

    for i in range(1,len(split_commands_to_pipe)-1):
        middle_process = subprocess.Popen(split_commands_to_pipe[i], stdin=parent.stdout, stdout=subprocess.PIPE)
        job = Job(middle_process, type)
        processes.append(job)
        parent = middle_process

    #out = sbp.stdout
    last_subprocess = subprocess.Popen(split_commands_to_pipe[-1], stdin=parent.stdout)
    last_job = Job(last_subprocess, type)

    processes.append(last_job)


    #print("AFTER PIPING PROCESSes ", processes)
    return processes

def subcommand(command, processes):
    command = command.replace(')', (''))
    #if command.find('$') > 0:
        #print("THERE IS A ODLLAR SIGN")
    command = command.replace('$', (''))
    command_tokens_split = command.split('(')

    for command in command_tokens_split[::-1]:
        execute(command, processes)


    print(command_tokens_split)
    #command_tokens = split_line(command)
    #print("CT IS,", command_tokens)
    #print("CT 1 is", command_tokens[1])
    #execute(command_tokens[1], processes)
    '''
    print(command_tokens)
    for i in command_tokens:
        print(i)
        if i.find(')') >= 0:
            print("HERE")
            i = i.split(0, i.find(')'))
    print(command_tokens)
    '''

    #os.system(command)
    #command_tokens = split_line(command)
    #print(command_tokens)
    #execute(command_tokens[1], processes)

    '''
    print("")
    command = command.replace('(','')
    command = command.replace(')','')
    print("UPDATED COMMAND", command)
    os.system(command)
    #command_tokens_1 = split_line(command)
    #command_tokens_2 = command.split('(')
    #print(command_tokens_1)
    #print(command_tokens_2)
    '''
    '''
    for i in command_tokens:
        if i.index(')') != -1:
            i = i.split(0, i.index(')'))
    print(command_tokens)

    os.system(command)
    #command_tokens = split_line(command)
    #print(command_tokens)
    #execute(command_tokens[1], processes)
    '''

def execute(command, processes):
    #if it contains any wild card characteres, it goes and looks at all the files in the current directory
    #which could match the glob, and copies and pastes them in
    #goes through and replaces every instance of *.txt with a.txt, b.txt, etc.
    #not modifying the whole command, just the filename. Anywhere you see the .txt or the ~txt, that is what gets replaced
    #for name in glob.glob(command):
        #print("")
    #print(glob.glob(command))
    input_redirection = None
    output_redirection = None
    piping = False
    subcommands = False

    #preprocessing - see subcommand, laucnh suboricess. Modify command tokens
    #nested subcommands
    clean_processes(processes)
    command_tokens = split_line(command)
    if "|" in command_tokens:
        piping = True
        print("PIPING is true")
        commands_to_pipe = (command.split("|"))
        split_commands_to_pipe = []
        for i in range(0,len(commands_to_pipe)):
            split_commands_to_pipe.append(split_line(commands_to_pipe[i]))
        command_tokens = split_commands_to_pipe
        print(split_commands_to_pipe)

        '''
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
        '''

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

    if ("($") in command:
        subcommand(command, processes)

    elif command_tokens[0] == "pwd":
        print(os.getcwd())

    elif command_tokens[0] == "cd":
        print("PATH IS", (command_tokens[len(command_tokens)-1]))
        try:
            os.chdir(command_tokens[1])
            print(os.getcwd())
        except:
            print("please enter a valid path for where to go")

    elif command_tokens[0] == "bg":
        pid = command_tokens[1]
        print(pid)
        for job in processes:
            if job.pid == pid:
                job.process.send_signal(signal.SIGSTOP)
                print("stop signal sent")
                job.process.send_signal(signal.SIGCONT)

    elif command_tokens[0] == "jobs":
        #print(processes)
        for job in processes:
            if job.type == "background":
                print(job.pid)

    elif command_tokens[0] == "fg":
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
        if piping == True:
            processes = launch_piping(split_commands_to_pipe, processes, input_redirection, output_redirection)

        else:
            type = "foreground"
            if "&" in command_tokens:
                type = "background"
                index = command_tokens.index("&")
                command_tokens.remove(command_tokens[index])
                print("JOB WILL BE BACKGROUND JOB")
            sbp = subprocess.Popen(command_tokens, stdin=input_redirection, stdout=output_redirection)
            child_job = Job(sbp,type)
            #current_pid = os.getpid()
            #print(current_pid)
            processes.append(child_job)
            if type == "foreground":
                sbp.wait()

    return processes

def split_line(command):
    return(shlex.split(command))

def glob(pathname):
    pass


def main():
    running_processes = []

    while True:
        command = input("$ ")
        try:
            if command == "exit":
                print("Exiting shell")
                break
            elif command == "help":
                print("Manat's shell. A basic Python shell")
            else:
                running_processes = execute(command, running_processes)
        except KeyboardInterrupt:
            print("DID TEH CONTROL THINGS")

#what is going on with type/attribute not found?
#how to handle the piping and the subcommands?
#where do I even do the globbing?
#thoughts on how to build the automated testing system?

if '__main__' == __name__:
    main()
