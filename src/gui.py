import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from .interface.components.app_tools import CustomLabel,UserCustomLabel, ClientCustomLabel, CustomButton, CustomEntry
from PyQt5.QtCore import QThread ,pyqtSignal
from .server_side.main_server import Server

class ConnectionStatus(QHBoxLayout):
    """
    Show the status of the connection.
    """
    def __init__(self,connect_function=None,is_server=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # Connection Label
        self.connection_label = CustomLabel("Connection :")
        self.addWidget(self.connection_label)

        # Connection Status Label (dynamic)
        self.connection_status_label = CustomLabel("Disconnect")
        self.connection_status_label.setStyleSheet("color:red;font-size:16px;")
        self.addWidget(self.connection_status_label)
        self.addStretch()

        # Connect Button
        if is_server:
            button_title = "Start Server"
        else:
            button_title = "Connect to Server"
        self.connect_button = CustomButton(button_title)
        self.connect_button.setStyleSheet( """*{border: 3px solid red;
            border-radius: 22px;
            color : white;
            font-size : 16px;
            font-weight:500;
            padding : 10px;}
            *:hover{background:red;color: #1C2833;}""")
        self.connect_button.clicked.connect(connect_function)
        self.addWidget(self.connect_button)

    def change_status(self):
        self.connection_status_label.setText("Connected")
        self.connection_status_label.setStyleSheet("color:green;font-size:16px;")

class Messages(QVBoxLayout):
    """
    This class handle the messages coming from server and client.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def receive_message(self, message) -> None:
        """
        Add a label widget for messages that come from client.
        """
        lbl = ClientCustomLabel(message)
        self.addWidget(lbl) 
        print(f"Received {message}")

    def send_message(self, message) -> None:
        """
        Add a label widget for messages that the user sending.
        """
        lbl = UserCustomLabel(message)
        self.addWidget(lbl)


class UserInteract(QHBoxLayout):
    """
    This class include 2 widget, an entry and a button to write message
    and send it.
    """

    def __init__(self, user_message=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_message_function = user_message
        # Entry
        self.message_entry = CustomEntry()
        # Button
        self.send_button = CustomButton("Send")
        self.send_button.clicked.connect(self.send_message)
        # Add Widgets to Layout
        self.addWidget(self.message_entry)
        self.addWidget(self.send_button)

    def send_message(self) -> None :
        """
        Pass the message that come from entry to a function from args.
        """
        self.user_message_function(self.message_entry.text())
        self.message_entry.setText("")



class WorkerThread(QThread):
    # This signal should defines in class level, otherwise it will not work!
    progress = pyqtSignal(str)

    def __init__(self,is_server=None):
        super().__init__()
        self.server = Server(is_server=is_server)

    def run(self) -> None:
        """
        Main method of QThread, call the server receive message
        method to collect messages and pass them into the signal(progress).
        """
        messages = self.server.server_receive_message()
        for message in messages:
            self.progress.emit(message)


    def send_message(self, message) -> None:
        """ Get message from gui and pass it to server to sending."""
        self.server.server_send_message(message)

class GuiAndServerConnection(QWidget):
    """
    Add all layouts in a Widget to make e nice ui.
    """
    def __init__(self, is_server:bool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_server = is_server
        # Add Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Add Connection Layout
        self.connection_layout = ConnectionStatus(connect_function=self.connect_to_server, is_server=is_server)
        self.main_layout.addLayout(self.connection_layout)

        # Add Message Layout to Main Layout
        self.messages_layout = Messages()
        self.main_layout.addLayout(self.messages_layout)

        # add Space between layouts
        self.main_layout.addStretch()

        # Add UserInteract Layout to Main Layout
        self.user_interact_layout = UserInteract(user_message=self.send_user_message)
        self.main_layout.addLayout(self.user_interact_layout)

    def connect_to_server(self) -> None:
        """
        Make server or connect to server and start receiving messages.
        """
        try:
            print("Connecting to server...")
            # Make a new thread to stablish a connection to server and interact with it.
            self.worker = WorkerThread(is_server=self.is_server) 
            # call the run() method from the class.
            self.worker.start()
            # listen to signal,foreach message come from server
            # signal will execute the get_client_message to show the message
            self.worker.progress.connect(self.get_client_message)
            # Change the status label on top of the app to CONNECTED.
            self.connection_layout.change_status()

        except Exception as err:
            print(err)



    def send_user_message(self, message) -> None:
        """
        Get user message and pass it to server to send it.
        """
        try:
            self.worker.send_message(message=message)
            self.messages_layout.send_message(message)

        except Exception as er:
            print(er)

    def get_client_message(self, message) -> None:
        """
        Get message from the signal and make a label by messages_layout
        for it show messages to user.
        """
        self.messages_layout.receive_message(message)


class MainWindow(QMainWindow):
    def __init__(self,title=None, is_server:bool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(550, 650)
        self.setWindowTitle(title)
        self.setStyleSheet("""
        background-color:#1C2833;
        """)

        self.setCentralWidget(GuiAndServerConnection(is_server=is_server))

