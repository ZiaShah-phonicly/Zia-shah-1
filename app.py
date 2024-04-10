from pymongo import MongoClient
from getpass import getpass

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users = db["users"]

def signup():
   
    username = input("Enter a username: ")
    email = input("Enter your email address: ")
    password = getpass("Enter a password: ")

    if users.find_one({"username": username}):
        print("Username already exists!")
        return

    user = {
        "username": username,
        "email": email,
        "password": password
    }

    users.insert_one(user)
    print("User created successfully!")

def login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    user = users.find_one({"username": username, "password": password})

    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")

def main():
    while True:
        print("\n1. Signup")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
