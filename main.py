from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    items = []
    total = 0
    if request.method == 'POST':
        items = [
            {"nama": request.form.get('item1', 'CL 350'), "qty": int(request.form.get('qty1', 1)), "harga": 53500},
            {"nama": request.form.get('item2', 'CLEO 550'), "qty": int(request.form.get('qty2', 34)), "harga": 6125}
        ]
        for item in items:
            item['subtotal'] = item['qty'] * item['harga']
        total = sum([item['subtotal'] for item in items])
    else:
        items = [
            {"nama": 'CL 350', "qty": 1, "harga": 53500, "subtotal": 53500},
            {"nama": 'CLEO 550', "qty": 34, "harga": 6125, "subtotal": 206125}
        ]
        total = 53500 + 206125
    return render_template('index.html', items=items, total=total)

if __name__ == '__main__':
    app.run(debug=True)
