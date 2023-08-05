from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

def tuples(*args):
	data_tuple = []
	lists = []
	for x in range(0, len(args[0])):
		lists.append([item[x] for item in args])
	data_tuples = [tuple(list) for list in lists]
	return data_tuples

def toDataFrame(*args):
	columnNames = args[0:int(len(args) / 2)]
	dataList = args[int(len(args) / 2):len(args)]
	data_tuples = tuples(*dataList)
	return pd.DataFrame(data_tuples, columns=columnNames)


class scrape:
	def __init__(self, path, hidden):
		options = Options()
		options.headless=hidden
		options.add_experimental_option("excludeSwitches", ["enable-logging"])
		self.element = webdriver.Chrome(options=options, executable_path=path)
	def get(self, url):
		self.element.get(url)
	def find(self, by, selector):
		if by == ("css"):
			self.by = By.CSS_SELECTOR
		elif by == ("xpath"):
			self.by = By.XPATH
		elif by == ("id"):
			self.by = By.ID
		elif by == ("name"):
			self.by = By.NAME
		else:
			self.by = by
		if ("/") in selector:
			if len(selector.split("/")) == 2:
				self.selector = (selector.split("/")[0] + "[" + selector.split("/")[-1] + "]")
			elif len(selector.split("/")) == 3:
				self.selector = (selector.split("/")[0] + "[" + selector.split("/")[1] + "='" + selector.split("/")[-1] + "']")
		else:
			self.selector = selector
	def wait(self, by, selector):
		self.find(by, selector)
		WebDriverWait(self.element, 10).until(EC.presence_of_element_located((self.by, self.selector)))
	def _wait(self, by, selector):
		self.find(by, selector)
		return WebDriverWait(self.element, 10).until(EC.presence_of_all_elements_located((self.by, self.selector)))
	def get_wait(self, url, by, selector):
		self.get(url)
		self.wait(by, selector)
	def _get_wait(self, url, by, selector):
		self.get(url)
		return self._wait(by, selector)
	def text(self):
		return self.element.find_element(self.by, self.selector).text
	def _text(self):
		elements = self.element.find_elements(self.by, self.selector)
		return [element.text for element in elements]
	def find_text(self, by, selector):
		self.find(by, selector)
		return self.text()
	def _find_text(self, by, selector):
		self.find(by, selector)
		return self._text()
	def attr(self, attribute):
		return self.element.find_element(self.by, self.selector).get_attribute(attribute)
	def _attr(self, attribute):
		elements = self.element.find_elements(self.by, self.selector)
		return [element.get_attribute(attribute) for element in elements]
	def find_attr(self, by, selector, attribute):
		self.find(by, selector)
		return self.attr(attribute)
	def _find_attr(self, by, selector, attribute):
		self.find(by, selector)
		return self._attr(attribute)
	def find_click(self, by, selector):
		self.find(by, selector)
		self.element.find_element(self.by, self.selector).click()
	def url(self):
		return self.element.current_url
	def html(self):
		return self.element.page_source
	def close(self):
		self.element.close()
	def back(self):
		self.element.back()
	def driver(self):
		return self.element

	def GetData(self, keyword, limit="\n", add="", forb=0):
		html = self.element.page_source
		soup = BeautifulSoup(html, features="html.parser")
		text = "\n".join([line for line in soup.get_text().splitlines() if line != ("")])
		if len(text.split(keyword)) == 1:
			return ("")
		else:
			if forb == 0:
				return (text.split(keyword)[-1].split(limit)[0] + add).strip()
			else:
				return (text.split(keyword)[0].split(limit)[-1] + add).strip()

	def GetDataHtml(self, keyword, limit=" ", add="", forb=0):
		html = self.element.page_source
		if len(html.split(keyword)) == 1:
			return ("")
		else:
			if forb == 0:
				return (html.split(keyword)[-1].split(limit)[0] + add).strip()
			else:
				return (html.split(keyword)[0].split(limit)[-1] + add).strip()

	def enumCookie(self):
		try:
			assert ("accept all") not in self.element.page_source.lower()
			assert ("accept cookie") not in self.element.page_source.lower()
			assert ("allow all") not in self.element.page_source.lower()
			assert ("allow cookie") not in self.element.page_source.lower()
			assert ("i agree") not in self.element.page_source.lower()
			assert ("accept and close") not in self.element.page_source.lower()
			assert ("accept &amp; close") not in self.element.page_source.lower()
			assert ("accept & close") not in self.element.page_source.lower()
			# accept &amp; close ### selector = self.element.page_source.lower().split("accept &amp; close")[0].split("<")[-1].split(" ")[0]
			assert ("i accept") not in self.element.page_source.lower()
			assert ("got it") not in self.element.page_source.lower()
			assert ("accept") not in self.element.page_source.lower()
			return False
		except:
			if ("accept all") in self.element.page_source.lower():
				selector = self.element.page_source.lower().split("accept all")[0].split("<")[-1].split(" ")[0]
				text = ("accept all")
			elif ("accept cookie") in self.element.page_source.lower():
				text = ("accept cookie")
				selector = self.element.page_source.lower().split("accept cookie")[0].split("<")[-1].split(" ")[0]
			elif ("allow all") in self.element.page_source.lower():
				text = ("allow all")
				selector = self.element.page_source.lower().split("allow all")[0].split("<")[-1].split(" ")[0]
			elif ("allow cookie") in self.element.page_source.lower():
				text = ("allow cookie")
				selector = self.element.page_source.lower().split("allow cookie")[0].split("<")[-1].split(" ")[0]
			elif ("i agree") in self.element.page_source.lower():
				text = ("i agree")
				selector = self.element.page_source.lower().split("i agree")[0].split("<")[-1].split(" ")[0]
			elif ("accept and close") in self.element.page_source.lower():
				text = ("accept and close")
				selector = self.element.page_source.lower().split("accept and close")[0].split("<")[-1].split(" ")[0]
			elif ("accept &amp; close") in self.element.page_source.lower():
				text = ("accept & close")
				selector = self.element.page_source.lower().split("accept &amp; close")[0].split("<")[-1].split(" ")[0]
			elif ("accept & close") in self.element.page_source.lower():
				text = ("accept & close")
				selector = self.element.page_source.lower().split("accept &amp; close")[0].split("<")[-1].split(" ")[0]
			elif ("i accept") in self.element.page_source.lower():
				text = ("i accept")
				selector = self.element.page_source.lower().split("i accept")[0].split("<")[-1].split(" ")[0]
			elif ("got it") in self.element.page_source.lower():
				text = ("got it")
				selector = self.element.page_source.lower().split("got it")[0].split("<")[-1].split(" ")[0]
			elif ("accept") in self.element.page_source.lower():
				text = ("accept")
				selector = self.element.page_source.lower().split("accept")[0].split("<")[-1].split(" ")[0]
		cookies = [element for element in self.element.find_elements(By.TAG_NAME, selector) if text in element.text.lower()]
		for cookie in cookies:
			try:
				cookie.click()
				try:
					for x in range(0, 100):
						cookie.click()
				except:
					return True
			except:
				continue
		return False
