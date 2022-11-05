import sys
import os

prefix = sys.argv[1];
# ---------------------------------------------------------------------------------------------------
# Functions
def remove_prefix_from_variable(line, prefix):
	return line.replace('vlSelf->'+prefix+'__DOT__','')

def exe(func, func_dict):
	body_status = False
	for l in func_dict[func].split('\n'):
		if body_status:
			if l[-2:] == ");" and l.strip().split('(')[0] in func_dict.keys():
				exe(l.strip().split('(')[0], func_dict)
			else:
				l = l.strip()
				if l.startswith('vlSelf->__'):
					continue
				l = remove_prefix_from_variable(l, prefix)
				l = l.replace('U]',']')
				print(l)
			continue
		if not body_status and l.strip()[:7] == "// Body":
			body_status = True
# ---------------------------------------------------------------------------------------------------
# Getting .h and .cpp files
all_files = os.listdir(str(os.getcwd())+'/obj_dir/')
code_files = []
for f in all_files:
	try:
		if (f.split('.')[1] == 'h' or f.split('.')[1] == 'cpp') and f.find('DepSet') != -1:
			code_files.append(f)
	except:
		pass

# ---------------------------------------------------------------------------------------------------
# Generating Dictionary of Functions {func_name : func_body}
func_dict = dict()
func_name = ""
func_body = ""
func_status = True

for code in code_files:
	f = open('./obj_dir/'+code)
	lines = f.readlines()
	f.close()
	for line in lines:
#		line = line.strip()
		if line == "\n":
			continue
			
		if line[:2] == "//":
			pass
		elif func_status and line[-3:] == ");\n":
			pass
		elif func_status and line[0] == "#":
			pass
		else:
			if func_status:
				func_name = line.split('(')[0].split(' ')[-1]
				func_status = False
				continue
			if line == "}\n":
				func_status = True
				func_dict[func_name] = func_body
				func_body = ""
			else:
				func_body = func_body + line

# ---------------------------------------------------------------------------------------------------
# Get All Variables
f = open('./obj_dir/V' + prefix + '___024root.h')
lines = f.readlines()
f.close()
var_start = False
print("// ====== VARIABLE DECLARATION STARTS======")
for line in lines:
	if "// DESIGN SPECIFIC STATE" in line:
		var_start = True
		continue
	if "// INTERNAL VARIABLES" in line:
		var_start = False
		break
	if var_start:
		line = line.replace(prefix+'__DOT__','')
		print(line)
print("// ====== VARIABLE DECLARATION ENDS======")
# ---------------------------------------------------------------------------------------------------
			
functions = ["V"+prefix+"___024root___eval_static", "V"+prefix+"___024root___eval_initial", "V"+prefix+"___024root___eval_settle"]

for f in functions:
	exe(f, func_dict)
