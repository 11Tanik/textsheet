import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import *
from datetime import datetime, timedelta

# Table class giving access to basic functions.
# Each Table is linked to a file.
class Table:
	def __init__(self, file):
		self.table = []
		self.file = file
		self.code = ""
	
	def get(self,i,j):
		i = i-1
		j = j-1
		if (i >= len(self.table)):
			return ""
		if (j >= len(self.table[i])):
			return ""
		return self.table[i][j]

	def val(self,i,j):
		s = self.get(i,j)
		if (s == ""):
			return 0
		r = None
		try:
			r = eval(s)
		except BaseException as e:
			print(str(e))
		return r

	def set(self,i,j,content):
		i = i-1
		j = j-1
		while (i >= len(self.table)):
			self.table.append([])
		while(j >= len(self.table[i])):
			self.table[i].append("")
		self.table[i][j] = str(content)
	
	def row(self, r):
		r -= 1
		while (r >= len(self.table)):
			self.table.append([])
		return self.table[r]
	
	def col(self, c):
		c -= 1
		col = []
		for row in self.table:
			while(c >= len(row)):
				row.append("")
			col.append(row[c])
		return col
	
	def reload(self):
		f = open(self.file, "r")
		content = f.read()
		f.close()
		self.code = self.parse(content)
		try:
			exec(self.code)
		except BaseException as e:
			print(str(e))
	
	def writeOut(self):
		newcontent = self.toString() + "\n__code__\n" + self.code
		f = open(self.file, "w")
		f.write(newcontent)
		f.close()
	
	def parse(self,s):
		self.table = []
		lines = s.splitlines()
		i = 0
		while((lines[i] != "__code__") and (i < len(lines)-1)):
			line = []
			cells = lines[i].split("\t")
			j = 0
			while(j < len(cells)):
				line.append(cells[j])
				j += 1
			self.table.append(line)
			i += 1
		if (i >= len(lines)):
			return ""
		code = ""
		i += 1
		while(i < len(lines)):
			code += lines[i]
			if (i < len(lines)-1):
				code += "\n"
			i += 1
		return code
	
	def toString(self):
		out = ""
		i = 0
		while(i < len(self.table)):
			j = 0
			while(j < len(self.table[i])):
				out += str(self.table[i][j])
				if (j < len(self.table[i])-1):
					out += "\t"
				j += 1
			if (i < len(self.table)-1):
				out += "\n"
			i += 1
		return out

	def printTable(self):
		print(self.toString())

# Handler to check for file modifications
class FileChangeHandler(FileSystemEventHandler):
	def __init__(self, table):
		super(FileSystemEventHandler, self).__init__()
		self.last_modified = datetime.now()
		self.table = table
          
	def on_modified(self, event):
		if datetime.now() - self.last_modified < timedelta(seconds=1):
			return
		print("modified")
		if (event.is_directory):
			print("directory")
			return
		if (os.path.normpath(table.file) != os.path.normpath(event.src_path)):
			print("last change to young")
			return
		print("recalculating table")
		table.reload()
		table.writeOut()
		self.last_modified = datetime.now()

# Table API
# These are the most commonly used functions providing
# spreadsheet-like functionality.
# They are shorthands for functions on the current Table.
# (It is possible to open additional Tables from within a Table!)
#
# All Table indices start at 1.

table = None

# Returns the content at (row,col) as a string.
def get(row, col):
	global table
	return table.get(row,col)

# Returns the content at (row,col) as an evaluated python object (e.g. a number).
def val(row, col):
	print(str(row) + "," + str(col))
	global table
	return table.val(row,col)

# Sets the content at (row,col) to val.
# In this process val will be converted to a string.
def set(row, col, val):
	print(str(row) + "," + str(col) + ":" + str(val))
	global table
	table.set(row, col, val)

def row(r):
	global table
	return table.row(r)

def col(c):
	global table
	return table.col(c)

if __name__ == "__main__":
	if (len(sys.argv) < 2):
		raise Exception("no file given")
	table = Table(sys.argv[1])
	table.reload()
	table.writeOut()
	dirpath = os.path.dirname(table.file)

	event_handler = FileChangeHandler(table)
	observer = Observer()
	observer.schedule(event_handler, dirpath, recursive=False)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
