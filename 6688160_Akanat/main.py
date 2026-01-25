"""
Simple Calculator Application

This is the main entry point for the calculator. It provides an interactive command-line interface.
"""

from calculator import add, subtract, multiply, divide


def display_menu():
    """Display the calculator menu."""
    print("\n" + "="*40)
    print("         SIMPLE CALCULATOR")
    print("="*40)
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
    print("="*40)


def main():
    """Main function to run the calculator."""
    print("Welcome to the Simple Calculator!")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "5":
            print("Thank you for using the calculator. Goodbye!")
            break
        
        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please select 1-5.")
            continue
        
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == "1":
                result = add(num1, num2)
                print(f"\n{num1} + {num2} = {result}")
            elif choice == "2":
                result = subtract(num1, num2)
                print(f"\n{num1} - {num2} = {result}")
            elif choice == "3":
                result = multiply(num1, num2)
                print(f"\n{num1} × {num2} = {result}")
            elif choice == "4":
                result = divide(num1, num2)
                print(f"\n{num1} ÷ {num2} = {result}")
        
        except ValueError as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Please enter valid numbers.")


if __name__ == "__main__":
    main()
