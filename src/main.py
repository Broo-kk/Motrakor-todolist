"""Main entry point for the To-Do List CLI application.

This module implements the CLI interface with a REPL-style interaction.
"""


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


def handle_login():
    """Handle the login process."""
    print("\n--- Login ---")
    print("Login functionality coming soon...")
    # TODO: Implement login logic


def handle_signup():
    """Handle the signup process."""
    print("\n--- Sign Up ---")
    print("Sign up functionality coming soon...")
    # TODO: Implement signup logic


def main():
    """Main application loop.

    Implements a REPL (Read-Eval-Print Loop) for the CLI application.
    """
    print("Starting To-Do List Application...")

    while True:
        display_pre_login_menu()
        choice = get_user_choice()

        if choice == "1":
            handle_login()
        elif choice == "2":
            handle_signup()
        elif choice == "3":
            print("\nThank you for using To-Do List Manager. Goodbye!")
            break
        else:
            print("\nInvalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
