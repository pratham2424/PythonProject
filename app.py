from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data structures for books, members, and transactions
books = []
members = []
transactions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
def books_view():
    if request.method == 'POST':
        book = {
            'id': len(books) + 1,
            'title': request.form['title'],
            'author': request.form['author'],
            'quantity': int(request.form['quantity']),
        }
        books.append(book)
        return redirect(url_for('books_view'))
    return render_template('books.html', books=books)

@app.route('/members', methods=['GET', 'POST'])
def members_view():
    if request.method == 'POST':
        member = {
            'id': len(members) + 1,
            'name': request.form['name'],
            'outstanding_debt': 0,
        }
        members.append(member)
        return redirect(url_for('members_view'))
    return render_template('members.html', members=members)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions_view():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'book_id': int(request.form['book_id']),
            'member_id': int(request.form['member_id']),
            'type': request.form['type'],  # 'issue' or 'return'
            'fee': 0 if request.form['type'] == 'issue' else 100,  # Flat fee on return
        }

        member = next(m for m in members if m['id'] == transaction['member_id'])
        book = next(b for b in books if b['id'] == transaction['book_id'])

        if transaction['type'] == 'issue':
            if book['quantity'] > 0 and member['outstanding_debt'] <= 500:
                book['quantity'] -= 1
                transactions.append(transaction)
        elif transaction['type'] == 'return':
            book['quantity'] += 1
            member['outstanding_debt'] += transaction['fee']
            transactions.append(transaction)
        return redirect(url_for('transactions_view'))
    return render_template('transactions.html', transactions=transactions, books=books, members=members)

if __name__ == '__main__':
    app.run(debug=True)
