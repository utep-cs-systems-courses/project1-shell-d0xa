#Ricardo Aguilar 
#os lab1
import os,sys,re
while(True):
		PS1 = "";
		if 'PS1' in os.environ['PATH']:
			PS1 = os.environ.get(['PATH'],'PS1');
		else:
			PS1 = "$ "
			
		user = input(PS1);
		os.write(2,user.encode()); # used in debugging
		print("\n");
		
		pid = os.getpid()
		
		args = user.split()
		
		if("exit" in args):
			sys.exit(0)
			
		if((".." in args) and "cd" in args):
				previousPath = os.getcwd()
				os.chdir("../previousPath")
				
		if((len(args) > 1) and "cd" in args):
				os.chdir(args[1])
				
		elif((len(args) == 1) and "cd" in args):
			os.chdir("/home")
			
		
		else:
			rc = os.fork()
			
			if rc < 0:
				sys.exit(1)
			elif rc == 0:                   # a "child" 
				if(">" in args):
					args.remove(">")
					os.close(1) # redirect child's stdout
					sys.stdout = open(args[(len(args)-1)], "w+")
					os.set_inheritable(1, True)
					args.remove(args[(len(args)-1)])

				if("<" in args):
					args.remove("<")
					os.close(0) # redirect child's stdin
					sys.stdin = open(args[(len(args)-1)], "r")
					os.set_inheritable(0, True)
					args.remove(args[(len(args)-1)])
					
				if("|" in args):
					args.remove("|")
					os.close(0) # pipe
					r = os.fdopen(r)
					sys.stdin = open(args[(len(args)-1)], "r")
					str = r.read();
					args.remove(args[(len(args)-1)])
				
				for dir in re.split(":", os.environ['PATH']): # try each directory in the path
					program = "%s/%s" % (dir, args[0])

					try:
						os.execve(program, args, os.environ) # try to exec program
					except FileNotFoundError:					   # ...expected
						pass                              # ...fail

				os.write(1, ("%s: command not found\n" % args[0]).encode())
				sys.exit(1)                 # terminate with error
				
			else:                           # parent (forked ok)
				
				childPIDCode = os.wait()
				if(childPIDCode[1] == 0):
					pass
				else:
					os.write(1, ("Program terminated with exit code %d \n" % 
						childPIDCode).encode())
