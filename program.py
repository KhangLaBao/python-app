from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt.6 import gui
from PyQt6 import uic

class alert(QMessageBox):
    def error_message(self, title, message):
        self.setIcon(QMessageBox.icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

    def success_message(self, title, message):
        self.setIcon(QMessageBox.icon.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

msg = alert()

class login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)

        self.email_input = self.findChild(QLineEdit,"txt_email")
        self.password_input = self.findChild(QLineEdit,"txt_passport")
        self.btn_log_in = self.findChild(QLineEdit,"btn_log_in")
        self.btn_sign_up = self.findChild(QLineEdit,"btn_sign_up")
        self.btn_eye = self.findChild(QLineEdit,"btn_eye")
        
        self.btn_eyes.clicked.connect(lambda: self.show_password(self.btn_eye, self.password_input))
        self.btn_login.clicked.connect(self.login)
    
    def show_password(self,button: QPushButton, Input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QlineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/Eyes-solid.svg"))
        else:
           input.setEchoMode(QlineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eyes-slash-solid.svg")) 
           
    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "":
            msg.error_message("Login", "Email is required")
            self.email_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Login", "Password is required")
            self.password_input.setFocus()
            return
        
    with open("data/user.txt", "r") as file:
        for line in file:
            data = line.strip().split()(" , ")
            if data[0] == email and data [1] == password:
                msg.success_message("Login","Welcome to the system")
                return
            
        msg.error_message("login", "Invailed email or password")
       self.email_input.setFocus()
    
    def show_home









class Register(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register", self)

        self.email_input = self.findChild(QLineEdit,"txt_email")
        self.password_input = self.findChild(QLineEdit,"txt_passport")
        self.btn_log_in = self.findChild(QLineEdit,"btn_log_in")
        self.btn_sign_up = self.findChild(QLineEdit,"btn_sign_up")
        self.btn_eye = self.findChild(QLineEdit,"btn_eye")

             
        self.btn_eyes.clicked.connect(lambda: self.show_password(self.btn_eye_p, self.password_input))
        self.btn_login.clicked.connect(lambda: self.show_password(self.btn_eye_cp,confirm_pass_input))

 def show_password(self,button: QPushButton, Input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QlineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/Eyes-solid.svg"))
        else:
           input.setEchoMode(QlineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eyes-slash-solid.svg")) 
           
    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "":
            msg.error_message("Login", "Email is required")
            self.email_input.setFocus()
            return
        
          if name == "":
            msg.error_message("Login", "Nme is required")
            self.name_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Login", "Password is required")
            self.password_input.setFocus()
            return





  if confrom_pass == "":
            msg.error_message("Login", "Confrom Password is required")
            self.pconfrom_pass_input.setFocus()
            return

  if password != confrom_pass:
            msg.error_message("Login", "Password and Confrom password do not match")
            self.password_input.setFocus()
            return

        with open("data/user.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data [0] = email:
                    msg.error_message("Login","Email already exists")
                    selff.email_inpuit.setFocus()
                    return
                
        with open("data/user.txt", "a") as file:
            file.write(f"{email},{password}",{name}\n")
                       
        msg.success_message("Login", "Account created successfully")
            self.show_login       