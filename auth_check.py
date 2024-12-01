# import sys
# from PyQt5 import QtWidgets, uic
# import mysql.connector
# from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtCore import Qt
# import bcrypt

# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         # Tải file UI từ main_window.ui
#         uic.loadUi('auth_app/log_in.ui', self)
        
#         # Kết nối các sự kiện
#         self.pushButton_sign_in.clicked.connect(self.sign_in)
#         self.pushButton_JoinNow.clicked.connect(self.open_registration_window)
        
#         # Kết nối nút ẩn/hiện mật khẩu với phương thức toggle_password_visibility
#         self.pushButton_show_hide.clicked.connect(self.toggle_password_visibility)
        
#         # Cờ để theo dõi trạng thái hiển thị mật khẩu
#         self.password_visible = False

#         # Kết nối đến cơ sở dữ liệu
#         self.db_connection = self.connect_to_db()

    
#     def connect_to_db(self):
#         try:
#             # Kết nối đến cơ sở dữ liệu MySQL
#             connection = mysql.connector.connect(
#                 host='localhost',
#                 user='root',
#                 password='123456789Mc@',
#                 database='user_db'
#             )
#             print("Connected to the database successfully!")
#             return connection
#         except mysql.connector.Error as e:
#             print(f"Error connecting to the database: {e}")
#             return None

#     def sign_in(self):
#         # Lấy thông tin đăng nhập từ giao diện
#         email = self.lineEdit_login_email.text()
#         password = self.lineEdit_login_password.text()

#         if self.db_connection:
#             try:
#                 cursor = self.db_connection.cursor()
#                 sql = "SELECT password FROM users WHERE username = %s"
#                 cursor.execute(sql, (email,))
#                 result = cursor.fetchone()

#                 if result:
#                     stored_password = result[0]
#                     if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
#                         QMessageBox.information(self, "Thành Công", "Đăng nhập thành công!")
#                         print("Login successful!")
#                     else:
#                         QMessageBox.warning(self, "Lỗi", "Mật khẩu không đúng.")
#                         print("Password is incorrect.")
#                 else:
#                     QMessageBox.warning(self, "Lỗi", "Tài khoản không tồn tại.")
#                     print("Account does not exist.")

#                 cursor.close()
#             except mysql.connector.Error as e:
#                 print(f"Error during login: {e}")
#                 QMessageBox.warning(self, "Lỗi", f"Đăng nhập thất bại: {e}")
#         else:
#             QMessageBox.warning(self, "Database Error", "Failed to connect to the database.")

#     def toggle_password_visibility(self):
#         # Chuyển đổi trạng thái của trường mật khẩu
#         if self.password_visible:
#             self.lineEdit_login_password.setEchoMode(QtWidgets.QLineEdit.Password)
#             self.pushButton_show_hide.setText("show")
#         else:
#             self.lineEdit_login_password.setEchoMode(QtWidgets.QLineEdit.Normal)
#             self.pushButton_show_hide.setText("hide")
#         # Đảo ngược giá trị của cờ password_visible
#         self.password_visible = not self.password_visible

#     def open_registration_window(self):
#         self.registration_window = RegistrationWindow(self.db_connection)
#         self.registration_window.show()

# class RegistrationWindow(QtWidgets.QWidget):
#     def __init__(self, db_connection):
#         super().__init__()
#         # Tải file UI từ join_now.ui
#         uic.loadUi('auth_app/register.ui', self)
        
#         # Kết nối sự kiện
#         self.pushButton_agree_and_join.clicked.connect(self.register)

#         # Lưu kết nối đến cơ sở dữ liệu
#         self.db_connection = db_connection

#     def register(self):
#         email = self.lineEdit_new_email.text()
#         password = self.lineEdit_new_password.text()

#         if self.db_connection:
#             try:
#                 hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#                 cursor = self.db_connection.cursor()
#                 sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
#                 cursor.execute(sql, (email, hashed_password.decode('utf-8')))
#                 self.db_connection.commit()
#                 print("User registered successfully!")
#                 QMessageBox.information(self, "Thành Công", "Đăng ký thành công!")

#                 cursor.close()
#             except mysql.connector.Error as e:
#                 print(f"Error while inserting user: {e}")
#                 QMessageBox.warning(self, "Error", f"Registration failed: {e}")
#         else:
#             QMessageBox.warning(self, "Database Error", "Failed to connect to the database.")

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())



# login.py
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
import bcrypt
from main import MainWindow  # Import MainAppWindow từ main_app.py

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('auth_app/log_in.ui', self)
        
        self.pushButton_sign_in.clicked.connect(self.sign_in)
        self.pushButton_JoinNow.clicked.connect(self.open_registration_window)
        self.pushButton_show_hide.clicked.connect(self.toggle_password_visibility)
        self.password_visible = False
        self.db_connection = self.connect_to_db()

    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='123456789Mc@',
                database='user_db'
            )
            print("Connected to the database successfully!")
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def sign_in(self):
        email = self.lineEdit_login_email.text()
        password = self.lineEdit_login_password.text()

        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                sql = "SELECT password FROM users WHERE username = %s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()

                if result:
                    stored_password = result[0]
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        QMessageBox.information(self, "Thành Công", "Đăng nhập thành công!")
                        self.open_main_app()  # Mở giao diện chính khi đăng nhập thành công
                    else:
                        QMessageBox.warning(self, "Lỗi", "Mật khẩu không đúng.")
                else:
                    QMessageBox.warning(self, "Lỗi", "Tài khoản không tồn tại.")
                
                cursor.close()
            except mysql.connector.Error as e:
                print(f"Error during login: {e}")
                QMessageBox.warning(self, "Lỗi", f"Đăng nhập thất bại: {e}")
        else:
            QMessageBox.warning(self, "Database Error", "Failed to connect to the database.")

    def toggle_password_visibility(self):
        if self.password_visible:
            self.lineEdit_login_password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pushButton_show_hide.setText("show")
        else:
            self.lineEdit_login_password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pushButton_show_hide.setText("hide")
        self.password_visible = not self.password_visible

    def open_registration_window(self):
        self.registration_window = RegistrationWindow(self.db_connection)
        self.registration_window.show()

    def open_main_app(self):
        print("Opening main app window...")  # Thông báo khi chuẩn bị mở giao diện chính
        self.main_app_window = MainAppWindow()  # Mở cửa sổ giao diện chính từ main_app.py
        self.main_app_window.show()  # Hiển thị giao diện chính
    self.close() 


class RegistrationWindow(QtWidgets.QWidget):
    def __init__(self, db_connection):
        super().__init__()
        uic.loadUi('auth_app/register.ui', self)
        
        self.pushButton_agree_and_join.clicked.connect(self.register)
        self.db_connection = db_connection

    def register(self):
        email = self.lineEdit_new_email.text()
        password = self.lineEdit_new_password.text()

        if self.db_connection:
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                cursor = self.db_connection.cursor()
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (email, hashed_password.decode('utf-8')))
                self.db_connection.commit()
                QMessageBox.information(self, "Thành Công", "Đăng ký thành công!")

                cursor.close()
            except mysql.connector.Error as e:
                print(f"Error while inserting user: {e}")
                QMessageBox.warning(self, "Error", f"Registration failed: {e}")
        else:
            QMessageBox.warning(self, "Database Error", "Failed to connect to the database.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
