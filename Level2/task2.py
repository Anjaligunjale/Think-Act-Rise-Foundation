# Number Guesser

import random

# Sprcifing the Range between 1-10
num=random.randrange(1,10)

guess=int(input("Guess any Number: "))

# Checking for Number
while num!=guess:
	if guess<num:
		print("too low")
		guess=int(input("Enter Number again: "))
	elif guess>num:
		print("too high!")
		guess=int(input("Enter Number again: "))
	else:
		break
print("Congrats! You guessed it Right!!")

