from website import Website
import json



class Runner:
	def __init__(self, websitefile, outputdir):
		self.websitefile = websitefile
		self.websites = self.openWebsiteFiles(websitefile)
		self.outputdir = outputdir




	def openWebsiteFiles(self, websitefile):

		with open(websitefile) as json_file:
		    data = json.load(json_file)

		return [self.serializeWebsite(website) for website in data]




	def serializeWebsite(self, website):
		if ("sitemap" in website.keys()):
			return Website(website['homepage'], website['input_dict'], website['lastmod'], sitemap=website['sitemap'])
		else:
			return Website(website['homepage'], website['input_dict'], website['lastmod'])





	def updateJSON(self):
		with open(self.websitefile, "w") as file:
		    file.write(json.dumps([website.exportWebsite() for website in self.websites]))




	def run(self):
		#For each website get recipes
		for website in self.websites:
			recipes = website.getRecipes()
			website.exportJSON(recipes, self.outputdir)

		self.updateJSON()




if __name__ == '__main__':
	r = Runner("websites.json", "./data/")
	r.run()


