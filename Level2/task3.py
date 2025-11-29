# Password Strength Checker

import re

print("Primary conditions for password validation:\n" \
"Minimum 8 characters.\n" \
"The alphabet must be between [a-z]\n"\
"At least one alphabet should be of Upper Case [A-Z]\n"\
"At least 1 number or digit between [0-9].\n"\
"At least 1 character from [ _ or @ or $ ].\n")

password= input("Enter a strong Password : ")

flag=0
while True:
	if (len(password)<=8):
		flag=-1
		break
	elif not re.search('[A-Z]',password):
		flag=-1
		break
	elif not re.search('[a-z]',password):
		flag=-1
		break
	elif not re.search('[0-9]',password):
		flag=-1
		break
	elif not re.search('[_@$]',password):
		flag=-1
		break
	elif re.search('/s',password):
		flag=-1
		break
	else:
		flag=0
		print("Valid Password")
		break
if flag==-1:
	print("Invalid Password")
	








