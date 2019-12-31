class RecipeObj:
	def __init__(self, data):
		self.serialize(data)



	def serialize(self, data):
		if (len(data) != 7):
			raise Exception("Error serializing data array")
		else:
			self.title = data[0]
			self.cooking_time = data[1]
			self.feeds = data[2]
			self.ingredients = data[3]
			self.method = data[4]
			self.image = data[5]
			self.url = data[6]



	def exportJson(self):
		return {
			"title": self.title,
			"cooking_time": self.cooking_time,
			"feeds": self.feeds,
			"ingredients": self.ingredients,
			"method": self.method,
			"image": self.image,
			"url": self.url
		}



	def prettify(self):
		print("title:", self.title)
		print("cooking_time:", self.cooking_time)
		print("feeds:", self.feeds)
		print("ingredients:", self.ingredients)
		print("method:", self.method)
		print("image:", self.image)
		print("url:", self.url)
