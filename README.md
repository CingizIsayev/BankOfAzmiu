# Python Banking System

A simple command-line banking project written in Python. Users can create an account or log in, then use the banking menu to manage their account.

## Requirements

- Python 3

## Run

Open a terminal in the `BankTask` folder and run:

```powershell
python Login.py
```

Choose **Create account** to register, or **Login** to use an existing account.

## Project files

- `Login.py` - application and banking menu
- `data.txt` - account data stored as JSON
- `time.py` - countdown used after repeated failed login attempts

Account information, including passwords, is stored locally in `data.txt` as plain text. This project is for learning and demonstration only; do not use real or sensitive credentials.
