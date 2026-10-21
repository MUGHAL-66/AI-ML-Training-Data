selling_price = float(input("Enter selling price per bag: "))
profit_percentage = float(input("Enter profit percentage: "))
bags = int(input("Enter number of bags sold: "))

profit_per_bag = selling_price * (profit_percentage / 100)
total_profit = profit_per_bag * bags

print("Total Profit: $", total_profit)