#!/usr/bin/env python3

# display a welcome message
print("The Miles Per Gallon program")
print()

# get input from the user
response = "y"
while response.lower() == "y":
    miles_driven = float(input("Enter miles driven:\t\t"))
    gallons_used = float(input("Enter gallons of gas used:\t"))
    cost_per_gallon = float(input("Enter cost per gallon:\t\t"))
    print()

# validate the input
    if miles_driven <= 0:
        print("Miles driven must be greater than zero. Please try again.")
    elif gallons_used <= 0:
        print("Gallons used must be greater than zero. Please try again.")
    elif cost_per_gallon <= 0:
        print("The cost per gallon must be greater than zero. Please try again.")
    else:
        mpg = round(miles_driven / gallons_used, 2)
        gas_cost = round(gallons_used * cost_per_gallon, 1)
        total_cost = round(gas_cost / miles_driven, 1)
        print("Miles Per Gallon:\t\t", mpg)
        print("Total Gas Cost:\t\t\t", gas_cost)
        print("Cost Per Mile:\t\t\t", total_cost)
        print()

    response = input("Get entries for another trip (y/n)? ")
    print()
  
print("Bye!")



