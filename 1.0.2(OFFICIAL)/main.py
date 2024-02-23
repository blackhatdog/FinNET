from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import time 
from datetime import date



app = Flask(__name__)
db = TinyDB('finance_db.json')
transactions_table = db.table('transactions')

logusr=[]
str='9658'
         
class Transaction:
    def __init__(self, date, name, amount, mode):
        self.date = date
        self.name = name
        self.amount = amount
        self.mode = mode

def save_transaction(date, name, amount, mode):
    transaction = {'date': date, 'name': name, 'amount': amount, 'mode': mode}
    transactions_table.insert(transaction)

def calculate_balance():
    balance = 0
    for transaction in transactions_table.all():
        if transaction['mode'] == 'credit':
            balance += transaction['amount']
        elif transaction['mode'] == 'debit':
            balance -= transaction['amount']
    return balance
def get_transactions_by_mode(mode):
    return transactions_table.search(Query().mode == mode)


@app.route('/')  
def loginr():  
      return render_template("login.html")

@app.route('/fx', methods=['POST'])
def fork():
    ip_addr = request.remote_addr
    
    password = request.form['psd']
    if (password == str):
        logusr.append(ip_addr)
        sk1=ip_addr in logusr
        

        return '''<meta http-equiv="Refresh" content="0; url='/dash'" />'''
    else:
        
        return render_template('404.html')


@app.route('/dash')
def home():
    ipaddr2=request.remote_addr
    if ipaddr2 not in logusr:
         return render_template('404.html')
    else:
        transactions = transactions_table.all()
        balance = calculate_balance()
        return render_template('index.html', transactions=transactions, balance=balance)

    
    

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.remote_addr not in logusr:
        return render_template('404.html')
    else:
        if request.method == 'POST':
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            name = request.form['name']
            amount = float(request.form['amount'])
            mode = request.form['mode']
            save_transaction(date, name, amount, mode)
            return redirect(url_for('home'))
        return render_template('add_transaction.html')

@app.route('/credits')
def credits():
    if request.remote_addr not in logusr:
        return render_template('404.html')
    else:
        credit_transactions = get_transactions_by_mode('credit')
        return render_template('credits.html', credits=credit_transactions)

@app.route('/debits')
def debits():
    if request.remote_addr not in logusr:
        return render_template("404.html")
    else:
        debit_transactions = get_transactions_by_mode('debit')
        return render_template('debits.html', debits=debit_transactions)

@app.route('/dwcp')  
def logir():  
      if request.remote_addr not in logusr:
          return render_template("404.html")
      else:
          return render_template("dwcp.html")

@app.route('/format', methods=['POST'])
def form():
    ip_addr = request.remote_addr
    password = request.form['psd']
    if (password == str):
        transactions_table.truncate()
        return '''Format Success Redirecting...<meta http-equiv="Refresh" content="0; url='/dash'" />'''
    else:
        
        return render_template('404.html')
    
@app.route('/about')
def abt():
    ip_addr3=request.remote_addr
    if ip_addr3 in logusr:
        
        return render_template('about.html')
    else:
        
        return render_template('404.html')
@app.route('/logout')
def lgt():
    if request.remote_addr in logusr:
        
        logusr.remove(request.remote_addr)
        return '''<meta http-equiv="Refresh" content="0; url='/'" />'''
    else:
        
        return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
