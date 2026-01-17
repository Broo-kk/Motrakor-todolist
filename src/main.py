"""Main entry point for the To-Do List CLI application.

This module implements the CLI interface with a REPL-style interaction.
"""

import json
import os

def display_pre_login_menu():
    """Display the pre-login menu options."""
    print("\n" + "=" * 40)
    print("  Welcome to To-Do List Manager")
    print("=" * 40)
    print("\n[1] Login")
    print("[2] Sign Up")
    print("[3] Exit")
    print()


def get_user_choice():
    """Get and validate user's menu choice.

    Returns:
        The user's choice as a string.
    """
    choice = input("Please select an option (1-3): ").strip()
    return choice

# ================= Load & Save users from/to JSON =============== 
def load_users(filename="login.json"):
    """Load users from JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_users(users, filename="login.json"):
    """Save users to JSON file."""
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)

# =================== User Login here =================== 
def handle_login(users):
    """Handle the login process."""
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    # TODO: Implement login logic
    for user in users:
        if user.get("username") == username and str(user.get("password")) == password:
            print(f"Login successful! Welcome back, {username}!")
            return
    print("Invalid username or password.")

# =================== User Signup here ===================
def handle_signup():
    """Handle the signup process."""
    print("\n--- Sign Up ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    users = load_users()
    # TODO: Implement login logic
    # Check if username already exists
    for user in users:
        if user.get("username") == username:
            print("Username already exists. Please choose another.")
            return

    users.append({"username": username, "password": password})
    save_users(users)
    print(f"Account created successfully! Welcome, {username}!")

def main():
    """Main application loop.

    Implements a REPL (Read-Eval-Print Loop) for the CLI application.
    """

    users = [{}]  # Placeholder for user data storage

    print("Starting To-Do List Application...")

    while True:
        display_pre_login_menu()
        choice = get_user_choice()

        if choice == "1":
            users = load_users()
            handle_login(users)
        elif choice == "2":
            handle_signup()
        elif choice == "3":
            print("\nThank you for using To-Do List Manager. Goodbye!")
            break
        else:
            print("\nInvalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
