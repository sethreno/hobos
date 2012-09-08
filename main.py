import cgi
import webapp2

from google.appengine.api import users
from google.appengine.ext import db

class Order(db.Model):
	name =db.StringProperty()
	ingredients = db.StringListProperty()

class OrderForm(webapp2.RequestHandler):
	def get(self):

		ingredients = ('Rice', 'Turkey', 'Peppers', 'Jalepenos', 'Potatoes', 'Corn', 'Cheese')
		self.response.out.write("""<html><body>
		<form action="/OrderSave" method="post">
			<table><tr>
				<td>Order For</td>
				<td><input type="text" name="name" /></td>
			</tr>""")

		for i in ingredients:
			self.response.out.write('<tr><td>' + i + '</td>')
			self.response.out.write('<td><input type="checkbox" name="ingredients" value=' + i + '" /></td></tr>')

		self.response.out.write("""
			</table>
			<div><input type="submit" value="Order Hobo" /></div>
		</form>
		<br />past orders:
		""")

		self.response.out.write("""</body></html>""")

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

