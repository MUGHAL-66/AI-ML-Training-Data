# Coffee Menu
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 200,
    },

    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 250,
    },

    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 300,
    }
}


# Starting profit
profit = 0


# Available resources
resources = {
    "water": 1000,
    "milk": 500,
    "coffee": 300,
}


# Welcome message
print("Welcome to the Manii Cafe..! ☕")


# Take customer name
name = input("Can I get your name please?\n> ")


# Get drink size
def get_size():

    res = input(
        "What size drink can I get for you?\n"
        "[s] Small\n"
        "[m] Medium\n"
        "[l] Large\n"
        "> "
    ).strip().lower()

    if res == "s":
        return "small"

    elif res == "m":
        return "medium"

    elif res == "l":
        return "large"

    else:
        print("Sorry, I didn't understand that input.")
        return get_size()


# Select size
selected_size = get_size()

print(f"You have selected a {selected_size} drink.")


# Check resources
def is_resource_sufficient(order_ingredients):

    # Check every ingredient
    for item in order_ingredients:

        # Check if enough resource is available
        if order_ingredients[item] > resources[item]:

            print(f"Sorry, there is not enough {item}.")
            return False

    # All resources are available
    print("Resources are sufficient.")
    return True


# Show remaining resources
def show_remaining_resources():

    print("\n----- Remaining Resources -----")
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: Rs{profit}")
    print("-------------------------------")


# Take payment
def process_rupees():

    print("\nPlease insert money.")

    total = int(
        input("How many Rupees are you giving?: ")
    )

    return total


# Check payment
def is_transaction_successful(
    money_received,
    drink_cost
):

    global profit

    if money_received >= drink_cost:

        # Calculate change
        change = money_received - drink_cost

        print(
            f"Here is your remaining money: Rs{change}"
        )

        # Add coffee price to profit
        profit += drink_cost

        return True

    else:

        print(
            "Sorry, that's not enough money. "
            "Money refunded."
        )

        return False


# Make coffee
def make_coffee(
    drink_name,
    order_ingredients
):

    # Subtract ingredients from resources
    for item in order_ingredients:

        resources[item] -= order_ingredients[item]

    print(f"\nHere is your {drink_name} ☕")
    print(f"Enjoy your coffee, {name}!")
    print("Thank you for visiting Manii Cafe ☕")

    # Show remaining resources
    show_remaining_resources()


# Ask for another coffee
def another_coffee():

    while True:

        answer = input(
            "\nWould you like another coffee? "
            "(yes/no): "
        ).strip().lower()

        if answer == "yes":
            return True

        elif answer == "no":
            return False

        else:
            print(
                "Please enter only yes or no."
            )


# Coffee machine
is_on = True


while is_on:

    # Ask customer for coffee
    choice = input(
        "\nWhat would you like? "
        "(espresso/latte/cappuccino): "
    ).strip().lower()


    # Turn machine off
    if choice == "off":

        is_on = False

        print("\nMachine is turned off.")


    # Show resources
    elif choice == "report":

        show_remaining_resources()


    # Check valid coffee
    elif choice in MENU:

        # Get selected coffee
        drink = MENU[choice]


        # Check resources
        if is_resource_sufficient(
            drink["ingredients"]
        ):

            # Take payment
            payment = process_rupees()


            # Check payment
            if is_transaction_successful(
                payment,
                drink["cost"]
            ):

                # Make coffee
                make_coffee(
                    choice,
                    drink["ingredients"]
                )


                # Ask if customer wants another coffee
                if another_coffee():

                    print(
                        f"\nSure {name}! "
                        "Let's get you another coffee. ☕"
                    )

                    # Continue the loop
                    continue

                else:

                    print(
                        f"\nThank you {name}! "
                        "Enjoy your coffee! ☕"
                    )

                    # Stop machine
                    is_on = False


    # Invalid coffee choice
    else:

        print(
            "I'm sorry, I did not understand "
            "your selection. "
            "Please enter a valid option."
        )


# Final message
print("\nThank you for using Manii Cafe! ☕")
print("Have a great day!")