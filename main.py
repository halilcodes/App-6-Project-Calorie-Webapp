import requests
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
import keys
from bs4 import BeautifulSoup

app = Flask(__name__)


class HomePage(MethodView):
    def get(self):

        return render_template('homepage.html')


class CalculationForm(Form):
    weight = StringField('Weight: ', default='70')
    height = StringField('Height: ', default='175')
    age = StringField('Age: ', default='32')
    city = StringField('City: ', default='Washington')
    country = StringField('Country: ', default='USA')

    button = SubmitField("Calculate")


class CalculationPage(MethodView):
    def __init__(self):
        self.form = None

    def get(self):
        result = False
        calculation_form = CalculationForm()
        return render_template('calculation_page.html',
                               calculation=calculation_form, result=result)

    def post(self):
        self.form = CalculationForm(request.form)
        result = True
        temperature = Temperature(self.form.country.data, self.form.city.data)

        temperature = temperature.timeanddate_temp()
        weight = float(self.form.weight.data)
        height = float(self.form.height.data)
        age = int(self.form.age.data)
        calorie = Calorie(weight, height, age, temperature)

        required_calories = calorie.calculate()
        return render_template('calculation_page.html',
                               calculation=self.form, result=result,
                               calories=required_calories)


class Temperature:
    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    def __init__(self, country, city):
        self.country = country.replace(" ", "-")
        self.city = city.replace(" ", "-")

    def openweather_temp(self):
        """ This method gets the temperature data using openweathermap.com API """

        url = "https://api.openweathermap.org/data/2.5/weather"
        api_key = keys.openweathermap_api
        city = self.city
        params = {
            "q": city,
            "appid": api_key
        }
        response = requests.get(url=url, params=params, headers=self.headers)

        data = response.json()
        temperature = round(data['main']['temp'] / 10, 2)
        return temperature

    def timeanddate_temp(self):
        """ This method gets the temperature data by scraping fom timeanddate.com/weather"""
        url = f"https://www.timeanddate.com/weather/{self.country}/{self.city}"
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        temp_str = soup.find(id='qlook').find(class_='h2').text
        temperature = temp_str.split()[0]

        return int(temperature)


class Calorie:
    def __init__(self, weight, height, age, temperature):
        self.weight = weight
        self.height = height
        self.age = age
        self.temperature = temperature

    def calculate(self):
        result = 10 * self.weight + 6.5 * self.height + 5 - self.temperature - 10
        return result


if __name__ == "__main__":
    app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
    app.add_url_rule('/calculation', view_func=CalculationPage.as_view('calculation_page'))

    app.run(debug=True)
