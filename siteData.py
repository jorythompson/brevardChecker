from typing import Optional

from thompcoutils.log_utils import get_logger


class SiteData:
    """
    Class to hold site data.
    """
    def __init__(self, account: int, owner: str, mailing_address: str, site_address: str):
        """
        Initialize the SiteData object.
        param account: The account number.
        param owner: The owner name.
        param mailing_address: The mailing address.
        param site_address: The site address of the property.
        """
        self.account = account
        self.owner = owner
        self.mailing_address = mailing_address
        self.site_address = site_address

    def __str__(self):
        """
        Return a string representation of the SiteData object.
        return: A string representation of the SiteData object.
        """
        return 'Account:{};Owner:{};Mailing Address:{};Site Address:{}'.format(self.account,
                                                                               self.owner,
                                                                               self.mailing_address,
                                                                               self.site_address)

    def differences(self, other: Optional["SiteData"], first_name='first', second_name='second'):
        """
        Return a string that represents the differences between the two SiteData objects.
        param other: The other SiteData object.
        param first_name: The name of the first object (for display).
        param second_name: The name of the second object (for display).
        return: A string that represents the differences between the two SiteData objects.
        """
        logger = get_logger()
        rtn = ''
        if self.account == other.account:
            if self.site_address != other.site_address and \
                    self.site_address != '' and self.site_address is not None and \
                    other.site_address != '' and other.site_address is not None:
                message = 'Site Addresses are different:\n{}:{}\n{}:{}'.format(first_name,
                                                                               self.site_address,
                                                                               second_name,
                                                                               other.site_address)
                logger.debug(message)
                rtn += message + "\n"
            if self.mailing_address != other.mailing_address and \
                    self.mailing_address != '' and self.mailing_address is not None and \
                    other.mailing_address != '' and other.mailing_address is not None:
                message = 'Mailing Addresses are different:\n{}:{}\n{}:{}'.format(first_name,
                                                                                  self.mailing_address,
                                                                                  second_name,
                                                                                  other.mailing_address)
                logger.debug(message)
                rtn += message + "\n"
            if self.owner != other.owner and \
                    self.owner != '' and self.owner is not None and \
                    other.owner != '' and other.owner is not None:
                message = 'Owners are different:\n{}:{}\n{}:{}'.format(first_name,
                                                                       self.owner,
                                                                       second_name,
                                                                       other.owner)
                logger.debug(message)
                rtn += message + "\n"
            if rtn != '':
                rtn = 'Site Data Differences:\n' + rtn
        else:
            rtn = 'Account numbers are different:\n{}:{}\n{}:{}'.format(first_name,
                                                                        self.account,
                                                                        second_name,
                                                                        other.account)
            logger.debug(rtn)
        return rtn
