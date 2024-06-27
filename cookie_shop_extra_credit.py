import csv

def bake_cookies(filepath):
    """
    Opens up the CSV data file from the path specified as an argument.
    - Each line in the file, except the first, is assumed to contain comma-separated information about one cookie.
    - Creates a dictionary with the data from each line.
    - Adds each dictionary to a list of all cookies that is returned.

    :param filepath: The path to the data file.
    :returns: A list of all cookie data, where each cookie is represented as a dictionary.
    """
    cookies = []
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cookie = {
                'id': int(row['id']),
                'title': row['title'],
                'description': row['description'],
                'price': float(row['price'].replace('$', '').replace(',', '')),
                'sugar_free': row['sugar_free'].lower() in ['true', 'yes', '1'],
                'gluten_free': row['gluten_free'].lower() in ['true', 'yes', '1'],
                'contains_nuts': row['contains_nuts'].lower() in ['true', 'yes', '1']
            }
            cookies.append(cookie)
    return cookies

def welcome():
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.")
    print("\nWe'd hate to trigger an allergic reaction in your body. So please answer the following questions:")

    sugar_free = input("Are you avoiding sugar? (yes/no): ").strip().lower() in ['yes', 'y']
    gluten_free = input("Are you allergic to gluten? (yes/no): ").strip().lower() in ['yes', 'y']
    contains_nuts = input("Are you allergic to nuts? (yes/no): ").strip().lower() in ['yes', 'y']
    
    return sugar_free, gluten_free, contains_nuts

def display_cookies(cookies, dietary_needs=None):
    """
    Takes a list of cookie dictionaries and prints out each one in a user-friendly way.
    Filters based on dietary needs if provided.
    """
    if dietary_needs:
        sugar_free, gluten_free, contains_nuts = dietary_needs
        filtered_cookies = [cookie for cookie in cookies if
                            (not sugar_free or cookie['sugar_free']) and
                            (not gluten_free or cookie['gluten_free']) and
                            (not contains_nuts or not cookie['contains_nuts'])]
    else:
        filtered_cookies = cookies

    if not filtered_cookies:
        print("No cookies match your dietary needs.")
        return

    print("\nHere are the cookies we have in the shop for you:\n")
    for cookie in filtered_cookies:
        print(f"#{cookie['id']} - {cookie['title']}")
        print(f"{cookie['description']}")
        print(f"Price: ${cookie['price']:.2f}\n")

def get_cookie_from_dict(cookies, cookie_id):
    """
    Takes a list of cookie dictionaries and a cookie id, 
    returns the cookie dictionary with the corresponding id.
    """
    for cookie in cookies:
        if cookie['id'] == cookie_id:
            return cookie
    return None

def solicit_quantity():
    """
    Solicits a quantity from the user, ensuring it is a positive integer.
    """
    while True:
        try:
            quantity = int(input("How many cookies would you like to buy? "))
            if quantity > 0:
                return quantity
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid number.")

def display_order_total(cookie, quantity):
    """
    Takes a cookie dictionary and a quantity, 
    displays the total cost for that quantity of cookies.
    """
    total = cookie['price'] * quantity
    print(f"Your total for {quantity} {cookie['title']} is ${total:.2f}")

def solicit_order(cookies):
    """
    Solicits an order from the user by getting a valid cookie ID and quantity.
    """
    orders = []
    while True:
        user_input = input("Enter the ID of the cookie you'd like to order (or type 'finished' to complete your order): ").strip().lower()
        if user_input in ['finished', 'done', 'quit', 'exit']:
            break
        try:
            cookie_id = int(user_input)
            cookie = get_cookie_from_dict(cookies, cookie_id)
            if cookie:
                quantity = solicit_quantity()
                orders.append((cookie, quantity))
                display_order_total(cookie, quantity)
            else:
                print("Invalid cookie ID. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    return orders

def display_final_order(orders):
    """
    Displays the final order summary and total cost.
    """
    print("\nThank you for your order. You have ordered:\n")
    total_cost = 0
    for cookie, quantity in orders:
        total_cost += cookie['price'] * quantity
        print(f"- {quantity} {cookie['title']}")
    
    print(f"\nYour total is ${total_cost:.2f}.")
    print("Please pay with Bitcoin before picking-up.")
    print("\nThank you!\n-The Python Cookie Shop Robot.")

def main():
    cookies = bake_cookies("data/cookies.csv")
    dietary_needs = welcome()
    display_cookies(cookies, dietary_needs)
    orders = solicit_order(cookies)
    if orders:
        display_final_order(orders)
    else:
        print("No order was placed.")

if __name__ == "__main__":
    main()
