import os
import subprocess
import shlex
import glob
#import Popen

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

def launch_piping(split_commands_to_pipe, processes):
    type = "foreground"
    if "&" in split_commands_to_pipe:
        type = "background"

    '''
    s_in, s_out = (0, 0)
    s_in = os.dup(0)
    s_out = os.dup(1)

    fdin = os.dup(s_in)
    '''

    #print(split_commands_to_pipe[0])
    #sbp = subprocess.Popen(split_commands_to_pipe[0], stdin=subprocess.stdout, stdout=subprocess.PIPE)

    for i in range(0, len(split_commands_to_pipe)):
        print("EXECUTING", split_commands_to_pipe[i])
        sbp = subprocess.Popen(split_commands_to_pipe[i], stdin=out, stdout=sbp.PIPE)
        child_job = Job(sbp,type)
        out = sbp.stdout

    processes.append(child_job)
    print("AFTER PIPING PROCESSes ", processes)
    return processes

def execute(command, processes):
    input_redirection = None
    output_redirection = None
    piping = False

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
            processes = launch_piping(split_commands_to_pipe, processes)

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

            #processes = launch_sbp(command_tokens,processes, input_redirection, output_redirection)

        '''
        type = "foreground"
        if "&" in command_tokens:
            type = "background"

        if piping == True:
            print(split_commands_to_pipe[0])
            sbp = subprocess.Popen(split_commands_to_pipe[i], stdin=sbp.stdout, stdout=sbp.PIPE)

            for i in range(0, len(split_commands_to_pipe)):
                old_process = process
                sbp = subprocess.Popen(split_commands_to_pipe[i], stdin=sbp.stdout, stdout=sbp.PIPE)
                child_job = Job(sbp,type)
                out = process.stdout


                processes.append(child_job)



            #print("OD", sbp.output_redirection)
            output_redirection = sbp.stdout
            print("OD", output_redirection)

        else:
            sbp = subprocess.Popen(split_commands_to_pipe[0], stdin=input_redirection, stdout=output_redirection)
        child_job = Job(sbp,type)
        #current_pid = os.getpid()
        #print(current_pid)
        processes.append(child_job)
        if type == "foreground":
            sbp.wait()
        '''

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
