import json
import subprocess
from datetime import date

with open('data.txt') as f: 
    users = json.load(f)

transactionamount = 0
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
        print("press enter to return to the main menu")
        input()

    elif userselection == "2":
        print("Your balance is:", users[username]["balance"])
        print("press enter to return to the main menu")
        input()

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
                print("press enter to return to the main menu")
                input()
            elif deposit_amount > remaining_limit:
                print(f"Daily deposit limit is ${daily_limit}. You can deposit up to ${remaining_limit} more today.")
                print("press enter to return to the main menu")
                input()
            else:
                users[username]["balance"] += deposit_amount
                daily_deposits[today] = deposited_today + deposit_amount
                users[username].setdefault("transaction_history", []).append({
                    "date": today,
                    "type": "deposit",
                    "amount": deposit_amount,
                })
                with open('data.txt', 'w') as f:
                    json.dump(users, f, indent=4)
                print("Deposit successful! Your new balance is:", users[username]["balance"])
                print("press enter to return to the main menu")
                input()
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
        print("press enter to return to the main menu")
        input()

    elif userselection == "6":
        history = users[username].get("transaction_history", [])
        if not history:
            print("No transactions found.")
        else:
            print("Transaction History:")
            for transaction in history:
                details = ""
                if transaction["type"] == "transfer":
                    details = f" ({transaction['direction']} {transaction['counterparty']})"
                elif transaction["type"] == "withdrawal" and transaction.get("commission", 0):
                    details = f" (commission: ${transaction['commission']:.2f})"
                print(
                    f"{transaction['date']} - {transaction['type'].title()}"
                    f"{details} - ${transaction['amount']:.2f}"
                )
        print("press enter to return to the main menu")
        input()

    elif userselection == "0":
        print("Exiting the program. Goodbye..")
        break




    elif userselection == "4":
        while True:
            today = date.today().isoformat()
            withdraw_amount = float(input("Enter the amount to withdraw: "))
            if withdraw_amount <= 0:
                print("Invalid withdrawal amount. Please enter a positive value.")
                print("press enter to return to the main menu")
                input()
                continue
            elif withdraw_amount > 1000:
                print("Withdrawal amount exceeds the maximum limit of $1000. Please enter a smaller amount.")
                print("press enter to return to the main menu")
                input()
                continue

            commission = withdraw_amount * 0.02 if withdraw_amount >= 500 else 0
            total_debit = withdraw_amount + commission
            if total_debit > users[username]["balance"]:
                print("Insufficient balance. Your current balance is:", users[username]["balance"])
                print("press enter to return to the main menu")
                input()
                continue

            remaining_limit = users[username].get("daily_withdrawal_limit", 1000)
            if total_debit > remaining_limit:
                print(f"Daily withdrawal limit exceeded. Remaining limit is: ${remaining_limit}")
                print("press enter to return to the main menu")
                input()
                continue

            users[username]["balance"] -= total_debit
            users[username]["daily_withdrawal_limit"] = remaining_limit - total_debit
            users[username].setdefault("transaction_history", []).append({
                "date": today,
                "type": "withdrawal",
                "amount": withdraw_amount,
                "commission": commission,
                "total_debit": total_debit,
            })
            with open('data.txt', 'w') as f:
                json.dump(users, f, indent=4)
            print(f"Withdrawal successful! Your new balance is: {users[username]['balance']}")
            print(f"Cash withdrawal remaining limit for today is: {users[username]['daily_withdrawal_limit']}")
            if commission:
                print(f"Commission: {commission}")
            else:
                print("No commission fee is charged for withdrawals of $500 or less.")
            print("press enter to return to the main menu")
            input()
            break

#5transfermoney
 
    elif userselection == "5":
        date_today = date.today().isoformat()
        recipient_username = input("Enter the recipient's username: ")
        if recipient_username not in users:
            print("Recipient username not found.")
            print("press enter to return to the main menu")
            input()
            continue
        if recipient_username == username:
            print("You cannot transfer money to your own account.")
            print("press enter to return to the main menu")
            input()
            continue

        transfer_amount = float(input("Enter the amount to transfer: "))
        if transfer_amount <= 0:
            print("Invalid transfer amount. Please enter a positive value.")
            print("press enter to return to the main menu")
            input()
            continue
        elif transfer_amount > users[username]["balance"]:
            print("Insufficient balance. Your current balance is:", users[username]["balance"])
            print("press enter to return to the main menu")
            input()
            continue
        else:
            if transactionamount <=5:
                users[username]["balance"] -= transfer_amount
                users[recipient_username]["balance"] += transfer_amount
                transactionamount += 1
                users[username].setdefault("transaction_history", []).append({
                    "date": date_today,
                    "type": "transfer",
                    "direction": "sent",
                    "amount": transfer_amount,
                    "counterparty": recipient_username,
                })
                users[recipient_username].setdefault("transaction_history", []).append({
                    "date": date_today,
                    "type": "transfer",
                    "direction": "received",
                    "amount": transfer_amount,
                    "counterparty": username,
                })
                with open('data.txt', 'w') as f:
                    json.dump(users, f, indent=4)
                print(f"Transfer successful! Your new balance is: {users[username]['balance']}")
                print(f"{transfer_amount} has been transferred to {recipient_username}.")
                print("press enter to return to the main menu")
                input()
            else:
                print("You have exceeded the maximum number of transactions for today. Please try again tomorrow.")
                print("press enter to return to the main menu")
                input()