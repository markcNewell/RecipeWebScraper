from website import Website





if __name__ == '__main__':
	#The data that will be stored in the database on how to retrieve the data from the webpage.
	#For http://www.mobkitchen.co.uk

	#Each part of the dictionary e.g. "title" has a list of places to search for the element incase the pages are not uniform

	#if contains then checks if text cotains that string.
	#otherwise if other attribute check if element has the attribute and value associated with it.
	mob_input_dict = {
		"title": [{"element": "h1", "class": "Blog-title Blog-title--item"}],
		"cooking_time": [{"element": "h3", "contains": "Cooking Time"},{"element": "h2", "contains": "Cooking Time"}],
		"feeds": [{"element": "h3", "contains": "Feeds"}],
		"ingredients": [{"element": "ul", "data-rte-list": "default"}],
		"method": [{"element": "ol", "data-rte-list": "default"}],
		"image": [{"element": "img", "contains": "static1.squarespace.com"}]
	}



	mob = Website("http://www.mobkitchen.co.uk/", mob_input_dict)
	mob.getRecipes()

