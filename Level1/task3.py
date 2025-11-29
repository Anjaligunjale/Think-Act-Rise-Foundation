import re

#Enter your email id 
email = input("Enter Your Email-id :")
#to validate the email id
valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

print("Valid email address." if valid else "Invalid email address.")