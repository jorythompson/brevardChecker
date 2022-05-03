import logging
from typing import Optional
from thompcoutils import config_utils, email_utils
from thompcoutils.log_utils import get_logger


class EmailHandler:
    """
    This class handles Email (text) traffic to the user
    """
    def __init__(self, config_mgr: Optional["config_utils.ConfigHandler"]):
        """
        Constructor for an EmailHandler
        param config_mgr: the config_mgr for the project
        """
        self.email_cfg = config_utils.EmailConnectionConfig(cfg_mgr=config_mgr)
        self.send_messages = config_mgr.read_entry(self.email_cfg.section, 'send messages', True,
                                                   'If true, indicates all messages should be sent')
        self.email_recipients = config_mgr.read_entry(self.email_cfg.section, 'email recipients', [''],
                                                      'list of comma-delimited emails to receive messages')

    def send_email(self, subject: str, message: str):
        """
        Sends an email to the user
        param subject: the subject of the email
        param message: message to send
        return: None
        """
        logger = get_logger()
        message = message.replace('\n', '<br>')
        logger.debug('Sending email to {}'.format(self.email_recipients))
        email_sender = email_utils.EmailSender(email_cfg=self.email_cfg)
        email_sender.send(to_email=self.email_recipients, subject=subject, message=message)
