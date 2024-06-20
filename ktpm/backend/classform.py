from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="register"
    )
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            object VARCHAR(255) NOT NULL,
            subject VARCHAR(255) NOT NULL,
            grade VARCHAR(255) NOT NULL,
            gender VARCHAR(255) NOT NULL,
            area VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            cond VARCHAR(255) NOT NULL
        )
    """)
    db.commit()
except mysql.connector.Error as err:
    app.logger.error(f"Error: {err}")

@app.route('/classform', methods=['POST'])
def form():
    try:
        data = request.json 
        app.logger.debug(f"Dữ liệu nhận được để đăng ký: {data}")
        
        if not data:
            return jsonify({"error": "Không có dữ liệu nào được cung cấp"}), 400

        object = data.get('object')
        subject = data.get('subject')  
        grade = data.get('grade')
        gender = data.get('gender')
        area = data.get('area')
        phone = data.get('phone')
        cond = data.get('cond')

        cursor = db.cursor()

        query = """
            INSERT INTO form (object, subject, grade, gender, area, phone, cond)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (object, subject, grade, gender, area, phone, cond)
        cursor.execute(query, values)
        db.commit()
        response = {'message': 'Thành công rồi, bạn giỏi quá!!!'}
    except mysql.connector.Error as err:
        app.logger.error(f"Lỗi: {err}")
        response = {'message': f'Lỗi: {err}'}
    finally:
        cursor.close()
    return jsonify(response)


if db.is_connected():
    print("Kết nối thành công đến cơ sở dữ liệu MySQL.")
else:
    print("Kết nối không thành công đến cơ sở dữ liệu MySQL.")

if __name__ == '__main__':
    app.run(port=5011)
