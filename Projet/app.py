from flask import Flask
from load_products import load_products
from render_html import render_html

app = Flask(__name__)


@app.get("/")
def home():
    return render_html()


@app.post("/load")
def load():
    try:
        products = load_products()
        return render_html(products)
    except Exception as e:
        return render_html(error_msg=str(e))


if __name__ == "__main__":
    app.run(debug=True)
