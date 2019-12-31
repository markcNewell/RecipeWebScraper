import re
from datetime import timedelta, datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from recipe import RecipeObj
import copy
import json
import requests




class Website:
	def __init__(self, homepage, input_dict):
		self.homepage = self.cleanUrl(homepage)
		self.urls = self.getAllUrls()
		self.input_dict = input_dict

		print(len(self.urls))






	###########################################COMMENT###############################################
	def getAllUrls(self):

		url = self.homepage + "/sitemap.xml"

		#Visual web browser
		#driver = webdriver.Firefox()
		#driver.get(url)
		#html = driver.page_source


		#Get web page using requests
		page = requests.get(url)
		html = page.content


		soup = BeautifulSoup(html, 'xml')
		#driver.quit()

		urls = soup.find_all("loc", text=re.compile("recipes/"))

		return [u.text for u in urls]


	def cleanUrl(self, url):
		return re.sub('\/$', '', url)


	def getNewUrls(self):
		newDate = datetime.now() - timedelta(days=365)

		driver = webdriver.Firefox()
		driver.get(self.homepage + "/sitemap.xml")
		soup = BeautifulSoup(driver.page_source, 'xml')
		driver.quit()

		urls = soup.find_all("lastmod", text=lambda t: self.compareDates(t, newDate.strftime("%Y-%m-%d")))	
		return [u.parent.findChildren("loc")[0].text for u in urls]


	def compareDates(self, first, second):
		first = first.split("-")
		second = second.split("-")

		if (int(first[0]) > int(second[0])):
			return True;
		elif (int(first[1]) > int(second[1])):
			return True;
		elif (int(first[2]) > int(second[2])):
			return True;
		else:
			return False;


	def clearText(self, text):
		return " ".join(text.split())


	def splitList(self, text):
		return re.split('\d. ', text)

	##################################################################################







	def getRecipes(self, overwrite=True):
		"""
		A method to get all the recipies of all the urls collected
		"""
		self.recipes = []
		exception_counter = 0



		#for url in self.urls:
		for u in range(1):
			url = self.urls[u]
			print(url)
			#try:
			self.recipes.append(self.getRecipe(url, self.input_dict))
			#except:
				#print(Exception)
				#exception_counter+=1



		print("Exception Counter:", exception_counter)

		if (len(self.recipes) > 0):
			self.exportJSON(self.recipes, overwrite)
		else:
			print("Nothing To Export")






	def exportJSON(self, recipes, overwrite):
		"""
		A method to export the list of recipes to a json file called the homepage
		Parameters:
			- recipes: A list of recipe objects to export
			- overwrite: A boolean to describe if an existing file can be overwritten or just appended to
		"""
		if (overwrite):
			param = 'w+'
		else:
			param = 'a+'

		recipes = [r.exportJson() for r in recipes]
		filename = self.homepage.split("//")[1]
		file = open(filename + '.json', param)
		file.write(json.dumps(recipes))







	def getRecipe(self, url, input_dict):
		"""
		A method to retrieve a recipe from the url using the input dictionary supplied
		Parameters:
			- url: a string url to search for a recipe.
			- input_dict: an object that details the way to locate the data on the page.
		Return:
			- an object with the same fields of the return_dict object with the recipe data.
		"""

		#Set up web browser and find web page visually
		driver = webdriver.Firefox()
		driver.get(url)
		html = driver.page_source

		#Get web page using requests
		#page = requests.get(url, headers=headers)
		#html = page.content

		soup = BeautifulSoup(html, 'lxml')
		driver.quit()
		data = []



		# kill all script and style elements
		for script in soup(["script", "style"]):
		    script.decompose()



		for key in input_dict:
			for place in range(len(input_dict[key])):
				element_type = input_dict[key][place]["element"]
				


				#Get the finder (last) part of the object.
				for part in input_dict[key][place]:
					finder = part



				#If the attribute is contains then search the text for it, if not check the attribute equals the value.
				if (finder == "contains"):
					#If the object is an image it won't have any text so searches the source of the image.
					if (element_type == "img"):
						element = soup.find_all(element_type, src=re.compile(input_dict[key][place][finder],re.I))
					else:
						element = soup.find_all(element_type, text=re.compile(input_dict[key][place][finder],re.I))
				else:
					element = soup.find_all(element_type, attrs={finder:input_dict[key][place][finder]})



				#If no elements are found end this loop and retry with the next possible location
				print(len(element))
				if (len(element) > 0):
					element = element[0]
				else:
					if (place == (len(input_dict[key])-1)):
						raise Exception("Error retrieving " + key + " for " + url)
					else:
						continue;



				#If the key is ingredients or method (which should both be lists), convert them to lists.
				if (key == "ingredients") | (key == "method"):
					if (element_type == "ul") | (element_type == "ol"):
						text = [self.clearText(item.text) for item in element.find_all("li")]
					else:
						text = self.splitList(self.clearText(element.text))
				elif (key == "feeds") | (key == "cooking_time"):
					text = [int(s) for s in element.text.split() if s.isdigit()][0]
				elif (key == "image"):
					text = element['src']
				else:
					text = self.clearText(element.text)

				data.append(text)



				#Break so if text is found and added no more is searched for in that place.
				break;



		#Add other information such as url
		data.append(url)

		return RecipeObj(data)

