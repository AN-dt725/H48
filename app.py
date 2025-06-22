from flask import Flask, render_template, request, redirect, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATA_PATH = 'data.xlsx'

def load_data():
    return pd.read_excel(DATA_PATH)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/banhang', methods=['GET', 'POST'])
def banhang():
    df = load_data()
    keyword = ''
    selected_df = pd.DataFrame(columns=df.columns)

    # Giỏ hàng khởi tạo
    if 'cart' not in session:
        session['cart'] = []

    # Tìm sản phẩm
    ket_qua = None
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip().lower()

        if 'add' in request.form:
            item = request.form['add']
            session['cart'].append(item)
            session.modified = True

        elif 'remove' in request.form:
            item = request.form['remove']
            session['cart'] = [x for x in session['cart'] if x != item]
            session.modified = True

        elif keyword:
            ket_qua = df[df['Tên mặt hàng'].str.lower().str.contains(keyword)]

    # Lấy danh sách sản phẩm trong giỏ
    if session['cart']:
        selected_df = df[df['Tên mặt hàng'].isin(session['cart'])]
    total = selected_df['Giá'].sum()

    return render_template('banhang.html', keyword=keyword, ket_qua=ket_qua, selected=selected_df, total=total)

@app.route('/tatca')
def tatca():
    df = load_data()
    return render_template('tatca.html', data=df)

@app.route('/tra', methods=['GET', 'POST'])
def tra():
    df = load_data()
    keyword = ''
    ket_qua = None

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip().lower()
        if keyword:
            ket_qua = df[df['Tên mặt hàng'].str.lower().str.contains(keyword)]

    return render_template('tra.html', keyword=keyword, ket_qua=ket_qua)

if __name__ == '__main__':
    app.run(debug=True)