from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class CustomLabel(QLabel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""color:white;font-size:16px;""")

class UserCustomLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                border: 3px solid #E74C3C;
                border-radius:15px;
                color:white;
                background-color:#E74C3C;
                padding:7px;
                font-size:16px;
                text-align: center;
        """)

class ClientCustomLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignLeft)
        self.setStyleSheet("""
                border: 3px solid #D68910;
                border-radius:15px;
                color:white;
                background-color:#D68910;
                padding:7px;
                font-size:16px;
                text-align: center;
        """)

class CustomButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(
            """*{border: 3px solid #D35400;
            border-radius: 25px;
            width:50px;
            color : white;
            font-size : 20px;
            padding-left : 25px;
            padding-right : 25px;
            padding-top : 10px;
            padding-bottom : 10px;
            }
            *:hover{background:#D35400;color: black;}""")


class CustomEntry(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            color:white;
            border: 3px solid #D35400;
            border-radius:15px;
            font-size:16px;
            padding:5px;""")
