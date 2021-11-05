
from flask import Flask, render_template, flash, redirect
from config import Config
from forms import LoginForm
from evm_compatible_api import get_chartdata
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)

portfolio_value = []

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('ADDRESS: {}, CHAIN ID={}'.format(form.address.data, form.chain.data))
		try:
			(portfolio_value,times) = get_chartdata(form.address.data, form.chain.data)
		except:
			return render_template('login.html', title='Sign In', form=form)
		return render_template("index.html", weeklyValues=portfolio_value, weeklyTimes=times, form=form)
	return render_template('login.html', title='Sign In', form=form)

if __name__ == "__main__":
	app.run()