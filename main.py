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
        return_message = ''
        for orig in self.worksheet_handler.get_accounts():
            for new in self.soup_handler.get_accounts(self.worksheet_handler.get_accounts()):
                differences = new.differences(orig)
                if differences != '' and self.config_handler.spreadsheet_auto_update:
                    self.worksheet_handler.update_account(new)
                return_message += differences
        return return_message


def run(config_mgr):
    logger = get_logger()
    logger.debug('Starting run')
    brevard_checker = BrevardAccountChecker(config_mgr)
    results = brevard_checker.validate()


if __name__ == '__main__':
    log_config_file = 'log.cfg'
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, default='config.ini',
                        help='configuration file for this app.  If it does not exist, it will be created')
    args = parser.parse_args()
    cfg = ConfigHandler(args.config)
    load_log_config(cfg.log_config_file)
    run(cfg)
