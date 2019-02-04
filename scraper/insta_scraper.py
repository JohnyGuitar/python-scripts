#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import re
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import urllib.request
import urllib.parse
from selenium.webdriver.firefox.options import Options


class Instagram_Scraper:

	def __init__(self):

		self.account_counter = 0

		self.element_h1_xpath = '//*[@id="react-root"]/section/main/div/header/section/div/h1'
		self.element_span_xpath = '//*[@id="react-root"]/section/main/div/header/section/div/span'
		self.element_a_xpath = '//*[@id="react-root"]/section/main/div/header/section/div/a'

		self.user_info = {}

		self.br_text = '\n___________________________________________________\n\n'





	def get_info(self, url):

		self.account_counter = self.account_counter + 1
		print('Идёт сбор информации, пользователь номер', self.account_counter)

		driver = self.load_selenium(url)
		followers = self.load_bs4(url)

		user_info = {}

		user_info['\n****************Номер сессии: '] = self.account_counter, '**************************' + '\n'
		user_info["Ссылка на инсту "] = url
		user_info["\nКол-во подписчиков"] = followers
		user_info["\nИмя "] = driver.find_element_by_xpath(self.element_h1_xpath).text

		try:

			user_info['\nСсылки аккаунта '] = driver.find_element_by_xpath(self.element_a_xpath).text

		except NoSuchElementException:

			print('Информация о ссылках не найдена')
			user_info['\nСсылки аккаунта '] = 'Информация о ссылках не найдена'

		try:

			user_info["\nИнформация:\n"] = driver.find_element_by_xpath(self.element_span_xpath).text

		except NoSuchElementException:

			print('Информация о пользователе не найдена')
			user_info["\nИнформация: "] = 'Не найдено'

		driver.close()

		print(user_info)

		return user_info





	def load_selenium(self, url):

		try:

			options = Options()
			options.headless = True

			driver = webdriver.Firefox(options = options)
			driver.get(url)

		except urllib.error.HTTPError:
			print('Ошибка 404, Не найдено....')
			print('Продолжение работы....')

		except ConnectionResetError:
			print('Ошибка подключения....')
			print('Продолжение работы....')

		except ConnectionRefusedError:
			print('Прервано')
			driver.close()

		except UnboundLocalError:
			print('Прервано')
			driver.close()

		except NameError:
			print('Прервано')
			driver.close()

		except KeyboardInterrupt:
			print('Прервано')
			driver.close()

		return driver





	def load_bs4(self, url):

		try:

			#bs4 для парса кол-ва подписчиков
			html = urllib.request.urlopen(url).read()
			soup = BeautifulSoup(html, 'html.parser')

			data = soup.find_all('meta', attrs={'property': 'og:description'})
			text = data[0].get('content').split()

			followers = text[0]

			if 'k' in followers:

				followers = re.sub('k', '', followers)
				followers = float(followers) * 1000


		except urllib.error.HTTPError:
			print('Ошибка 404, Не найдено....')
			print('Продолжение работы....')

		except ConnectionResetError:
			print('Ошибка подключения....')
			print('Продолжение работы....')


		return followers





	def main(self):

        #читаем файл с ссылками на пользователя
		with open('user_for_scraper.txt') as inner_file:

			self.content = inner_file.readlines()
			self.content = [element.strip() for element in self.content]

		for url in self.content:

			with open('insta_info.txt', 'a', encoding='utf-8') as out_file:

				for value, key in self.get_info(url).items():
					out_file.write(('{}: {}').format(value, key))

				out_file.write(self.br_text)





if __name__ == '__main__':
	obj = Instagram_Scraper()
	obj.main()
