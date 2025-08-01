def format_currency(amount):
    return f"${amount:,.2f}"

def add_new_item(inventory):
    name = input("Enter item name: ").strip()
    if not name:
        print("Item name cannot be empty.")
        return
    if name in inventory:
        print(f"{name} already exists in inventory.")
        return

    try:
        price_str = input("Enter price ($XX.XX): ").strip().replace("$", "")
        price = float(price_str)
        if price < 0:
            print("Price cannot be negative.")
            return
    except ValueError:
        print("Invalid price format.")
        return

    try:
        stock = int(input("Enter initial stock (integer): ").strip())
        if stock < 0:
            print("Stock cannot be negative.")
            return
    except ValueError:
        print("Invalid stock amount. Must be an integer.")
        return

    category = input("Enter category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    inventory[name] = {"price": price, "stock": stock, "category": category}
    print(f"Added {name} to inventory.")

def update_stock(inventory):
    if not inventory:
        print("Inventory is empty. Add items first.")
        return

    name = input("Enter item name to update stock: ").strip()
    if name not in inventory:
        print(f"{name} not found in inventory.")
        return

    try:
        change = int(input("Enter stock change (positive to add, negative to remove): ").strip())
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    new_stock = inventory[name]['stock'] + change
    if new_stock < 0:
        print(f"Cannot reduce stock below zero. Current stock: {inventory[name]['stock']}")
        return

    inventory[name]['stock'] = new_stock
    print(f"Updated stock for {name}. New stock: {new_stock}")

def search_by_category(inventory):
    if not inventory:
        print("Inventory is empty.")
        return

    category = input("Category to search: ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    found_items = [(item, data) for item, data in inventory.items() if data['category'].lower() == category.lower()]
    if not found_items:
        print(f"No items found in category '{category}'.")
        return

    print(f"Found {len(found_items)} item{'s' if len(found_items) > 1 else ''} in {category}:")
    for item, data in found_items:
        price_formatted = format_currency(data['price'])
        print(f"• {item} - {price_formatted} ({data['stock']} in stock)")

def low_stock_alert(inventory):
    low_stock_items = [(item, data['stock']) for item, data in inventory.items() if data['stock'] <= 5]
    if not low_stock_items:
        print("No low stock items (≤5 units).")
        return

    print("\n⚠️ LOW STOCK ALERT:")
    for item, stock in low_stock_items:
        unit_word = "unit" if stock == 1 else "units"
        print(f"- {item} ({stock} {unit_word} remaining)")

def calculate_inventory_value(inventory):
    total = sum(data['price'] * data['stock'] for data in inventory.values())
    return total

def main():
    inventory = {}

    while True:
        total_value = calculate_inventory_value(inventory)
        print("\n=== SMART INVENTORY MANAGER ===")
        print(f"Current Inventory Value: {format_currency(total_value)}\n")

        low_stock_alert(inventory)
        print("\nMenu Options:")
        print("1. Add new item")
        print("2. Update stock (add/remove)")
        print("3. Search items by category")
        print("4. Check low stock items (≤5 units)")
        print("5. Calculate total inventory value")
        print("6. Exit")
        choice = input("Choose option: ").strip()

        if choice == '1':
            add_new_item(inventory)
        elif choice == '2':
            update_stock(inventory)
        elif choice == '3':
            search_by_category(inventory)
        elif choice == '4':
            low_stock_alert(inventory)
        elif choice == '5':
            total_value = calculate_inventory_value(inventory)
            print(f"Total Inventory Value: {format_currency(total_value)}")
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
