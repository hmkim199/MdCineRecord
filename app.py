from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기
app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbMediRecord  # 'dbMediRecord'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/medicine/record', methods=['POST'])
def write_record():
    # 1. 클라이언트가 준 년도(year), 월(month), 일(day), 병원명(hos_name), 처방약 이름(medi_name), 메모(memo)
    year = request.form["year"]
    month = request.form["month"]
    day = request.form["day"]
    hos_name = request.form["hos_name"]
    medi_name = request.form["medi_name"]
    memo = request.form["memo"]

    print(year, month, day, hos_name, medi_name, memo)

    # 2. DB에 정보 삽입하기
    db.records.insert_one({'year': year, 'month': month, 'day': day, 'hos_name': hos_name, 'medi_name': medi_name, 'memo': memo})

    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '기록을 추가했습니다.'})


@app.route('/medicine/record', methods=['GET'])
def read_records():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    articles = list(db.records.find({}, {'_id': False}))

    print(articles)

    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'msg': 'GET 연결되었습니다!', 'articles': articles})


# @app.route('/medicine/info', methods=['POST'])
# def get_data_from_api():
#     # 공공 API로부터 데이터를 가져옴






@app.route('/medicine/record', methods=['POST'])
def post_record():
    # 1. 클라이언트로부터 데이터를 받기
    url = request.form["url"]
    comment = request.form["comment"]

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')["content"]
    image = soup.select_one('meta[property="og:image"]')["content"]
    desc = soup.select_one('meta[property="og:description"]')['content']

    db.articles.insert_one({'url': url, 'comment': comment, 'title': title, 'image': image, 'desc': desc})

    # 3. mongoDB에 데이터 넣기
    return jsonify({'result': 'success', 'msg': '메모가 작성되었습니다!'})


if __name__ == '__main__':
    app.run()
