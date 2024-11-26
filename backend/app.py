from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        type TEXT,
                        category TEXT,
                        amount REAL,
                        date TEXT
                     )''')
    conn.commit()
    conn.close()

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        cursor.execute('INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)',
                       (data['type'], data['category'], data['amount'], data['date']))
        conn.commit()
        return jsonify({'message': 'Transaction added successfully'}), 201

    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    
    return jsonify(transactions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
