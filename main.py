from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request

app = Flask(__name__)


class HomePage(MethodView):
    def get(self):

        return render_template('homepage.html')


class CalculationPage(MethodView):
    def get(self):
        result = False
        calculation_form = CalculationForm()
        return render_template('calculation_page.html',
                               calculation=calculation_form, result=result)

    def post(self):
        calculation_form = CalculationForm(request.form)
        result = True

        required_calories = 100
        return render_template('calculation_page.html',
                               calculation=calculation_form, result=result,
                               calories=required_calories)

    def calculate(self, calculationform):
        pass


class CalculationForm(Form):
    weight = StringField('Weight: ', default='70')
    height = StringField('Height: ', default='175')
    age = StringField('Age: ', default='32')
    city = StringField('City: ', default='Washington')
    country = StringField('Country: ', default='USA')

    button = SubmitField("Calculate")


if __name__ == "__main__":
    app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
    app.add_url_rule('/calculation', view_func=CalculationPage.as_view('calculation_page'))

    app.run(debug=True)
