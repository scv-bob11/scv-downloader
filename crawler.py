import os
import re
import json
import urllib
import requests
from dotenv import dotenv_values

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ImmunefiCrawler:
    def __init__(self):
        self.immunefi_base_url = 'https://immunefi.com'
        self.make_param = lambda x: '&'.join([f'{k}={"%2C".join(v)}' for k,v in x.items()])
    

    def get_assets(self, url):
        r = requests.get(url)
        bs = BeautifulSoup(r.content, 'html.parser')

        assets_list = list()
        assets_in_scope = bs.find('h3', string='Assets in scope').parent
        assets_ul = assets_in_scope.find('ul')
        for li in assets_ul.children:
            if li.find(attrs={'title': 'smart_contract'}):
                assets_list.append(li.find('a').attrs['href'])
        return assets_list


    def get_all_count(self, filters={'programType': ['Smart Contract']}):
        params = self.make_param(filters)
        r = requests.get(f'{self.immunefi_base_url}/explore/?filter={urllib.parse.quote(params)}')
        bs = BeautifulSoup(r.content, 'html.parser')
        text = bs.find_all(lambda tag:tag.name=="div" and "Showing" in tag.text)[-1].text
        return int(re.search('\d+', text).group())


    def get_all(self, filters={'programType': ['Smart Contract']}):
        chr_options = webdriver.ChromeOptions()
        chr_options.add_argument('headless')
        chr_options.add_argument('window-size=1920x1080')
        chr_options.add_argument("disable-gpu")
        driver = webdriver.Chrome(dotenv_values('.env')['CHROME_DRIVER'], chrome_options=chr_options)

        params = self.make_param(filters)
        driver.get(f'{self.immunefi_base_url}/explore/?filter={urllib.parse.quote(params)}')

        bounties = list()
        while True:
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/section/div[3]/div/a')))
                driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section/div[3]/div/a').click()
            except:
                ul = driver.find_elements(By.TAG_NAME, 'ul')[1]
                for li in ul.find_elements(By.TAG_NAME, 'li'):
                    bounties.append(li.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                break
        driver.quit()

        return bounties



if __name__ == '__main__':
    ic = ImmunefiCrawler()
    print(ic.get_all_count())
    '''
    for x in ic.get_all():
        print(ic.get_assets(x))
    '''
        
