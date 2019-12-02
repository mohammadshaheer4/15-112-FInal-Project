import random
class player:
	def __init__(self,name,token,position,properties,money,houses,mortgaged properties, unmortgaged properties,allproperties):
		self.name=name
		self.token=token
		self.position=position
		self.properties=properties
		self.money=money
		self.houses=houses
		self.mortgaged properties=mortgaged properties
		self.unmortgaged properties=unmortgaged properties
		self.allproperties=allproperties

	def rollDie(self):
		a=random.randint(1,6)
		self.position+=a

	def buyProperty(self):
		self.money-=priceofproperty
		self.property[key]=propertydetails
		del self.allproperties[key]

	def payRent(self):
		if property not in self.properties and self.allproperties:
			self.money-=propertyrent



