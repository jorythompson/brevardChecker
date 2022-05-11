from configHandler import ConfigHandler
from emailHandler import EmailHandler
from sheetHandler import SheetHandler
from soupHandler import SoupHandler
import argparse
from thompcoutils.log_utils import load_log_config, get_logger


class BrevardAccountChecker:
    """
    This class is used to check the account status of the Brevard County Property Appraiser
    It uses an Excel spreadsheet to interact with the user.
    If you run the script without any arguments, it will create a new spreadsheet and configure file
    """
    def __init__(self, config_handler: ConfigHandler):
        """
        Initialize the class
        param config_mgr: The configuration manager
        """
        self.config_handler = config_handler
        self.worksheet_handler = SheetHandler(self.config_handler.spreadsheet_file_name)
        self.soup_handler = SoupHandler(self.config_handler)
        self.email_handler = EmailHandler(self.config_handler.config_mgr)
        self.updated_accounts = self.soup_handler.get_accounts(self.worksheet_handler.get_accounts())

    def validate(self):
        logger = get_logger()
        return_message = ''
        return_accounts = []
        for orig in self.worksheet_handler.get_accounts():
            logger.debug(f'Checking account {orig.account}')
            for new in self.soup_handler.get_accounts(self.worksheet_handler.get_accounts()):
                substantial_differences, differences = new.differences(orig)
                if substantial_differences:
                    return_accounts.append(new)
                if differences != '':
                    if self.config_handler.spreadsheet_auto_update:
                        self.worksheet_handler.update_account(new)
                return_message += differences
        return return_message, return_accounts


def run(config_handler: ConfigHandler):
    logger = get_logger()
    logger.debug('Starting run')
    brevard_checker = BrevardAccountChecker(config_handler)
    diff_text, diff_site_data = brevard_checker.validate()
    if len(diff_site_data) > 0:
        if len(diff_site_data) > 1:
            properties = 'properties'
        else:
            properties = 'property'
        if config_handler.spreadsheet_auto_update:
            changes = 'changes have been updated in {}'.format(config_handler.spreadsheet_file_name)
        else:
            changes = 'changes will not be updated in {}'.format(config_handler.spreadsheet_file_name)
        if brevard_checker.email_handler.send_messages:
            logger.info('Sending email')
            brevard_checker.email_handler.send_email(
                subject='changes in your {} on the Brevard Property Appraiser web site'.format(properties),
                message=diff_text + '\n' + changes)
        else:
            logger.info('Not sending email')
        logger.warning(diff_text)
        logger.warning(changes)
    else:
        logger.info('No changes found')


if __name__ == '__main__':
    """
    This is the main function that is called when the script is run from the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, default='config.ini',
                        help='configuration file for this app.  If it does not exist, it will be created')
    args = parser.parse_args()
    cfg = ConfigHandler(args.config)
    load_log_config(cfg.log_config_file)
    run(cfg)
