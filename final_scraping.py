from bs4 import BeautifulSoup
import requests
import threading

from pymongo import MongoClient

GOOGLE_NEWS_URL = 'https://news.google.com.mx/'
CUSTOME_TARGET = 'www.eluniversal.com'

def get_beautiful_soup(href):
	re = requests.get( href )
	if re.status_code == 200:
		return BeautifulSoup( re.text, 'html.parser')

def set_robot(article, database):
	title = article.find('span', {'class': 'titletext'} ).getText()
	href = article.find('a').get('href')

	if CUSTOME_TARGET in href:
		soup = get_beautiful_soup(href)
		if soup is not None:
			container = soup.find('div', {'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
			paragraphs = container.find_all('p')

			final_article = ''
			for paragraph in paragraphs:
				final_article = '{} {}'.format(final_article, paragraph)
			
			json = { 'title' : title, 'href': href, 'article': final_article }
			database.articles.insert_one( json )
			print "Nuevo articulo en la base de datos!"
			
def scraping_site():
	soup = get_beautiful_soup(GOOGLE_NEWS_URL)
	
	if soup is not None:
		client = MongoClient('localhost', 27017)
		database = client.codigo_facilito

		articles = soup.find_all('h2', {'class' : 'esc-lead-article-title'})
		for article in articles:
			robot = threading.Thread(	name='set_robot',
																target=set_robot, 
																args = (article, database) )
			robot.start()

if __name__ == '__main__':
	scraping_site()