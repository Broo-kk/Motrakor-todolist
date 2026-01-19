"""Main entry point for the To-Do List CLI application.

This module implements the CLI interface with a REPL-style interaction.
"""

import json
import os
from models import TodoItem, Priority, Status

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


def display_post_login_menu(username):
    """Display the post-login menu options."""
    print("\n" + "=" * 40)
    print(f"  Welcome, {username}!")
    print("=" * 40)
    print("\n[1] Create To-Do Item")
    print("[2] View All To-Do Items")
    print("[3] View To-Do Item Details")
    print("[4] Mark To-Do as Completed")
    print("[5] Logout")
    print()


def get_post_login_choice():
    """Get and validate user's post-login menu choice.

    Returns:
        The user's choice as a string.
    """
    choice = input("Please select an option (1-5): ").strip()
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

# ================= Load & Save todos from/to JSON =============== 
def load_todos(filename="todos.json"):
    """Load todos from JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            todos_data = json.load(f)
            return [TodoItem.from_dict(todo) for todo in todos_data]
    return []

def save_todos(todos, filename="todos.json"):
    """Save todos to JSON file."""
    todos_data = [todo.to_dict() for todo in todos]
    with open(filename, 'w') as f:
        json.dump(todos_data, f, indent=4)

# =================== User Login here =================== 
def handle_login(users):
    """Handle the login process.
    
    Returns:
        The username if login is successful, None otherwise.
    """
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    # TODO: Implement login logic
    for user in users:
        if user.get("username") == username and str(user.get("password")) == password:
            print(f"Login successful! Welcome back, {username}!")
            return username
    print("Invalid username or password.")
    return None

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

# =================== Create Todo here ===================
def handle_create_todo(username):
    """Handle creating a new todo item.
    
    Args:
        username: The username of the current user.
    """
    print("\n--- Create To-Do Item ---")
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    
    details = input("Details: ").strip()
    
    print("\nPriority levels:")
    print("[1] HIGH")
    print("[2] MID")
    print("[3] LOW")
    priority_choice = input("Select priority (1-3): ").strip()
    
    priority_map = {"1": Priority.HIGH, "2": Priority.MID, "3": Priority.LOW}
    priority = priority_map.get(priority_choice, Priority.MID)
    
    # Create the todo item
    todo = TodoItem(
        title=title,
        details=details,
        priority=priority,
        owner=username
    )
    
    # Load existing todos, add the new one, and save
    todos = load_todos()
    todos.append(todo)
    save_todos(todos)
    
    print(f"\n✓ To-Do item '{title}' created successfully!")
    print(f"  ID: {todo.id}")
    print(f"  Priority: {priority.value}")
    print(f"  Status: {todo.status.value}")

# =================== Post-Login Menu Handler ===================
def handle_post_login_menu(username):
    """Handle the post-login menu loop.
    
    Args:
        username: The username of the current user.
    """
    while True:
        display_post_login_menu(username)
        choice = get_post_login_choice()
        
        if choice == "1":
            handle_create_todo(username)
        elif choice == "2":
            print("\n[TODO] View all to-do items - coming soon!")
        elif choice == "3":
            print("\n[TODO] View to-do item details - coming soon!")
        elif choice == "4":
            print("\n[TODO] Mark to-do as completed - coming soon!")
        elif choice == "5":
            print(f"\nLogging out... Goodbye, {username}!")
            break
        else:
            print("\nInvalid option. Please select 1-5.")

def main():
    """Main application loop.

    Implements a REPL (Read-Eval-Print Loop) for the CLI application.
    """
    
    print("Starting To-Do List Application...")

    while True:
        display_pre_login_menu()
        choice = get_user_choice()

        if choice == "1":
            users = load_users()
            username = handle_login(users)
            if username:
                handle_post_login_menu(username)
        elif choice == "2":
            handle_signup()
        elif choice == "3":
            print("\nThank you for using To-Do List Manager. Goodbye!")
            break
        else:
            print("\nInvalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
