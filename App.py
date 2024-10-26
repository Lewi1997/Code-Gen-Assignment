from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Mock database to store transactions
transactions = []

# Function to calculate total income and expenses
def calculate_totals():
    income = sum(item['amount'] for item in transactions if item['type'] == 'income')
    expenses = sum(item['amount'] for item in transactions if item['type'] == 'expense')
    return income, expenses, income - expenses

@app.route('/')
def index():
    income, expenses, balance = calculate_totals()
    return render_template('index.html', income=income, expenses=expenses, balance=balance)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        type_ = request.form['type']
        
        transactions.append({
            'amount': amount,
            'category': category,
            'type': type_,
            'date': datetime.now()
        })
        
        return redirect(url_for('index'))
    
    return render_template('add_transaction.html')

@app.route('/summary')
def summary():
    income, expenses, balance = calculate_totals()
    categorized_expenses = {}
    
    # Organize expenses by category
    for item in transactions:
        if item['type'] == 'expense':
            if item['category'] not in categorized_expenses:
                categorized_expenses[item['category']] = 0
            categorized_expenses[item['category']] += item['amount']
    
    return render_template('summary.html', income=income, expenses=expenses, balance=balance, categorized_expenses=categorized_expenses)

if __name__ == '__main__':
    app.run(debug=True)
