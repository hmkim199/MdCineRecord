from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기
app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbMediRecord  # 'dbMediRecord'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/main')
def get_main_page():
    return render_template('main_page.html')


@app.route('/medicine/infos', methods=['GET'])
def read_infos():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    mediInfos = list(db.infos.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'msg': 'GET 연결되었습니다!', 'mediInfos': mediInfos})


@app.route('/medicine/record', methods=['GET'])
def read_records():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    records = list(db.records.find({}, {'_id': False}).sort('date'))

    print(records)

    return jsonify({'result': 'success', 'msg': 'GET 연결되었습니다!', 'records': records})


@app.route('/medicine/modify', methods=['POST'])
def post_record_modify():
    date_receive = request.form['date_give']
    hospN_receive = request.form['hospN_give']
    mdCineN_receive = request.form['mdCineN_give']
    memo_receive = request.form['memo_give']

    # DB에 삽입할 record 만들기
    record = {
        'date': date_receive,
        'hospName': hospN_receive,
        'mdCineName': mdCineN_receive,
        'memo': memo_receive
    }
    db.records.delete_one(record)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success'})


@app.route('/medicine/record', methods=['POST'])
def post_record():
    date_receive = request.form['date_give']
    hospN_receive = request.form['hospN_give']
    mdCineN_receive = request.form['mdCineN_give']
    memo_receive = request.form['memo_give']

    # DB에 삽입할 record 만들기
    record = {
        'date': date_receive,
        'hospName': hospN_receive,
        'mdCineName': mdCineN_receive,
        'memo': memo_receive
    }
    # reviews에 review 저장하기
    db.records.insert_one(record)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})


if __name__ == '__main__':
    app.run()
