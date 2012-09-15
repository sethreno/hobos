import cgi
import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.api import users
from google.appengine.ext import db

ingredients = (
	'Rice', 'Turkey', 'Peppers', 'Jalepenos', 'Potatoes', 'Corn', 'Cheese')
statuses = (
	'queued', 'preparing', 'cooking', 'ready', 'served')

class Order(db.Model):
	name =db.StringProperty()
	ingredients = db.StringListProperty()
	status = db.StringProperty()

class OrderForm(webapp2.RequestHandler):
	def get(self):
		vals = {'ingredients': ingredients}
		t = jinja_env.get_template('OrderForm.html')
		self.response.out.write(t.render(vals))

class OrderSave(webapp2.RequestHandler):
	def post(self):
		order = Order()
		order.name = self.request.get('name')
		order.ingredients = self.request.get_all('ingredients')
		order.status = "queued"
		order.put()
		self.redirect('/OrderThanks?key=' + str(order.key()))

class OrderThanks(webapp2.RequestHandler):
	def get(self):
		o = db.get(self.request.get('key'))
		vals = {'o': o}
		t = jinja_env.get_template('OrderThanks.html')
		self.response.out.write(t.render(vals))

class ViewOpenOrders(webapp2.RequestHandler):
	def get(self):
		orders = db.GqlQuery("SELECT * FROM Order WHERE status != 'served'")
		vals = {'orders': orders, 'statuses': statuses}
		t = jinja_env.get_template('ActiveOrderList.html')
		self.response.out.write(t.render(vals))

	def post(self):
		keys = self.request.get_all('key')
		status = self.request.get_all('status')
		for i in range(len(keys)):
			o = db.get(keys[i])
			o.status = status[i]
			o.put()

		self.redirect('/ViewOpenOrders')

app = webapp2.WSGIApplication([
		('/', OrderForm)
		,('/OrderSave', OrderSave)
		,('/OrderThanks', OrderThanks)
		,('/ViewOpenOrders', ViewOpenOrders)
		,('/ViewOpenOrders/Update', ViewOpenOrders)
	], debug=True)

