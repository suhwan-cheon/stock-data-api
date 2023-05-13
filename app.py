from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('./index.html')

@app.route("/get_stock")
def get_stock():
    msft = yf.Ticker("MSFT")

    # get all stock info
    data = msft.info
    print(data)
    return render_template('./index.html')
