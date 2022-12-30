from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
import pymysql


app = Flask(__name__)
CORS(app)
connection = pymysql.connect(host='database2.czy1sygl9ixu.ap-northeast-1.rds.amazonaws.com',
                             user='admin',
                             password='admin123',
                             db='database2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

@app.route('/fetch')
def facilityy():
    with connection.cursor() as cursor:
            sql = "SELECT * FROM `students`"
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            resp=jsonify(result[0])
            print(resp)
            print(result)
            return resp


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

