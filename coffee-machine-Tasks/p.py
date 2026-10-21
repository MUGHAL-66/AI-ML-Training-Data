# Available resources
water = 500
milk = 300
coffee = 100
cups = 10
money = 0


# Coffee recipes
espresso = {
    "water": 50,
    "milk": 0,
    "coffee": 18,
    "cost": 50
}

latte = {
    "water": 200,
    "milk": 150,
    "coffee": 24,
    "cost": 100
}

cappuccino = {
    "water": 250,
    "milk": 100,
    "coffee": 24,
    "cost": 120
}


# Check available resources
def check_resources(drink):
    if water < drink["water"]:
        print("Sorry, there is not enough water.")
        return False

    elif milk < drink["milk"]:
        print("Sorry, there is not enough milk.")
        return False

    elif coffee < drink["coffee"]:
        print("Sorry, there is not enough coffee.")
        return False

    elif cups < 1:
        print("Sorry, there are no cups.")
        return False

    else:
        return True


# Show remaining resources
def show_resources():
    print("\nRemaining Resources:")
    print("Water:", water)
    print("Milk:", milk)
    print("Coffee:", coffee)
    print("Cups:", cups)
    print("Money:", money)


# Ask user for coffee choice
choice = input("What would you like? (espresso/latte/cappuccino): ")


# Select drink
if choice == "espresso":
    drink = espresso

elif choice == "latte":
    drink = latte

elif choice == "cappuccino":
    drink = cappuccino

else:
    print("Invalid choice")
    drink = None


# Check resources
if drink:
    if check_resources(drink):

        # Take payment
        payment = float(input("Enter money: "))

        # Check payment
        if payment >= drink["cost"]:

            # Calculate change
            change = payment - drink["cost"]

            # Add money
            money = money + drink["cost"]

            # Reduce resources
            water = water - drink["water"]
            milk = milk - drink["milk"]
            coffee = coffee - drink["coffee"]
            cups = cups - 1

            # Return change
            print("Your change is:", change)

            # Drink ready
            print("Here is your", choice, "☕ Enjoy!")

            # Show remaining resources
            show_resources()

        else:
            print("Sorry, not enough money.")

    else:
        print("Cannot make the drink.")