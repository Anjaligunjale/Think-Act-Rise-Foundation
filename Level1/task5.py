# Palindrome Checker

string=input("Enter a String : ")

# Reversing entered String
rev=string[::-1]

# checking conditions for palindrome String
if string==rev:
	print(string ,"is a palindrome string")
else:
	print(string ,"is not a palindrome string") 