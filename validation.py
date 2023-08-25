#!/usr/bin/env python3

def get_float(prompt, low, high):
    while True:
        number = float(input(prompt))
        if number > low and number <= high:
            is_valid = True
            return number
        else:
            print(f"This number must be greater than {low} and less than or equal to {high}. Please try again.")
            continue

def get_int(prompt, low, high):
    while True:
        number = int(input(prompt))
        if number > low and number <= high:
            is_valid = True
            return number
        else:
            print(f"This number must be greater than {low} and less than or equal to {high}. Please try again.")
            continue

def main():
    choice = "y"
    while choice.lower() == "y":
        # see if the user wants to continue
        choice = input("Continue? (y/n): ")
        print()

    print("Bye!")

if __name__ == "__main__":
    main()
