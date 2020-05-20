# RecipeWebScraper
This project contains a web scraper to scrape data from any recipe websites (using standard formatting) and to collate these gathered recipies into a json storage which could be inserted into a database.

## Running ##
To start create a `/data/websites.json` file which contains an array of website strings which point to the sitemaps of the respective websites e.g. `["https://www.bbcgoodfood.com/sitemap"]`\n
Then by running `python main.py` it should collate the recipies found.

## Work In Progress ##
The front end folder is a work in progress front end to simplify the ading of recipie sitemaps.
