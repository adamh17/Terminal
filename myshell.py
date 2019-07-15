import os
from cmd import Cmd
import sys
import subprocess

class MyPrompt(Cmd):


	def default(self, args): #runs as a subprocess.
		args = args.split()
		try:
			if args[-1] == "&": #ensures the program is run as a background process.
				for i in range(0, len(args[:-1])):
					if args[i] == ">": #using overwrite.
						try:
							overiding(subprocess.Popen(args[:i]), args[i+1:])
						except IndexError:
							print("No filename was given.")
					elif args[i] == '>>': #using append.
						try:
							appending(subprocess.Popen(args[:i], args[i+1]))
						except IndexError: #no filename.
							print('No filename was given.')
					else:
						try:
							subprocess.Popen(args[:-1])
						except FileNotFoundError:
							print('Error: No such command exists.')
			else:
				try:
					subprocess.run(args)
				except FileNotFoundError: #the entered command doesn't exist.
					print('Error: No such command exists.')
		except IndexError:
			try:
				subprocess.run(args)
			except FileNotFoundError:
				print('Error: No such command exists.')


	def do_help(self, args):
		with open("README.txt", "r") as f:
			line = 1
			for n in f:
				print(n.strip())
				if line % 20 == 0:
					input()
				line += 1


	def do_cd(self,args):
		try:
			os.environ['PWD'] = os.getcwd()
			os.chdir(args)
		except FileNotFoundError:
			print("Try again.")
		finally:
			prompt.prompt = ">" + os.getcwd() + "/myshell>"
			print(os.getcwd())


	def do_clr(self,args):
		os.system("clear") #clear the screen.


	def do_environ(self,args):
		args = args.split() #split the args into a list.
		comment = []
		count = 0
		try:
			for i in range(0, len(args)):
				if args[i] == ">": #check to see if we need the overwrite redirection function.
					try:
						sentence = str(get_env())
						overiding([sentence], args[i+1:]) #Output to the given file.
						break
					except IndexError:
						print("No filename was given.")
						break
				elif args[i] == ">>": #check to see if we need the append redirection function.
					try:
						sentence = str(get_env())
						appending([sentence], args[i+1:]) #appends the output to a file.
						break
					except IndexError: #error message.
						print("No filename was given.")
						break
				else:
					comment.append(args[i])
					count += 1
			if count == len(args):
				print("\n".join(get_env()))
		except IndexError:
			print("\n".join(get_env()))


	def do_quit(self,args):
		raise SystemExit #exists the shell.


	def do_echo(self,arg):
		args = arg.split() #spit the args into a list.
		comment = []
		count = 0
		for i in range(0, len(args)): #move through our list.
			if args[i] == ">": #check to see if we need the overwrite redirection function.
				sentence = get_echo(comment) #convert the arguments into a string.
				try:
					overiding([sentence], args[i+1:]) #Output to the given file.
					break
				except IndexError: #error message.
					print("Filename was not given.")
					break
			elif args[i] == ">>": #check to see if we need the append redirection function.
				sentence = get_echo(comment)
				try:
					appending([sentence], args[i+1:]) #appends the output to a file.
					break
				except IndexError:
					print("Filename was not given.")
					break
			else:
				comment.append(args[i])  #appends arguments that are not commands into a list.
				count += 1
		if count == len(args): #used if the loop broke.
			print(get_echo(comment))


	def do_pause(self,args):
		line = input()
		while line != "":
			line = input() #pause the shell until "Enter" is pressed.


	def do_dir(self, args):
		args = args.split() #split args into a list.
		comment = []
		count = 0
		try:
			for i in range(0, len(args)):
				if args[i] == '>': #check to see if we need the overwrite redirection function.
					sentence = str_dir(args[0])
					try:
						overiding([sentence], args[i+1:]) #Output to the given file.
						break
					except IndexError:
						print("No filename given.")
						break
				elif args[i] == '>>': #check to see if we need the append redirection function.
					try:
						sentence = str_dir(args[0])
						appending([sentence], args[i+1:]) #appends the output to a file.
						break
					except IndexError:
						print("No filename given.")
						break
				else:
					comment.append(args[i])
					count += 1
			if count == len(args): #used if the loop broke.
				print(str_dir(args[0]))
		except IndexError:
			print(str_dir()) #prints details of the current directory.


def str_dir(directory=None): #returns directory contents as a string.
	try:
		if directory is not None: #if a directory is provided.
			return "\n".join([f for f in os.listdir(directory)]) #return the contents as a string.
		else: #if no directory is provided.
			return "\n".join([f for f in os.listdir(os.getcwd())]) #return the contents of the cd as a string.
	except FileNotFoundError: #error message.
		print('Error: Directory "{}" not found'.format(directory))


def cl_file(filename):
	try:
		with open(filename, 'r') as f:
			return [args.strip() for args in f.readlines()]
	except FileNotFoundError:
		print("Error: File {} not found".format(filename))
	raise SystemExit


def overiding(bits, args):
		try:
			with open(args[0], "w+") as f:
				for n in bits:
					f.write(n) #writes the contents to the file by overiding.
					f.write("\n")
		except IndexError:
			print("Correct Syntax: <command> > <filename>")


def appending(bits, args):
		try:
			with open(args[0], "a+") as f:
				for n in bits:
					f.write(n) #writes the contents to file by appending.
					f.write("\n")
		except IndexError:
			print("Correct Syntax: <command> > <filename>")


def get_env(): #returns a list of the environment values as strings seperated by newlines.
	environ_list = []
	for n in os.environ:
		environ_list.append("{} : {}".format(n, os.environ[n]))
	return environ_list


def get_echo(comment): #turns a list into a string.
	return " ".join(comment)




if __name__ == '__main__':
	try:
		with open(sys.argv[1], 'r') as f:
			prompt = MyPrompt()
			queue = f.readlines()
			queue.append('quit')
			prompt.cmdqueue = queue
			prompt.cmdloop()
	except:
		prompt = MyPrompt()
		prompt.prompt = ">" + os.getcwd() + "/myshell>"
		prompt.cmdloop()