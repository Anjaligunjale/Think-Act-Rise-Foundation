# Guessing Game

import random

num=random.randint(1,100)

guess=int(input("Guess any Number between 1-100: "))

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

