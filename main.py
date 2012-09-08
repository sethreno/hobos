import cgi
import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.api import users
from google.appengine.ext import db

class Order(db.Model):
	name =db.StringProperty()
	ingredients = db.StringListProperty()

class OrderForm(webapp2.RequestHandler):
	def get(self):
		ingredients = (
			'Rice', 'Turkey', 'Peppers', 'Jalepenos', 'Potatoes', 'Corn', 'Cheese')
		vals = {'ingredients': ingredients}
		t = jinja_env.get_template('OrderForm.html')
		self.response.out.write(t.render(vals))

class OrderSave(webapp2.RequestHandler):
	def post(self):
		order = Order()
		order.name = self.request.get('name')
		order.ingredients = self.request.get_all('ingredients')
		order.put()
		self.redirect('/OrderThanks')

class OrderThanks(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>Thanks for your order</body></html>')

class ViewOpenOrders(webapp2.RequestHandler):
	def get(self):
		orders = db.GqlQuery("SELECT * FROM Order")
		for o in orders:
			self.response.out.write('<div>')
			self.response.out.write(cgi.escape(o.name) + ' : ' + ' '.join(o.ingredients))
			self.response.out.write('</div>')

app = webapp2.WSGIApplication([
		('/', OrderForm)
		,('/OrderSave', OrderSave)
		,('/OrderThanks', OrderThanks)
		,('/ViewOpenOrders', ViewOpenOrders)
	], debug=True)

