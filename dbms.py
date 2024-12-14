import tkinter as tk
from tkinter import messagebox
import mysql.connector

###### Database Connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bank_management_system"
    )

####### Main Screen
def main_screen():
    root = tk.Tk()
    root.title("Bank Account Management")
    root.geometry("400x400")
    root.configure(bg="#F9C0AB") 

    tk.Label(root, text="WELCOME to BANK NETWORKS", font=("Arial", 20, "bold"), bg="#F9C0AB", fg="#355F2E").pack(pady=20)
    tk.Button(root, text="Login", font=("Arial", 14), bg="#A8CD89", fg="white", command=login_screen).pack(pady=10)
    tk.Button(root, text="Register", font=("Arial", 14), bg="#A8CD89", fg="white", command=register_screen).pack(pady=10)

    root.mainloop()

##### Registration Screen
def register_screen():
    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        bank_account = entry_account.get()

        if username and password and bank_account:
            conn = connect_to_db()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (username, password, bank_account_number) 
                    VALUES (%s, %s, %s)
                """, (username, password, bank_account))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                register_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "All fields are required!")

    register_win = tk.Toplevel()
    register_win.title("Register")
    register_win.geometry("300x400")
    register_win.configure(bg="#F4E0AF")  

    tk.Label(register_win, text="Register", font=("Arial", 18, "bold"), bg="#F4E0AF", fg="#355F2E").pack(pady=10)

    tk.Label(register_win, text="Username", bg="#F4E0AF").pack(pady=5)
    entry_username = tk.Entry(register_win)
    entry_username.pack(pady=5)

    tk.Label(register_win, text="Password", bg="#F4E0AF").pack(pady=5)
    entry_password = tk.Entry(register_win, show="*")
    entry_password.pack(pady=5)

    tk.Label(register_win, text="Bank Account Number", bg="#F4E0AF").pack(pady=5)
    entry_account = tk.Entry(register_win)
    entry_account.pack(pady=5)

    tk.Button(register_win, text="Register", command=register_user, bg="#A8CD89", fg="white").pack(pady=10)

####### Login 
def login_screen():
    def login_user():
        account_number = entry_account.get()
        password = entry_password.get()

        if account_number and password:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users 
                WHERE bank_account_number = %s AND password = %s
            """, (account_number, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Success", "Login successful!")
                dashboard(user[0])  # Pass user ID
                login_win.destroy()
            else:
                messagebox.showerror("Error", "Invalid credentials!")
            conn.close()
        else:
            messagebox.showerror("Error", "All fields are required!")

    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x300")
    login_win.configure(bg="#A8CD89")  

    tk.Label(login_win, text="Login", font=("Arial", 18, "bold"), bg="#A8CD89", fg="#F4E0AF").pack(pady=10)

    tk.Label(login_win, text="Bank Account Number", bg="#A8CD89", fg="white").pack(pady=5)
    entry_account = tk.Entry(login_win)
    entry_account.pack(pady=5)

    tk.Label(login_win, text="Password", bg="#A8CD89", fg="white").pack(pady=5)
    entry_password = tk.Entry(login_win, show="*")
    entry_password.pack(pady=5)

    tk.Button(login_win, text="Login", command=login_user, bg="#355F2E", fg="white").pack(pady=10)

######## Dashboard
def dashboard(user_id):
    def check_balance():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]
        conn.close()
        messagebox.showinfo("Balance", f"Your current balance is: {balance} Taka")

    def deposit():
        amount = float(entry_amount.get())
        if amount > 0:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
            cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'deposit', %s)", (user_id, amount))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"{amount} Taka deposited successfully!")
            entry_amount.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Enter a valid amount")

    def withdraw():
        amount = float(entry_amount.get())
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]
        if amount > 0 and balance >= amount:
            cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
            cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'withdrawal', %s)", (user_id, amount))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"{amount} Taka withdrawn successfully!")
            entry_amount.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Insufficient funds or invalid amount")

    def transaction_history():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT transaction_type, amount, transaction_date 
            FROM transactions 
            WHERE user_id = %s 
            ORDER BY transaction_date DESC
        """, (user_id,))
        transactions = cursor.fetchall()
        conn.close()

        history_win = tk.Toplevel()
        history_win.title("Transaction History")
        history_win.geometry("400x300")
        history_win.configure(bg="#F9C0AB")
        tk.Label(history_win, text="Transaction History", font=("Arial", 18, "bold"), bg="#F9C0AB", fg="#355F2E").pack(pady=10)

        for t in transactions:
            tk.Label(history_win, text=f"{t[0].capitalize()}: {t[1]} Taka on {t[2]}", bg="#F9C0AB").pack()
#####-LOG OUT

    def logout():
        dashboard_win.destroy()
        main_screen()

    dashboard_win = tk.Toplevel()
    dashboard_win.title("Dashboard")
    dashboard_win.geometry("400x400")
    dashboard_win.configure(bg="#F4E0AF")  

    tk.Label(dashboard_win, text="Dashboard", font=("Arial", 18, "bold"), bg="#F4E0AF", fg="#355F2E").pack(pady=10)

    tk.Button(dashboard_win, text="Check Balance", command=check_balance, bg="#A8CD89", fg="white").pack(pady=10)

    tk.Label(dashboard_win, text="Amount:", bg="#F4E0AF").pack()
    entry_amount = tk.Entry(dashboard_win)
    entry_amount.pack(pady=5)

    tk.Button(dashboard_win, text="Deposit", command=deposit, bg="#355F2E", fg="white").pack(pady=10)
    tk.Button(dashboard_win, text="Withdraw", command=withdraw, bg="#355F2E", fg="white").pack(pady=10)
    tk.Button(dashboard_win, text="Transaction History", command=transaction_history, bg="#A8CD89", fg="white").pack(pady=10)
    tk.Button(dashboard_win, text="Logout", command=logout, bg="#F9C0AB", fg="#355F2E").pack(pady=10)

# Run the App
main_screen()