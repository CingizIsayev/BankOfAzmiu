import json
import subprocess
from datetime import date

with open('data.txt') as f: 
    users = json.load(f)

wrong_attempt = 0
countdownamount = 0
while True:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username]["password"] == password:
        print("Login successful! You are logged in as", username, "." , "Your balance is", users[username]["balance"])
        break
    else:
        
        wrong_attempt += 1
        print("Invalid username or password. Incorrect attempts:", wrong_attempt)
        if wrong_attempt == 3:
            print("You are blocked for 60 seconds!")
            subprocess.run(["python", "time.py"])
            wrong_attempt = 0
            countdownamount += 1
            if countdownamount == 2:
                        print("You have exceeded the maximum number of attempts. Your card has been blocked. Please contact the bank for administrator.")
                        break



while True:
    print("====================================          PYTHON BANKING SYSTEM ==================================== Welcome, user01! " + "\n" + "1. View Account Information" + "\n" + "2. Check Balance" + "\n" + "3. Deposit Money" + "\n" + "4. Withdraw Money" + "\n" + "5. Transfer Money" + "\n" + "6. Transaction History" + "\n" + "7. Daily Limits" + "\n" + "8. Change Password" + "\n" + "9. Logout" + "\n" + "0. Exit" + "\n" + "==================================== Select an option:")
    userselection = input("Enter your selection: ")

    if userselection == "1":
        print("Account Information:")
        print("Username:", username)
        print("Balance:", users[username]["balance"])
        print("account_number:", users[username]["account_number"])
        print("Account status: Active")

    elif userselection == "2":
        print("Your balance is:", users[username]["balance"])

    elif userselection == "3":
        today = date.today().isoformat()
        daily_limit = users[username].get("daily_limit", 2000)
        daily_deposits = users[username].setdefault("daily_deposits", {})
        deposited_today = daily_deposits.get(today, 0)
        remaining_limit = max(0, daily_limit - deposited_today)

        while True:
            deposit_amount = float(input("Enter the amount to deposit: "))
            if deposit_amount <= 0:
                print("Invalid deposit amount. Please enter a positive value.")
            elif deposit_amount > remaining_limit:
                print(f"Daily deposit limit is ${daily_limit}. You can deposit up to ${remaining_limit} more today.")
            else:
                users[username]["balance"] += deposit_amount
                daily_deposits[today] = deposited_today + deposit_amount
                with open('data.txt', 'w') as f:
                    json.dump(users, f, indent=4)
                print("Deposit successful! Your new balance is:", users[username]["balance"])
                break

    elif userselection == "7":
        today = date.today().isoformat()
        daily_limit = users[username].get("daily_limit", 2000)
        deposited_today = users[username].get("daily_deposits", {}).get(today, 0)
        remaining_limit = max(0, daily_limit - deposited_today)
        json.dump(users, open('data.txt', 'w'), indent=4)
        print("Daily deposit calendar date:", today)
        print(f"Daily deposit limit: ${daily_limit}")
        print(f"Deposited today: ${deposited_today}")
        print(f"Remaining today: ${remaining_limit}")

    elif userselection == "0":
        print("Exiting the program. Goodbye <3")
        break




    elif userselection == "4":
        while True:
            today = date.today().isoformat()
            daily_limit = users[username].get("daily_withdrawal_limit", 1000)
            withdraw_amount = float(input("Enter the amount to withdraw: "))
            if withdraw_amount <= 0:
                print("Invalid withdrawal amount. Please enter a positive value.")
                break
            elif withdraw_amount > users[username]["balance"]:
                print("Insufficient balance. Your current balance is:", users[username]["balance"])
                break
            
            if withdraw_amount <= users[username]["daily_withdrawal_limit"]:

                if withdraw_amount > 500:
                    commission = withdraw_amount * 0.02
                    withdraw_amount += commission
                    users[username]["balance"] -= withdraw_amount
                    users[username]["daily_withdrawal_limit"] -= withdraw_amount
                    with open('data.txt', 'w') as f:
                        json.dump(users, f, indent=4)
                    print(f"Withdrawal successful! Your new balance is: {users[username]['balance']}")
                    print(f"Cash withdrawal remaining limit for today is: {users[username]['daily_withdrawal_limit']}")
                    print(f"Commission: {commission}")
                    break
                else:
                    users[username]["balance"] -= withdraw_amount
                    users[username]["daily_withdrawal_limit"] -= withdraw_amount
                    with open('data.txt', 'w') as f:
                        json.dump(users, f, indent=4)
                    print(f"Withdrawal successful! Your new balance is: {users[username]['balance']}")
                    print(f"Cash withdrawal remaining limit for today is: {users[username]['daily_withdrawal_limit']}")
                    print("No commission fee is charged for withdrawals of $500 or less.")
                    break
            elif withdraw_amount > 1000:
                print("Withdrawal amount exceeds the maximum limit of $1000. Please enter a smaller amount.")
                break
