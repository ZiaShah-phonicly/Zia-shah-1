import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
from getpass import getpass

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users = db["users"]

def send_email(to_email, subject, body):
    # Set up email server
    smtp_server = "smtp.example.com"  # Update with your SMTP server
    smtp_port = 587  # Update with your SMTP port
    sender_email = "your_email@example.com"  # Update with your email address
    sender_password = "your_password"  # Update with your email password

    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

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

def reset_password():
    email = input("Enter your email address: ")
    user = users.find_one({"email": email})
    if user:
        new_password = getpass("Enter your new password: ")
        confirm_password = getpass("Confirm your new password: ")
        if new_password == confirm_password:
            users.update_one({"email": email}, {"$set": {"password": new_password}})
            send_email(email, "Password Reset Confirmation", "Your password has been successfully reset.")
            print("Password reset successful! Check your email for confirmation.")
        else:
            print("Passwords do not match. Please try again.")
    else:
        print("Email address not found. Please try again.")

def main():
    while True:
        print("\n1. Signup")
        print("2. Login")
        print("3. Reset Password")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            reset_password()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
