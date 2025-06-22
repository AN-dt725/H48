from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

df = pd.read_excel("data.xlsx")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/banhang', methods=['GET', 'POST'])
def banhang():
    ket_qua = []
    keyword = request.form.get("keyword", "").strip().lower()
    if keyword:
        ket_qua = df[df["Tên mặt hàng"].str.lower().str.contains(keyword) |
                     df["Loại hàng"].str.lower().str.contains(keyword)]
    return render_template("banhang.html", ket_qua=ket_qua, keyword=keyword)

@app.route('/tra', methods=['GET', 'POST'])
def tra():
    ket_qua = []
    keyword = request.form.get("keyword", "").strip().lower()
    if keyword:
        ket_qua = df[df["Tên mặt hàng"].str.lower().str.contains(keyword) |
                     df["Loại hàng"].str.lower().str.contains(keyword)]
    return render_template("tra.html", ket_qua=ket_qua, keyword=keyword)

@app.route('/tatca')
def tatca():
    return render_template("tatca.html", data=df.to_dict(orient="records"))

@app.route('/autocomplete')
def autocomplete():
    term = request.args.get('term', '').lower()
    matched = df[df["Tên mặt hàng"].str.lower().str.contains(term)]
    suggestions = [{"label": f'{row["Tên mặt hàng"]} - {row["Loại hàng"]} - {row["Giá"]}',
                    "value": row["Tên mặt hàng"],
                    "loai": row["Loại hàng"],
                    "gia": row["Giá"]}
                   for _, row in matched.iterrows()]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
