"""
Console Interface Module

This module provides a simple console interface for user interaction.
It accepts user input from the console and calls the appropriate database operation functions.

The console interface allows users to:
1. Create a new user
2. Create a new product
3. Create a new order
4. List orders for a user
"""

from db_operations import create_user, create_product, create_order, list_orders


def print_menu():
    """Display the main menu options to the user."""
    print("\n" + "="*50)
    print("Order Management System - Console Interface")
    print("="*50)
    print("1. Create a new user")
    print("2. Create a new product")
    print("3. Create a new order")
    print("4. List orders for a user")
    print("5. Exit")
    print("="*50)


def handle_create_user():
    """
    Handle user creation from console input.
    
    Prompts the user for email and full name, then calls create_user().
    """
    print("\n--- Create New User ---")
    
    # Get user input
    email = input("Enter email: ").strip()
    full_name = input("Enter full name: ").strip()
    
    # Call database operation function
    result = create_user(email, full_name)
    
    # Display result
    print("\n✅ User created successfully!")
    print(f"   ID: {result['id']}")
    print(f"   Email: {result['email']}")
    print(f"   Full Name: {result['full_name']}")
    print(f"   Created At: {result['created_at']}")


def handle_create_product():
    """
    Handle product creation from console input.
    
    Prompts the user for product name and price, then calls create_product().
    """
    print("\n--- Create New Product ---")
    
    # Get user input
    name = input("Enter product name: ").strip()
    
    # Get price and convert to cents
    price_str = input("Enter price (e.g., 19.99 for $19.99): ").strip()
    try:
        price_dollars = float(price_str)
        price_cents = int(price_dollars * 100)  # Convert dollars to cents
    except ValueError:
        print("❌ Invalid price format. Please enter a number.")
        return
    
    # Call database operation function
    result = create_product(name, price_cents)
    
    # Display result
    print("\n✅ Product created successfully!")
    print(f"   ID: {result['id']}")
    print(f"   Name: {result['name']}")
    print(f"   Price: ${result['price_cents'] / 100:.2f}")


def handle_create_order():
    """
    Handle order creation from console input.
    
    Prompts the user for order details and items, then calls create_order().
    """
    print("\n--- Create New Order ---")
    
    # Get user input
    try:
        user_id = int(input("Enter user ID: ").strip())
    except ValueError:
        print("❌ Invalid user ID. Please enter a number.")
        return
    
    status = input("Enter order status (pending/paid/shipped/cancelled) [default: pending]: ").strip()
    if not status:
        status = "pending"
    
    # Get order items
    items = []
    print("\nEnter order items (press Enter with empty product_id to finish):")
    while True:
        try:
            product_id_str = input("  Product ID (or press Enter to finish): ").strip()
            if not product_id_str:
                break
            
            product_id = int(product_id_str)
            quantity = int(input("  Quantity: ").strip())
            
            items.append({
                "product_id": product_id,
                "quantity": quantity
            })
        except ValueError:
            print("❌ Invalid input. Please enter numbers.")
            continue
    
    if not items:
        print("❌ Order must have at least one item.")
        return
    
    # Call database operation function
    result = create_order(user_id, status, items)
    
    # Display result
    print("\n✅ Order created successfully!")
    print(f"   Order ID: {result['id']}")
    print(f"   User ID: {result['user_id']}")
    print(f"   Status: {result['status']}")
    print(f"   Created At: {result['created_at']}")
    print(f"   Total Amount: ${result['total_amount_cents'] / 100:.2f}")
    print(f"   Total Quantity: {result['total_quantity']}")
    print("\n   Items:")
    for item in result['items']:
        print(f"     - {item['product_name']}: {item['quantity']} x ${item['price_cents_at_purchase'] / 100:.2f}")


def handle_list_orders():
    """
    Handle listing orders from console input.
    
    Prompts the user for user ID, then calls list_orders().
    """
    print("\n--- List Orders for User ---")
    
    # Get user input
    try:
        user_id = int(input("Enter user ID: ").strip())
    except ValueError:
        print("❌ Invalid user ID. Please enter a number.")
        return
    
    # Call database operation function
    result = list_orders(user_id)
    
    # Display result
    print(f"\n📋 Found {result['total']} order(s) for user {user_id}:")
    
    if result['total'] == 0:
        print("   No orders found.")
    else:
        for order in result['orders']:
            print(f"\n   Order ID: {order['id']}")
            print(f"   User: {order['user_name']} (ID: {order['user_id']})")
            print(f"   Status: {order['status']}")
            print(f"   Created At: {order['created_at']}")
            print(f"   Total Amount: ${order['total_amount_cents'] / 100:.2f}")
            print(f"   Total Quantity: {order['total_quantity']}")
            print("   Items:")
            for item in order['items']:
                print(f"     - {item['product_name']} (ID: {item['product_id']}): "
                      f"{item['quantity']} x ${item['price_cents_at_purchase'] / 100:.2f}")


def main():
    """
    Main function that runs the console interface.
    
    Displays menu and handles user choices in a loop until user chooses to exit.
    """
    print("Welcome to Order Management System!")
    print("This is a simple console interface for database operations.")

    
    while True:
        # Display menu
        print_menu()
        
        # Get user choice
        choice = input("\nEnter your choice (1-5): ").strip()
        
        # Handle user choice
        if choice == "1":
            handle_create_user()
        elif choice == "2":
            handle_create_product()
        elif choice == "3":
            handle_create_order()
        elif choice == "4":
            handle_list_orders()
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    # Run the console interface
    main()

