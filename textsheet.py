import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import *
from datetime import datetime, timedelta

# TODO create better table API

# Table File Layout
################################################
# The File starts with TSV values in rows
# Then __code__ signifies the start of the code segment
# Then code

table = []
file = ""

# Table API

def cell(i,j):
	global table
	i = i-1
	j = j-1
	if (i >= len(table)):
		return ""
	if (j >= len(table[i])):
		return ""
	return table[i][j]

def val(i,j):
	s = cell(i,j)
	if (s == ""):
		return 0
	return eval(s)

def set(i,j,content):
	global table
	i = i-1
	j = j-1
	while (i >= len(table)):
		table.append([])
	while(j >= len(table[i])):
		table[i].append([])
	table[i][j] = str(content)

class FileChangeHandler(FileSystemEventHandler):
	def __init__(self):
		super(FileSystemEventHandler, self).__init__()
		self.last_modified = datetime.now()
          
	def on_modified(self, event):
		if datetime.now() - self.last_modified < timedelta(seconds=1):
			return
		print("modified")
		if (event.is_directory):
			print("directory")
			return
		if (os.path.normpath(file) != os.path.normpath(event.src_path)):
			print("last change to young")
			return
		print("recalculating table")
		recalculateTable()
		self.last_modified = datetime.now()

def parse(str):
	global table
	table = []
	lines = str.splitlines()
	i = 0
	while(lines[i] != "__code__" and i < len(lines)):
		line = []
		cells = lines[i].split("\t")
		j = 0
		while(j < len(cells)):
			line.append(cells[j])
			j += 1
		table.append(line)
		i += 1
	if (i >= len(lines)):
		return ""
	if (lines[i] != "__code__"):
		raise Exception("no code block found")
	code = ""
	i += 1
	while(i < len(lines)):
		code += lines[i]
		if (i < len(lines)-1):
			code += "\n"
		i += 1
	return code

def tableToString():
	global table
	out = ""
	i = 0
	while(i < len(table)):
		j = 0
		while(j < len(table[i])):
			out += str(table[i][j])
			if (j < len(table[i])-1):
				out += "\t"
			j += 1
		if (i < len(table)-1):
			out += "\n"
		i += 1
	return out

def printTable():
	print(tableToString())

def recalculateTable():
	global file
	global table
	f = open(file, "r")
	content = f.read()
	f.close()
	#print(content)
	c = parse(content)
	exec(c)

	newcontent = tableToString() + "\n__code__\n" + c
	f = open(file, "w")
	f.write(newcontent)
	f.close()



if __name__ == "__main__":
	if (len(sys.argv) < 2):
		raise Exception("no file given")
	file = sys.argv[1]
	path = os.path.dirname(file)
	recalculateTable()

	event_handler = FileChangeHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=False)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

