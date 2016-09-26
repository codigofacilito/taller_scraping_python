import urllib
import re

""" Primera forma """
def get_page(file_path):
	open_file = open(file_path, 'w')
	html_file = urllib.urlopen('http://econpy.pythonanywhere.com/ex/001.html')
	html_file = html_file.read()

	open_file.write( html_file )
	open_file.close()

def get_title(file_path):
	open_file = open(file_path, 'r')
	regex = '<div title="buyer-name">'
	regex_end = '</div>'
	for line in open_file.readlines():
		sentence = line.strip('\n')

		if regex in sentence:
			initial_pos = sentence.find(regex)
			initial_pos = initial_pos + len( regex )
			final_pos = sentence.find(regex_end)
			print sentence[initial_pos: final_pos]

""" Segunda forma """
def get_title_regex():
	html_file = urllib.urlopen('http://econpy.pythonanywhere.com/ex/001.html')
	html_file = html_file.read()

	regex = '<div title="buyer-name">(.+?)</div>'
	titles = re.findall( regex, html_file )
	for title in titles:
		print title

if __name__ == '__main__':
	file_path = 'econpy.html'
	get_page(file_path)
	get_title(file_path)
