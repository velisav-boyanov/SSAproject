from line import Line
import os

class Table():
	def __init__(self, name):
		self.name = name
		self.lines = []
		self.size = 0	

	def add_line(self, elements=[]):
		is_first = False
		l = len(self.lines)
		if l == 0:
			is_first = True

		line = Line(self.name, l, elements, is_first)	
		self.lines.append(line)
		print(f"Added line {line.line_number}.")

	def remove_line(self, line_number, file_name):
		for e in list(self.lines):
			if e.line_number == line_number:
				e.read_from_file(file_name, delete=True)
		print(f"Line {line_number} removed.")		

	def get_line(self, line_number):
		for e in list(self.lines):
			if e.line_number == line_number:
				return e.line_to_str()

	def edit_line(self, line_number, key, value):
		for e in self.lines:
			if e.line_number == line_number:			
				e.elements.set_element(key, value)
		print(f"Line {line_number} edited.")

	def table_to_file(self, file_name):
		for e in self.lines:
			size = e.add_to_file(file_name)
			self.size+=size
		print("Table written to file.")	

	def file_to_table(self, file_name):
		while(True):
			l = len(self.lines)
			is_first = True
			
			line = Line(self.name, l, [], is_first)
			self.lines.append(line)
			r = self.lines[l].read_from_file(file_name)
			if r[0] == 0 and r[1] == 0:
				self.lines.pop()
			self.size+=r[1]
			if r[0] == 1 and self.lines[l].line_number != 0:
				self.lines[l].is_first = False 
			elif r[0] != 1:
				break
		print("Table info found in file.")

							


			
