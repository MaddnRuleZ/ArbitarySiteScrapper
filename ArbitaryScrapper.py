import random
import re
import time
from urllib.parse import urlparse, urljoin
from selenium import webdriver
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


    # search for all mails on root and Kontakt / Impressum Site
    def get_all_matching_links(self):
        fbMails = self.handle_facebook_links()
        if fbMails is not None:
            return fbMails

        print("Obtaining Matching")
        kontaktUrl = ""
        impressumUrl = ""
        contactUrl = ""
        servicesUrl = ""
        impressumLinks = self.get_links_with_keyword("impressum")
        kontaktLinks = self.get_links_with_keyword("kontakt")
        contactUrl = self.get_links_with_keyword("contact")
        servicesUrl = self.get_links_with_keyword("services")
        combined_set = set(impressumLinks).union(kontaktLinks, contactUrl, servicesUrl)
        combined_set.add(self.url)

        for url in combined_set:
            print(url)
            self.driver.get(url)
            for address in self.get_email_addresses():
                self.emailAddresses.add(address)
            for address2 in self.get_email_addresses_in_href():
                self.emailAddresses.add(address2)
        email_addresses = ", ".join(email for email in self.emailAddresses)
        return email_addresses

    def handle_facebook_links(self):
        if not self.is_facebook_link(self.url):
            return None
        self.click_allow_all_cookies()
        self.wait_random_time()
        mail_addresses = self.get_email_addresses()
        final_addresses = ", ".join(email for email in self.emailAddresses)
        return final_addresses

    def chlick_on_fb_x(self):
        try:
            # Find the div by class names
            custom_div_element = self.driver.find_element(By.XPATH, "//i[contains(@class, 'x1b0d499') and contains(@class, 'x1d69dk1')]")


            # Click on the div
            custom_div_element.click()

            print("Clicked on the custom div element.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def click_allow_all_cookies(self):
        try:
            # Find the element by XPath
            allow_cookies_button = self.driver.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq') and contains(@class, 'x6ikm8r') and contains(@class, 'x10wlt62') and contains(@class, 'x1n2onr6') and contains(@class, 'xlyipyv') and contains(@class, 'xuxw1ft') and text()='Optionale Cookies ablehnen']")

            allow_cookies_button.click()
            print("Clicked on 'Alle Cookies erlauben' button.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def wait_random_time(self):
        random_time = random.uniform(1, 3)  # Generate a random float between 1 and 3
        time.sleep(random_time)

    def get_email_addresses(self):
        # Get the page source
        page_source = self.driver.page_source
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+(?:\(at\)|@)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        email_addresses = email_pattern.findall(page_source)
        return email_addresses

    def get_email_addresses_in_href(self):
        try:
            # Get the page source
            page_source = self.driver.page_source

            # Compile regex pattern for email addresses
            email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

            # Find all email addresses in href attributes
            href_emails = set()
            for match in re.finditer(r'href="(.*?)"', page_source):
                href = match.group(1)
                if href.startswith('mailto:'):
                    email = href.split(':')[1]
                    href_emails.add(email)
                else:
                    for email_match in email_pattern.finditer(href):
                        href_emails.add(email_match.group())

            return list(href_emails)
        except Exception as e:
            print(f"An error occurred: {e}")
            return []




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

    def is_facebook_link(self, link):
        try:
            parsed_url = urlparse(link)
            if parsed_url.netloc.endswith('facebook.com'):
                return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


class Result:
    def __init__(self, url,  kontakt_url, impressum_url, emailAddresses):
        # todo check for None Values
        self.url = url
        self.kontakt_url = kontakt_url
        self.impressum_url = impressum_url
        self.emailAddresses = emailAddresses

    def to_csv(self):
        csv_format = f"{self.url}, {self.emailAddresses}, {self.kontakt_url}, {self.impressum_url}"
        return csv_format
