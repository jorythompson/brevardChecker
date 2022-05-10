from thompcoutils import file_utils
from thompcoutils.config_utils import ConfigManager
from os.path import exists


class ConfigHandler:
    """
    This class is used to manage the configuration of the BrevardCheck script.
    """
    def __init__(self, file_name):
        """
        Initialize the class with the file name.
        param file_name: The name of the configuration file.
        """
        create = not exists(file_name)
        if create:
            file_utils.touch(file_name)
        self.config_mgr = ConfigManager(file_name=file_name, create=create)
        heading = 'web'
        self.web_page_delay = self.config_mgr.read_entry(heading, 'page delay', 1)
        heading = 'spreadsheet'
        self.spreadsheet_file_name = self.config_mgr.read_entry(heading, 'spreadsheet file name', 'brevard_data.xlsx')
        self.spreadsheet_auto_update = self.config_mgr.read_entry(heading, 'auto-update spreadsheet', False)
        heading = 'debug'
        self.debug_folder = self.config_mgr.read_entry(heading, 'debug folder', 'debug')
        self.debug = self.config_mgr.read_entry(heading, 'debug', False)
        heading = 'files'
        self.json_extension = self.config_mgr.read_entry(heading, 'json extension', 'json')
        self.log_config_file = self.config_mgr.read_entry(heading, 'log config file', 'logging.config')
        if create:
            self.config_mgr.write(out_file=file_name, overwrite=True, stop=True)
            print('Created config file: {}'.format(file_name))
            exit(0)
