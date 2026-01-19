"""Main entry point for the To-Do List CLI application.

This module implements the CLI interface with a REPL-style interaction.
"""

import json
import os
from datetime import datetime
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
    print("[4] Edit To-Do Item")
    print("[5] Mark To-Do as Completed")
    print("[6] Logout")
    print()


def get_post_login_choice():
    """Get and validate user's post-login menu choice.

    Returns:
        The user's choice as a string.
    """
    choice = input("Please select an option (1-6): ").strip()
    return choice

# ================= Load & Save users from/to JSON =============== 
def load_users(filename="users.json"):
    """Load users from JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_users(users, filename="users.json"):
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

# ================= Load & Save login history from/to JSON =============== 
def load_login_history(filename="login_history.json"):
    """Load login history from JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_login_history(history, filename="login_history.json"):
    """Save login history to JSON file."""
    with open(filename, 'w') as f:
        json.dump(history, f, indent=4)

def log_login_attempt(username, success):
    """Log a login attempt to history file.
    
    Args:
        username: The username attempting to login.
        success: Boolean indicating if login was successful.
    """
    history = load_login_history()
    login_record = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "success": success
    }
    history.append(login_record)
    save_login_history(history)

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
            log_login_attempt(username, True)
            return username
    print("Invalid username or password.")
    log_login_attempt(username, False)
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

# =================== View All Todos here ===================
def handle_view_all_todos(username):
    """Handle viewing all to-do items for the current user.
    
    Args:
        username: The username of the current user.
    """
    todos = load_todos()
    user_todos = [todo for todo in todos if todo.owner == username]
    
    if not user_todos:
        print("\n✗ You have no to-do items yet.")
        return
    
    print("\n" + "=" * 80)
    print(f"  Your To-Do Items ({len(user_todos)} total)")
    print("=" * 80)
    
    for idx, todo in enumerate(user_todos, 1):
        status_symbol = "✓" if todo.status.value == "COMPLETED" else "○"
        print(f"\n[{idx}] {status_symbol} {todo.title}")
        print(f"    Priority: {todo.priority.value}")
        print(f"    Status: {todo.status.value}")
        if todo.details:
            print(f"    Details: {todo.details}")
        print(f"    Created: {todo.created_at}")
        print(f"    Updated: {todo.updated_at}")

# =================== View Todo Details here ===================
def handle_view_todo_details(username):
    """Handle viewing detailed information about a specific todo item.
    
    Args:
        username: The username of the current user.
    """
    todos = load_todos()
    
    # Get user's todos
    user_todos = [todo for todo in todos if todo.owner == username]
    
    if not user_todos:
        print("\n✗ You have no to-do items to view.")
        return
    
    print("\n--- View To-Do Item Details ---")
    print("\nYour to-do items:")
    for idx, todo in enumerate(user_todos, 1):
        status_symbol = "✓" if todo.status.value == "COMPLETED" else "○"
        print(f"[{idx}] {status_symbol} {todo.title}")
    
    try:
        choice = int(input("\nSelect item number to view (0 to cancel): ").strip())
        if choice == 0:
            return
        if choice < 1 or choice > len(user_todos):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return
    
    todo = user_todos[choice - 1]
    
    print("\n" + "=" * 60)
    print("  To-Do Item Details")
    print("=" * 60)
    print(f"\nTitle:        {todo.title}")
    print(f"Details:      {todo.details if todo.details else 'N/A'}")
    print(f"Priority:     {todo.priority.value}")
    print(f"Status:       {todo.status.value}")
    print(f"Owner:        {todo.owner}")
    print(f"Created:      {todo.created_at}")
    print(f"Updated:      {todo.updated_at}")
    print("=" * 60)

# =================== Edit Todo here ===================
def handle_edit_todo(username):
    """Handle editing an existing todo item.
    
    Args:
        username: The username of the current user.
    """
    todos = load_todos()
    
    # Get user's todos
    user_todos = [todo for todo in todos if todo.owner == username]
    
    if not user_todos:
        print("\n✗ You have no to-do items to edit.")
        return
    
    print("\n--- Edit To-Do Item ---")
    print("\nYour to-do items:")
    for idx, todo in enumerate(user_todos, 1):
        print(f"[{idx}] {todo.title} (Priority: {todo.priority.value}, Status: {todo.status.value})")
    
    try:
        choice = int(input("\nSelect item number to edit (0 to cancel): ").strip())
        if choice == 0:
            return
        if choice < 1 or choice > len(user_todos):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return
    
    todo_to_edit = user_todos[choice - 1]
    
    print(f"\nEditing: '{todo_to_edit.title}'")
    print("\nWhat would you like to edit?")
    print("[1] Title")
    print("[2] Details")
    print("[3] Priority")
    print("[4] Cancel")
    
    edit_choice = input("Select option (1-4): ").strip()
    
    if edit_choice == "1":
        new_title = input("New title: ").strip()
        if new_title:
            todo_to_edit.title = new_title
    elif edit_choice == "2":
        new_details = input("New details: ").strip()
        if new_details:
            todo_to_edit.details = new_details
    elif edit_choice == "3":
        print("\nPriority levels:")
        print("[1] HIGH")
        print("[2] MID")
        print("[3] LOW")
        priority_choice = input("Select priority (1-3): ").strip()
        priority_map = {"1": Priority.HIGH, "2": Priority.MID, "3": Priority.LOW}
        if priority_choice in priority_map:
            todo_to_edit.priority = priority_map[priority_choice]
    elif edit_choice == "4":
        return
    else:
        print("Invalid option.")
        return
    
    # Update the timestamp
    from datetime import datetime
    todo_to_edit.updated_at = datetime.now().isoformat()
    
    # Find and update the original todo in the list
    for i, todo in enumerate(todos):
        if todo.id == todo_to_edit.id:
            todos[i] = todo_to_edit
            break
    
    save_todos(todos)
    print(f"\n✓ To-Do item updated successfully!")

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
            handle_view_all_todos(username)
        elif choice == "3":
            handle_view_todo_details(username)
        elif choice == "4":
            handle_edit_todo(username)
        elif choice == "5":
            print("\n[TODO] Mark to-do as completed - coming soon!")
        elif choice == "6":
            print(f"\nLogging out... Goodbye, {username}!")
            break
        else:
            print("\nInvalid option. Please select 1-6.")

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
