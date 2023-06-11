from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)


BUDGET_FILE = 'budget_data.csv'

@app.route('/')
def home():
    budget_data = load_budget_data()
    total_expenses = calculate_total_expenses(budget_data)
    return render_template('index.html', budget_data=budget_data, total_expenses=total_expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    date = request.form.get('date')
    description = request.form.get('description')
    amount = request.form.get('amount')

    if not date or not description or not amount:
        return redirect(url_for('home'))


    with open(BUDGET_FILE, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([date, description, amount])

    return redirect(url_for('home'))

def load_budget_data():
    budget_data = []
    try:
        with open(BUDGET_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    budget_data.append({'date': row[0], 'description': row[1], 'amount': float(row[2])})
    except FileNotFoundError:
        pass
    return budget_data

def calculate_total_expenses(budget_data):
    total = 0.0
    for expense in budget_data:
        total += expense['amount']
    return total

if __name__ == '__main__':
    app.run(debug=True)
