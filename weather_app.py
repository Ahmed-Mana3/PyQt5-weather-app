import sys
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("weather-icon.ico"))
        
        self.title = QLabel("Enter city name:", self)
        
        self.input_box = QLineEdit(self)
        
        self.submit_button = QPushButton("Show Weather", self)
        
        self.result_box = QLabel(self)
        self.imoji_box = QLabel(self)
        self.description_box = QLabel(self)

        self.initUI()
    
    def initUI(self):
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.input_box)
        vbox.addWidget(self.submit_button)
        vbox.addWidget(self.result_box)
        vbox.addWidget(self.imoji_box)
        vbox.addWidget(self.description_box)
        
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        
        self.title.setAlignment(Qt.AlignCenter)
        self.input_box.setAlignment(Qt.AlignCenter)
        self.result_box.setAlignment(Qt.AlignCenter)
        self.imoji_box.setAlignment(Qt.AlignCenter)
        self.description_box.setAlignment(Qt.AlignCenter)

        
        self.title.setObjectName("title")
        self.result_box.setObjectName("result_box")
        self.imoji_box.setObjectName("imoji_box")
        self.description_box.setObjectName("description_box")

        
        self.setStyleSheet("""
                           QLabel {
                               font-size: 30px;
                               font-family: Arial;
                           }
                           QLineEdit {
                               padding: 5px;
                               font-size: 25px;
                               width: 300px;
                           }
                           QPushButton {
                               font-size: 20px;
                               font-weight: bold;
                               padding: 15px;
                           }
                           #title{
                               margin-bottom: 10px;
                               font-style: italic;
                           }
                           #imoji_box{
                               font-size: 80px;
                               font-family: segoe UI emoji;
                           }
                           #result_box{
                               font-size: 50px;
                               margin-top: 10px;
                           }
                           #description_box {
                               margin-bottom: 10px;
                           }
                           
                           """)
        
        self.submit_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        api_key = "422d69c13b098cf4613ebba7c43e955e"
        city_name = self.input_box.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("bad request:\nplease check your input")
                case 401:
                    self.display_error("Unauthorized:\ninvalid API key")
                case 403:
                    self.display_error("Forbidden:\naccess is denied")
                case 404:
                    self.display_error("not found:\ncity not found")
                case 500:
                    self.display_error("internal server error:\ntry again later")
                case 502:
                    self.display_error("bad gateway:\ninvalid response from the server")
                case 503:
                    self.display_error("service unavailable:\nserver is down")
                case 504:
                    self.display_error("gateway timeout:\n no response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("connection error\ncheck you internet connection")

        except requests.exceptions.Timeout:
            self.display_error("timeout error\nthe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("too many redirects\ncheck the url")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"request error {req_error}")
        
    def display_error(self, message):
        self.result_box.setStyleSheet("font-size: 25px; color: red;")
        self.result_box.setText(message)
        self.input_box.clear()
        self.imoji_box.clear()
        self.description_box.clear()
    
    def display_weather(self, data):
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        self.result_box.setStyleSheet("font-size: 40px; color: #000000; font-weight: 500;")
        self.result_box.setText(f"{temp_c:.0f}°C")
        emoji_id = data["weather"][0]["id"]
        self.imoji_box.setText(self.get_emoji(emoji_id))
        temp_emoji = data['weather'][0]['description']
        self.description_box.setText(f"{temp_emoji}")

    @staticmethod
    def get_emoji(emoji_id):
        if 200 <=  emoji_id <= 232:
            return "⛈️️"
        elif 300 <= emoji_id <= 321:
            return "🌦️"
        elif  500 <= emoji_id <= 531:
            return "🌧️"
        elif  600 <= emoji_id <= 622:
            return "❄️"
        elif  701 <= emoji_id <= 741:
            return "🌫️"
        elif  emoji_id == 762:
            return "🌋"
        elif  emoji_id == 771:
            return "💨"
        elif emoji_id == 781:
            return "🌪️"
        elif emoji_id == 800:
            return "☀️"
        elif 801 <= emoji_id <= 804:
            return "🌥️"
        else:
            return " "
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



