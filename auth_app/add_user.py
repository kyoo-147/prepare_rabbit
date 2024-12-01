import mysql.connector
import bcrypt

# Kết nối tới cơ sở dữ liệu
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456789Mc@',
    database='user_db'
)

cursor = conn.cursor()

# Người dùng mẫu
username = 'admin'
password = 'password123'

# Mã hóa mật khẩu
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Chèn người dùng vào bảng
cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
conn.commit()

cursor.close()
conn.close()
