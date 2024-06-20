from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

db_status = "Chưa kết nối đến MySQL."

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="register"
    )
    if db.is_connected():
        db_status = "Kết nối thành công đến cơ sở dữ liệu MySQL."
        app.logger.info(db_status)
except mysql.connector.Error as err:
    db_status = f"Lỗi kết nối đến cơ sở dữ liệu MySQL: {err}"
    app.logger.error(db_status)

@app.route('/')
def home():
    return render_template('personalinfor.html', db_status=db_status)

@app.route('/userinfo', methods=['GET'])
def get_user_info():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    cursor = db.cursor(dictionary=True)
    query = "SELECT username, name, gender, role, area, phone, academic FROM users WHERE username = %s"
    app.logger.debug(f"Executing query: {query} with username={username}")
    
    try:
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        app.logger.debug(f"Query result: {result}")
    except mysql.connector.Error as err:
        app.logger.error(f"SQL Error: {err}")
        return jsonify({"error": "Database query error"}), 500
    finally:
        cursor.close()

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(port=5009, debug=True)
