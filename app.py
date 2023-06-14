from dotenv import load_dotenv
import os
import pickle
from flask import Flask, render_template
import yfinance as yf
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from confluent_kafka import Producer

app = Flask(__name__)

load_dotenv(".env")

# 토픽 이름 설정
topic = 'sufka-topic-1'

# Kafka Producer 설정
producer = Producer({'bootstrap.servers': os.getenv("KAFKA_SERVER")})

# 메시지 전송 콜백 함수
def delivery_callback(err, msg):
    if err is not None:
        print(f'메시지 전송 실패: {err}')
    else:
        print(f'메시지 전송 성공: {msg.topic()} [{msg.partition()}]')


@app.route("/")
def index():
    return render_template('./index.html')


@app.route("/get_stock_info/<stock_name>", methods=['GET'])
def get_stock_info(stock_name):
    stock = yf.Ticker(stock_name)

    # 모든 주식 정보를 가져옵니다.
    data = stock.info
    return data


def kafka_send_stock_info():
    stock = yf.Ticker('AAPL')

    # 모든 주식 정보를 가져옵니다.
    data = stock.info

    # 지정 kafka 로 데이터를 보냅니다.
    producer.produce(topic, value=pickle.dumps(data), callback=delivery_callback)
    # 모든 메시지 전송 완료 대기
    producer.flush()
    return data


scheduler = BackgroundScheduler(max_instances=10)


# 매 초 마다 카프카에 주식 정보를 하나 씩 보내는 함수를 실행
@app.route("/kafka/send_stock_info/start", methods=['POST'])
def kafka_send_stock_info_start():
    scheduler.start()
    scheduler.add_job(func=kafka_send_stock_info, trigger="interval", seconds=1, id='kafka-send-stock-info')
    return "send start"

# 매 초 마다 카프카에 주식 정보를 하나 씩 보내는 함수를 중단
@app.route("/kafka/send_stock_info/stop", methods=['POST'])
def kafka_send_stock_info_stop():
    scheduler.remove_job('kafka-send-stock-info')
    return "send stop"
