Val1=float(input("Enter first Number: "))
Val2=float(input("Enter Second Number: "))

print("Please select operation -\n" \
        "1. Add\n" \
        "2. Subtract\n" \
        "3. Multiply\n" \
        "4. Divide\n" \
	"5. Modulus\n")
ope=int(input("Select operations from 1,2,3,4,5 \n"))

if ope==1:
	add=Val1+Val2
	print(Val1,"+",Val2,"=",add)
elif ope==2:
	sub=Val1-Val2
	print(Val1,"-",Val2,"=",sub)
elif ope==3:
	mul=Val1*Val2
	print(Val1,"*",Val2,"=",mul)
elif ope==4:
	div=Val1/Val2
	print(Val1,"/",Val2,"=",div)
elif ope==5:
	mod=Val1%Val2
	print(Val1,"%",Val2,"=",mod)
else:
	print("Enter a Correct option")
	

