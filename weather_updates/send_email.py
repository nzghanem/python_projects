from get_data import WeatherData
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import make_msgid
import os
import re
import pathlib


class send_email():
    def __init__(self, receiver_email, msn_link, city):
        self.sender_email = "p.nezar.ghanem@gmail.com"
        self.password = "opwexbckxwitatyo"
        self.msn_link = msn_link
        self.dataCity = list(WeatherData(self.msn_link))
        self.receiver_email = receiver_email
        self.city = city
        self.sendto()

    def get_path(self, text):
        # to change directory to where your python files are located as when it runs auto it doesn't run from this directory
        os.chdir('/Users/nezaraboghanem/Documents/Programming/main_programming_languages/Python/projects_2022/weather_updates')
        conditions = 'conditions'  # name of the folder
        files = os.listdir(conditions)  # list of the items in the folder
        weather_condition = ""
        for condition in files:
            condition = condition.replace(".jpg", "")
            if re.search(f"({condition[0]}|{condition[0].upper()})({condition[1:]})", text):
                weather_condition = os.path.join(
                    pathlib.Path().absolute(),
                    conditions,
                    condition
                )
        return weather_condition + ".jpg"

    def looplis(self, index, starting):
        string = ""
        for i in range(len(self.dataCity[0][index])-starting):
            if re.search("[a-z]", self.dataCity[0][index][i+starting]):
                string += "\n" + self.dataCity[0][index][i+starting] + " - "
            else:
                string += f" {self.dataCity[0][index][i+starting]}"
        return string

    def ten_day_weather(self):
        string = self.looplis(0, 5) + self.looplis(1, 3)
        data = string.split("\n")
        data = list(filter(None, data))
        return data

    def get_realfeel(self):
        return self.dataCity[1].split("\n")[1]

    def create_string(self):
        data = self.ten_day_weather()
        string = ""
        for i in range(9):
            string += f"<img src='cid:{self.image_cid[i]}' width='50' height='50'/> {data[i]}" + "\n"
        return string

    def sendto(self):
        message = EmailMessage()
        message["To"] = self.receiver_email
        message["From"] = self.sender_email
        message["Subject"] = f"Today is {self.dataCity[0][0][2]} in {self.city}"
        special_id = make_msgid()[1:-1]
        self.image_cid = [make_msgid()[1:-1] for _ in range(9)]
        message.set_content(f"""
            <p>
                Morning Nezar,
            </p>

            <!-- Weather Today -->
            <p style='font-family:Cavolini;font-size:30px;white-space: pre-line'>
                <img src="cid:{special_id}" width="50" height="50"/> Today is {self.dataCity[0][0][2].lower()} in {self.city}
                <p style="font-size:20px;margin-left:100px"><strong>Feels like:</strong> {self.get_realfeel()}</p>
                <p style="font-size:20px;margin-left:100px"><strong>Today's High:</strong> {self.dataCity[0][0][1]}</p>
                <p style="font-size:20px;margin-left:100px"><strong>Today's Low:</strong> {self.dataCity[0][0][3]}</p>
            </p>
            <!-- Weather Next Ten Days -->

            <p style='font-family:Cavolini;font-size:30px'>
                Weather Next 10 Days
                    <p style='font-family:Cavolini;font-size:22px;white-space: pre-line;margin-left:100px'>
                        {self.create_string()}
                    </p>
            </p>

            <a href={self.msn_link}>Source</a>
            """, 'html')

        with open(self.get_path(self.dataCity[0][0][2]), 'rb') as fp:
            message.add_related(
                fp.read(), 'image', 'jpg', cid=f"<{special_id}>")
        self.dataCity[2].pop(0)

        for idx, imgtup in enumerate(self.dataCity[2]):
            with open(self.get_path(imgtup), "rb") as img:
                message.get_payload()[0].add_related(
                    img.read(),
                    maintype="image",
                    subtype="jpg",
                    cid=f"<{self.image_cid[idx]}>")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, self.receiver_email, message.as_string())


if __name__ == "__main__":
    send_email("nz.ghanem@gmail.com", "https://www.msn.com/en-us/weather/forecast/in-Brno,South-Moravia?loc=eyJsIjoiQnJubyIsInIiOiJTb3V0aCBNb3JhdmlhIiwicjIiOiJCcm5vIC0gbcSbc3RvIiwiYyI6IkN6ZWNoaWEiLCJpIjoiQ1oiLCJ0IjoxMDIsImciOiJlbi11cyIsIngiOiIxNi42MTMyIiwieSI6IjQ5LjE5MjEifQ%3D%3D&weadegreetype=C", "Brno")
