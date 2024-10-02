import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from collections import Counter

class ExpenseTracker:
    def __init__(self, filename='expenses.csv'):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                self.expenses = [row for row in reader]

    def add_expense(self, category, amount, date):
        expense = {'Category': category, 'Amount': amount, 'Date': date}
        self.expenses.append(expense)
        self.save_expenses()

    def save_expenses(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['Category', 'Amount', 'Date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.expenses)

    def visualize_expenses(self):
        categories = [expense['Category'] for expense in self.expenses]
        category_counts = Counter(categories)
        plt.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%')
        plt.title("Expenses by Category")
        plt.savefig('expenses_pie_chart.png')
        plt.close()

class App:
    def __init__(self, master):
        self.master = master
        self.tracker = ExpenseTracker()

        master.title("Personal Expense Tracker")

        self.label_category = tk.Label(master, text="Category")
        self.label_category.pack()
        self.entry_category = tk.Entry(master)
        self.entry_category.pack()

        self.label_amount = tk.Label(master, text="Amount")
        self.label_amount.pack()
        self.entry_amount = tk.Entry(master)
        self.entry_amount.pack()

        self.label_date = tk.Label(master, text="Date (YYYY-MM-DD)")
        self.label_date.pack()
        self.entry_date = tk.Entry(master)
        self.entry_date.pack()

        self.button_add = tk.Button(master, text="Add Expense", command=self.add_expense)
        self.button_add.pack()

        self.button_view = tk.Button(master, text="View Expenses", command=self.view_expenses)
        self.button_view.pack()

        self.button_visualize = tk.Button(master, text="Visualize Expenses", command=self.visualize_expenses)
        self.button_visualize.pack()

        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.pack()

    def add_expense(self):
        category = self.entry_category.get()
        amount = self.entry_amount.get()
        date = self.entry_date.get()

        if not category or not amount or not date:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        
        try:
            amount = float(amount)
            self.tracker.add_expense(category, amount, date)
            self.entry_category.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
            self.entry_date.delete(0, tk.END)
            messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount.")

    def view_expenses(self):
        self.text_output.delete(1.0, tk.END)
        expenses = self.tracker.expenses
        if not expenses:
            self.text_output.insert(tk.END, "No expenses available.\n")
            return
        for expense in expenses:
            self.text_output.insert(tk.END, f"{expense['Date']}: {expense['Category']} - ${expense['Amount']}\n")

    def visualize_expenses(self):
        self.tracker.visualize_expenses()
        messagebox.showinfo("Visualization", "Pie chart saved as 'expenses_pie_chart.png'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
