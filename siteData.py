from typing import Optional

from thompcoutils.log_utils import get_logger


class SiteData:
    """
    Class to hold site data.
    """
    def __init__(self, account: int, owner: str, mailing_address: str, site_address: str, notes=''):
        """
        Initialize the SiteData object.
        param account: The account number.
        param owner: The owner name.
        param mailing_address: The mailing address.
        param site_address: The site address of the property.
        param notes: The notes for the property.  Note that this is only available from the spreadsheet
        """
        self.account = account
        self.owner = owner
        self.mailing_address = mailing_address
        self.site_address = site_address
        self.notes = notes

    def __str__(self):
        """
        Return a string representation of the SiteData object.
        return: A string representation of the SiteData object.
        """
        rtn = 'Account:{};Owner:{};Mailing Address:{};Site Address:{}'.format(self.account,\
                                                                              self.owner,
                                                                              self.mailing_address,
                                                                              self.site_address)
        if self.notes:
            rtn += ';Notes:{}'.format(self.notes)
        return rtn

    def differences(self, other: Optional["SiteData"], first_name='first', second_name='second'):
        """
        Return a string that represents the differences between the two SiteData objects.
        param other: The other SiteData object.
        param first_name: The name of the first object (for display).
        param second_name: The name of the second object (for display).
        return: True/False if the differences are not empty strings and a string that represents the differences between the two SiteData objects.
        """
        logger = get_logger()
        dif_string = ''
        substantial_differences = False
        if self.account == other.account:
            if self.site_address != other.site_address:
                if self.site_address and other.site_address:
                    substantial_differences = True
                message = 'Site Addresses are different:\n{}:{}\n{}:{}'.format(first_name,
                                                                               self.site_address,
                                                                               second_name,
                                                                               other.site_address)
                logger.debug(message)
                dif_string += message + "\n"
            if self.mailing_address != other.mailing_address:
                if self.mailing_address and other.mailing_address:
                    substantial_differences = True
                message = 'Mailing Addresses are different:\n{}:{}\n{}:{}'.format(first_name,
                                                                                  self.mailing_address,
                                                                                  second_name,
                                                                                  other.mailing_address)
                logger.debug(message)
                dif_string += message + "\n"
            if self.owner != other.owner:
                if self.owner and other.owner:
                    substantial_differences = True
                message = 'Owners are different:\n{}:{}\n{}:{}'.format(first_name,
                                                                       self.owner,
                                                                       second_name,
                                                                       other.owner)
                logger.debug(message)
                dif_string += message + "\n"
            if dif_string != '':
                notes = self.notes if self.notes else other.notes
                dif_string = 'Site Data Differences for account {} ({}):\n'.format(self.account, notes) + dif_string
        return substantial_differences, dif_string
