from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="register"
        )
        if db.is_connected():
            app.logger.info("Kết nối thành công đến cơ sở dữ liệu MySQL.")
            return db
    except mysql.connector.Error as err:
        app.logger.error(f"Lỗi kết nối đến cơ sở dữ liệu MySQL: {err}")
        return None

@app.route('/students', methods=['GET'])
def get_students():
    object_filter = request.args.get('object', default='', type=str)
    subject_filter = request.args.get('subject', default='', type=str)
    grade_filter = request.args.get('grade', default='', type=str)
    gender_filter = request.args.get('gender', default='', type=str)
    area_filter = request.args.get('area', default='', type=str)

    query = "SELECT * FROM form WHERE 1=1"
    filters = []

    if object_filter:
        query += " AND object LIKE %s"
        filters.append(f"%{object_filter}%")
    if subject_filter:
        query += " AND subject LIKE %s"
        filters.append(f"%{subject_filter}%")
    if grade_filter:
        query += " AND grade LIKE %s"
        filters.append(f"%{grade_filter}%")
    if gender_filter:
        query += " AND gender LIKE %s"
        filters.append(f"%{gender_filter}%")
    if area_filter:
        query += " AND area LIKE %s"
        filters.append(f"%{area_filter}%")
        
    query += " ORDER BY id DESC"

    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, filters)
        students = cursor.fetchall()
        db.close()
        return jsonify(students)
    else:
        return jsonify({"error": "Không thể kết nối đến cơ sở dữ liệu"}), 500

@app.route('/')
def index():
    return send_from_directory('.', 'search.html')

if __name__ == '__main__':
    app.run(port=5012, debug=True)
