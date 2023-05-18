from flask import Flask, render_template
import yfinance as yf
# from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('./index.html')


@app.route("/get_stock_info/<stock_name>", methods=['GET'])
def get_stock_info(stock_name):
    stock = yf.Ticker(stock_name)

    # 모든 주식 정보를 가져옵니다.
    data = stock.info
    return data

# def cron_job():
#     stock = yf.Ticker('AAPL')
#
#     # 모든 주식 정보를 가져옵니다.
#     data = stock.info
#     print(data)
#
#     # 스케줄러를 실행한 후 1분 뒤에 스케줄러를 중지합니다.
#     elapsed_time = datetime.now() - start_time
#     if elapsed_time >= timedelta(minutes=1):
#         scheduler.shutdown()
#     return data

# @app.route("/get_live_stock_data/<second>", methods=['GET'])
# def get_live_stock_data(second):
#     # 스케줄러 시작 시간을 저장합니다.
#     start_time = datetime.now()
#
#     scheduler.add_job(cron_job, 'interval', seconds=int(second))
#     scheduler.start()
#
#
#     return render_template('./index.html')