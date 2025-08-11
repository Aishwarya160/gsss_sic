#Check is the given integer number is Even or not.

input_number= int(input("Enter a number to check if it is Even: "))

if input_number % 2 == 0:
    print("The given number", input_number, 'is an Even number')
else:
    print("The given number", input_number, 'is not an Even number')
