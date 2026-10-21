number = int(input("Enter a number: "))
if number % 2 == 0:
    print("Even Number")
else:
    print("Odd Number")


    #------------------------------------------------

year = int(input("Enter year: "))

if year % 400 == 0:
    print("Leap Year")

elif year % 4 == 0 and year % 100 != 0:
    print("Leap Year")

else:
    print("Not a Leap Year")

 #---------------------------------------------------

    year = int(input("Enter year: "))

if year % 4 == 0:
    print("Leap Year")
else:
    print("Not a Leap Year")