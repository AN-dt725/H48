from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_excel("data.xlsx")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/banhang', methods=['GET', 'POST'])
def banhang():
    ket_qua = []
    keyword = request.form.get("keyword", "").strip().lower()
    if keyword:
        ket_qua = df[
            df["Tên mặt hàng"].str.lower().str.contains(keyword) |
            df["Loại hàng"].str.lower().str.contains(keyword)
        ]
    return render_template("banhang.html", ket_qua=ket_qua, keyword=keyword)

@app.route('/autocomplete')
def autocomplete():
    term = request.args.get("term", "").strip().lower()
    results = []
    if term:
        matched = df[
            df["Tên mặt hàng"].str.lower().str.contains(term) |
            df["Loại hàng"].str.lower().str.contains(term)
        ]
        for _, row in matched.iterrows():
            results.append({
                "name": row["Tên mặt hàng"],
                "type": row["Loại hàng"],
                "price": row["Giá"]
            })
    return jsonify(results)

@app.route('/tra', methods=['GET', 'POST'])
def tra():
    ket_qua = []
    keyword = request.form.get("keyword", "").strip().lower()
    if keyword:
        ket_qua = df[
            df["Tên mặt hàng"].str.lower().str.contains(keyword) |
            df["Loại hàng"].str.lower().str.contains(keyword)
        ]
    return render_template("tra.html", ket_qua=ket_qua, keyword=keyword)

@app.route('/tatca')
def tatca():
    return render_template("tatca.html", data=df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)