#  Fibonacci Sequence

num1=0
num2=1
next_number=num2
count =1

fab=int(input("Enter a n th term of Fabonacci series: "))
fab=fab-2
print(num1 , num2 )
while count<= fab:
	print(next_number,end=" ")
	count+=1
	num1,num2= num2,next_number
	next_number=num1 + num2
print()
	