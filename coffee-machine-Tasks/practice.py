age = int(input("Enter your age: "))

if age > 20:
    print("Eligible for voting")
else:
    print("Not eligible for voting")

    age = int(input("Enter your age: "))

if age < 20:
    print("Under 20")
elif 20 <= age <= 35:
    print("Young")
elif 36 <= age <= 55:
    print("Mid-age")
else:
    print("Senior Citizen")