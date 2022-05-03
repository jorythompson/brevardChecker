from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from thompcoutils.config_utils import ConfigManager
from bs4 import BeautifulSoup
from os.path import exists
from chromedriver import get_driver
import os
import time
from thompcoutils.log_utils import get_logger
from siteData import SiteData


class SoupHandler:
    """
    This class is used to scrape the Brevard County website for data.  It can get it from the site or from a file with
    the saved data
    """
    URL = 'https://www.bcpao.us/propertysearch/#/account/{}'

    def __init__(self, config_mgr: ConfigManager):
        """
        Initialize the class
        param config_mgr: ConfigManager that holds the configuration from the config file
        """
        self.config_mgr = config_mgr
        self.values = None

    def download_soup(self, url: str):
        """
        Download soup from url
        param url: url to download (including account number)
        return: the beautiful soup object
        """
        logger = get_logger()
        logger.debug("Downloading soup from url: {}".format(url))
        d = get_driver()
        d.get('https://www.google.com')
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(self.config_mgr.page_delay)
        page = driver.page_source
        driver.quit()
        return BeautifulSoup(page, 'html.parser')

    def get_soup(self, account_number: int):
        """
        Return soup for account number
        Base url is: https://www.bcpao.us/propertysearch/#/account/2609299
        param account_number: account number to look up
        """
        logger = get_logger()
        url = SoupHandler.URL.format(account_number)
        if not exists(self.config_mgr.debug_folder):
            os.mkdir(self.config_mgr.debug_folder)
        debug_file = os.path.join(self.config_mgr.debug_folder,
                                  str(account_number) + "." + self.config_mgr.json_extension)
        if self.config_mgr.debug:
            if exists(debug_file):
                logger.debug("Getting soup for account number: {} from file {}".format(account_number, debug_file))
                with open(debug_file, 'r') as f:
                    beautiful_soup = BeautifulSoup(f.read(), 'html.parser')
            else:
                logger.debug("Getting soup for account number: {} URL {} and saving it to {}".format(
                    account_number, url, debug_file))
                beautiful_soup = self.download_soup(url)
                with open(debug_file, 'w', encoding="utf-8") as f:
                    f.write(beautiful_soup.prettify())
        else:
            logger.debug("Getting soup for account number: {} URL {}".format(account_number, url))
            beautiful_soup = self.download_soup(url)
        return beautiful_soup

    @staticmethod
    def get_site_data(beautiful_soup: BeautifulSoup, account_number: int):
        """
        Get the SiteData from the beautiful soup object
        param beautiful_soup: beautiful soup object
        param account_number: account number (used for error reporting)
        return: SiteData object representing the data from the beautiful soup object
        """
        logger = get_logger()
        account_entry = beautiful_soup.find_all("div", {"id": "divPropertySearch_Details_Account"})
        if len(account_entry) == 0:
            message = 'Account number "{}" not found on web site'.format(account_number)
            logger.error(message)
            raise Exception(message)
        account_str = account_entry[0].text.rstrip().lstrip()
        account = int("".join(filter(str.isdigit, account_str)))
        owner = beautiful_soup.find('div', {'data-bind': "text: publicOwners"}).text.rstrip().lstrip()
        mailing_address = beautiful_soup.find('div',
                                              {'data-bind': "text: mailingAddress.formatted"}).text.rstrip().lstrip()
        site_address = beautiful_soup.find('div', {'data-bind': "text: siteAddressFormatted"}).text.rstrip().lstrip()
        site_data = SiteData(account=account, owner=owner, mailing_address=mailing_address, site_address=site_address)
        logger.debug('got account information from soup:{}'.format(str(site_data)))
        return site_data

    def get_accounts(self, accounts: list[SiteData]):
        """
        Get the account information for the list of account numbers from the soup
        param accounts: list of SiteData accounts
        return: list of SiteData accounts
        """
        if self.values is None:
            self.values = []
            for account in accounts:
                soup = self.get_soup(account_number=account.account)
                updated_account = self.get_site_data(soup, account.account)
                self.values.append(updated_account)
        return self.values
