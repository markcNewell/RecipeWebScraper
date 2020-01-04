import re
import os
import json
import requests
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from recipe import RecipeObj





class Website:
	def __init__(self, homepage, input_dict, last_mod, sitemap=None):		
		self.sitemap = sitemap
		self.homepage = self.cleanUrl(homepage)
		self.urls = self.getNewUrls(last_mod)
		self.input_dict = input_dict

		print(len(self.urls))







	#Small utility methods
	def cleanUrl(self, url):
		return re.sub('\/$', '', url)


	def clearText(self, text):
		return " ".join(text.split())


	def splitList(self, text, splitter):
		if (splitter == "line"):
			sp = "\n"
		elif (splitter == "number"):
			sp = "\d. "
		else:
			sp = "\n"

		return re.split(sp, text)


	def cleanLastMod(self, date):
		return date[:10]








	def getNewUrls(self, last_mod):
		"""
		A method to get all the urls since the last modification time of the website data held.
		Parameters:
			- last_mod: a string in the form "2018-12-30" (year-month-date)
		Returns:
			- The list of urls that have been modified since the last check
		"""
		allurls = []

		if (self.sitemap == None):
			sitemapurls = [self.homepage + "/sitemap.xml"]
		else:
			sitemapurls = self.sitemap



		for url in sitemapurls:
			print(url)


			#Get web page using requests
			page = requests.get(url)
			html = page.content
			code = page.status_code


			if (code != 200):
				#Set up web browser and find web page visually
				driver = webdriver.Firefox()
				driver.get(url)
				html = driver.page_source
				driver.quit()


			soup = BeautifulSoup(html, 'xml')


			#Find all the dates which are after the last modification date
			times = soup.find_all("lastmod", text=lambda t: self.compareDates(self.cleanLastMod(t), last_mod))


			if (len(times) > 0):
				#For each time
				for u in times:
					#Find the url associated
					url = u.parent.findChildren("loc")[0].text


					#If the url is a recipe then add it
					if (re.search("recipes/",url)):
						allurls.append(url)

			else:
				urls = soup.find_all("loc", text=re.compile("recipes/"))


				for u in urls:
					allurls.append(url)



		return allurls







	def compareDates(self, first, second):
		"""
		A method to compare two dates as strings in the form year-month-date.
		Parameters:
			- first: The first date to compare.
			- second: The second date to compare.
		Returns:
			- boolean if first is after second date
		"""
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








	def getRecipes(self):
		"""
		A method to get all the recipies of all the urls collected
		"""
		self.recipes = []
		exception_counter = 0



		#for url in self.urls:
		for u in range(1):#len(self.urls)):
			url = self.urls[u]
			print(url)

			#Remove try to see exceptions
			try:
				self.recipes.append(self.getRecipe(url, self.input_dict))
			except:
				exception_counter+=1


		print("Exception Counter:", exception_counter)
		return self.recipes






	def exportWebsite(self):
		return {
			"homepage": self.homepage,
			"input_dict": self.input_dict,
			"lastmod": datetime.now().strftime("%Y-%m-%d")
		}







	def exportJSON(self, recipes, outputdir):
		"""
		A method to export the list of recipes to a json file called the homepage
		Parameters:
			- recipes: A list of recipe objects to export
			- overwrite: A boolean to describe if an existing file can be overwritten or just appended to
		"""
		if (len(self.recipes) > 0):
			filename = self.homepage.split("//")[1]
			filepath = outputdir + filename + '.json'

			old_recipes = self.removeOldVersions(recipes, filepath)

			new_recipes = [r.exportJson() for r in recipes]
			
			file = open(filepath, 'w')
			file.write(json.dumps(old_recipes+new_recipes))
		else:
			print("Nothing To Export")







	def removeOldVersions(self, recipes, filepath):
		"""
		A method to check through the old recipes to remove duplicates.
		Parameters:
			- recipes: an array of Recipe objects to check for.
			- filepath: the path to the file holding the data.
		Returns:
			- a list of recipes from the file and from the website without duplicates
		"""
		oldcounter = 0

		if (os.path.exists(filepath)):			


			#Open the file
			with open(filepath, "r+") as file:
				data = json.load(file)


			#For each object in the file check against the new recipe objects
			for x in range(len(data)):
				url_data = data[x]['url']


				for y in range(len(recipes)):
					url_recipe = recipes[y].url


					#If the same urls then delete the object from the data array
					if (url_data == url_recipe):
						del data[x]
						oldcounter+=1

		else:
			data = []


		print("Updated Counter:", oldcounter)
		return data











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

				if (element_type != "none"):					


					#Get the finder (last) part of the object.
					p=0
					for part in input_dict[key][place]:
						if (p == 1):
							finder = part
						p+=1



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
					if (len(element) > 0):
						element = element[0]
					else:
						if (place == (len(input_dict[key])-1)):
							raise Exception("Error retrieving " + key + " for " + url)
						else:
							continue;



					#If the key is ingredients or method (which should both be lists), convert them to lists.
					if (key == "ingredients") | (key == "method"):
						if (element_type == "ul") | (element_type == "ol") | (input_dict[key][place]["splitter"] == "list"):
							text = [self.clearText(item.text) for item in element.find_all("li")]
						else:
							text = self.splitList(element.text, input_dict[key][place]["splitter"])
					elif (key == "feeds") | (key == "cooking_time"):
						text = [int(s) for s in element.text.split() if s.isdigit()][0]
					elif (key == "image"):
						text = element['src']
					else:
						text = self.clearText(element.text)


				else:
					text = "N/A"



				data.append(text)


				#Break so if text is found and added no more is searched for in that place.
				break;



		#Add other information such as url
		data.append(url)

		return RecipeObj(data)

