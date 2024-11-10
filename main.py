import sys
import requests
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout
from PyQt5.QtCore import Qt


class WheatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name :",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)

        self.tempreture_label = QLabel(self)
        self.emoji_label = QLabel(self)

        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App by Ashu")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.tempreture_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.tempreture_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.tempreture_label.setObjectName("tempreture_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family : calibri;

            }
            QLabel#city_label{
            font-size: 40px;
            font-style: italic;

            }
            QLineEdit#city_input{
                font-size:40px;
                  
         
            }
            QPushButton#get_weather_button{
                  font-size:30px;
                  font-weight:bold;
            }
            QLabel#tempreture_label{
        font-size:70px;
        }
        QLabel#emoji_label{
                           font-size: 100px;
                           font-family: Segeo UI emoji;}

        QLabel#description_label{
                       font-size:50px;    }



       """ )
        self.get_weather_button.clicked.connect(self.get_weather)
        
    def get_weather(self):
        api_key = "1974497dc4b19e3f24d9f8cf5951fd4b"
        city = self.city_input.text()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad requets\n check your input")
                case 401:
                    self.display_error("Unautorized\nInvalid api key")
                case 403:
                    self.display_error("Forbidden\n acess denied")
                case 404:
                    self.display_error("not found\n city not found")
                case 500:
                    self.display_error("Internal server error\n try again later")

                case 502:
                    self.display_error("Bad gateway\n invalid response from the server")

                case 503:
                    self.display_error("service unaviable\n server is down")

                case 504:
                    self.display_error("Gateway timeout\n no response")
                
                case _:
                    self.display_error(f"HTTPError occured\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("connection error\n check your connection")

        except requests.exceptions.Timeout:
            self.display_error("time out error \n request time out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("too many redirects\n check the url")
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"request error \n {req_error}")
               

               




    def display_error(self,message):

        self.tempreture_label.setStyleSheet("font-size : 30px;")
        self.tempreture_label.setText(message)

    def display_weather(self,data):
        self.tempreture_label.setStyleSheet("font-size : 50px;")
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        temp_f = (temp_k - 273.15)*(9/5)+32
        weather_id = data["weather"][0]["id"]
        weather_descr = data["weather"][0]["description"]
        self.emoji_label.clear()
        self.description_label.clear()



        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.tempreture_label.setText(f"{temp_c:.0f}°C \n {temp_f:.0f}°F")
        self.description_label.setText(weather_descr)

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "☁️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "🌋"
        
        elif weather_id == 800:
            return "☀️"
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wheather_app = WheatherApp()
    wheather_app.show()
    sys.exit(app.exec_())


