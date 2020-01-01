from website import Website
import json



class Runner:
	def __init__(self, websitefile, outputdir):
		self.websites = self.openWebsiteFiles(websitefile)
		self.outputdir = outputdir




	def openWebsiteFiles(self, websitefile):

		with open(websitefile) as json_file:
		    data = json.load(json_file)

		return [self.serializeWebsite(website) for website in data]




	def serializeWebsite(self, website):
		return Website(website['homepage'], website['input_dict'], website['lastmod'])




	def run(self):
		#For each website get recipes
		for website in self.websites:
			recipes = website.getRecipes()
			website.exportJSON(recipes, self.outputdir)




if __name__ == '__main__':
	r = Runner("websites.json", "./data/")
	r.run()


