import random
import re
import time
import traceback
from urllib.parse import urlparse, urljoin
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class ArbitaryScrapper:

    def __init__(self, url):
        print("starting Arbitary Scrapper")
        self.url = url

        # HEADLESS OPTION
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1800, 900)
        self.driver.get(url)
        self.matching_links_set = set()
        self.emailAddresses = set()

    def get_all_matching_links(self):
        impressumLinks = self.get_links_with_keyword("impressum")
        kontaktLinks = self.get_links_with_keyword("kontakt")
        print("FIRST 4")
        for url in self.matching_links_set:
            print(url)
            self.driver.get(url)
            for address in self.get_email_addresses():
                self.emailAddresses.add(address)
                
        email_addresses = "{" + ", ".join('"' + email + '"' for email in self.emailAddresses) + "}"

        res = Result(self.url, "telNr", kontaktLinks[0], impressumLinks[0], email_addresses)
        return res


    def get_email_addresses(self):
        # Get the page source
        page_source = self.driver.page_source
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+(?:\(at\)|@)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        email_addresses = email_pattern.findall(page_source)
        return email_addresses


    def get_links_with_keyword(self, keyword, max_links=2):
        base_url = urlparse(self.driver.current_url).scheme + '://' + urlparse(self.driver.current_url).hostname

        all_links = self.driver.find_elements(By.TAG_NAME, 'a')
        matching_links = []

        for link in all_links:
            href = link.get_attribute('href')
            if href:
                full_url = urljoin(base_url, href)
                if base_url in full_url and keyword in full_url:
                    matching_links.append(full_url)

        # Add the first two matching links to the set
        # return instead self.matching_links_set.update(matching_links[:max_links])
        return matching_links[:max_links]

class Result:
    def __init__(self, url, tel_nr, kontakt_url, impressum_url, emailAddresses):
        # todo check for None Values


        self.url = url
        self.tel_nr = tel_nr
        self.kontakt_url = kontakt_url
        self.impressum_url = impressum_url
        self.emailAddresses = emailAddresses

    def to_csv(self):
        csv_format = f"{self.url},{self.tel_nr},{self.kontakt_url},{self.impressum_url},{self.emailAddresses}"
        return csv_format





