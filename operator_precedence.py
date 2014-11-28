import sys
import shlex
import csv

#Write a program which will provide an implementation of operator precedance parser. Read an operator grammar and precedance table from input file/files (file for grammar, file for precedence). Read an input sentence and show the step by step parsing of that given sentence.


def main():
	
	input_string = "i + i - i"
	input_ind = list(shlex.shlex(input_string))
	input_ind.append('$')
	
	master = {}
	master_list = []
	new_list = []
	non_terminals = []
	grammar = open('grammar.txt', 'r')
	
	for row2 in grammar:
		
		if '->' in row2:
			#new production
			if len(new_list) == 0:
				start_state = row2[0]
				non_terminals.append(row2[0])
				new_list = []
				new_list.append(row2.rstrip('\n'))
			else:
				master_list.append(new_list)
				del new_list
				new_list = []
				new_list.append(row2.rstrip('\n'))
				non_terminals.append(row2[0])
				
		
		elif '|' in row2:
			new_list.append(row2.rstrip('\n'))	
	
	master_list.append(new_list)
	
	
	for x in xrange(len(master_list)):
		for y in xrange(len(master_list[x])):
			master_list[x][y] = [s.replace('|', '') for s in master_list[x][y]]
			master_list[x][y] = ''.join(master_list[x][y])
			master[master_list[x][y]] = non_terminals[x] 

	for key, value in master.iteritems():
		if '->' in key:
			length = len(key)
			for i in xrange(length):
				if key[i] == '-' and key[i + 1] == ">":
					index =  i+2
					break
			var_key = key
			new_key = key[index:]
	
	var = master[var_key]
	del master[var_key]
	master[new_key] = var	
	
	order_table = []
	with open('order.csv', 'rU') as file2:
		order = csv.reader(file2)
		for row in order:
			order_table.append(row)
	
	operators = order_table[0]
	print order_table
	###### Analysis
	stack = []

	stack.append('$') 
	
	
	print "Stack", "\t\t\t\t", "Input", "\t\t\t\t", "Precedence relation", "\t\t", "Action"
	
	vlaag = 1
	while vlaag:
		if input_ind[0] == '$' and len(stack)==2:
			vlaag = 0

		length = len(input_ind)

		buffer_inp = input_ind[0] 
		temp1 = operators.index(str(buffer_inp))
		print "stack",stack, stack[-1]
		if stack[-1] in non_terminals:
			buffer_stack = stack[-2]
		else:
			buffer_stack = stack[-1]
		temp2 = operators.index(str(buffer_stack))
		#print buffer_inp, buffer_stack
					
		precedence = order_table[temp2][temp1]
			
		if precedence == '<':
			action = 'shift'
		elif precedence == '>':
			action = 'reduce'
				
		print stack, "\t\t", input_ind, "\t\t", precedence, "\t\t", action, "\n"
		
		if action == 'shift':
			stack.append(buffer_inp)
			input_ind.remove(buffer_inp)
		elif action == 'reduce':
			for key, value in master.iteritems():
				var1 = ''.join(stack[-1:])
				var2 = ''.join(stack[-3:])
				if str(key) == str(buffer_stack):
					stack[-1] = value
					break
				elif key == var1 or stack[-3:]==list(var1):
					stack[-3:] = value
					break
				elif key == var2:
					stack[-3:] = value	
		del buffer_inp, temp1, buffer_stack, temp2, precedence
		
		if vlaag == 0:
			print "Accepted!!"
		
	return 2
	
if __name__ == "__main__":
	sys.exit(main())
