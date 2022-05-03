import logging
from enum import Enum
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
        self.email_sender = email_utils.EmailSender(email_cfg=self.email_cfg)
        self.send_messages = config_mgr.read_entry(self.email_cfg.section, 'send_messages', True,
                                                   'If true, indicates all messages should be sent')
        self.email_recipients = config_mgr.read_entry(self.email_cfg.section, 'email_recipients', [''],
                                                      'list of comma-delimited emails to receive messages')

    def send_email(self, level: int, message: str, force=False):
        """
        Sends an email to the user

        param level: level of message which is translated to the subject of the email
        param message: message to send
        param force: overrides the send_messages member
        return: None
        """
        logger = get_logger()
        subject = None
        if level == logging.INFO:
            subject = 'Info'
        elif level == logging.ERROR:
            subject = 'Error'
        elif level == logging.WARNING or level == logging.WARN:
            subject = 'Warning'
        else:
            subject = level

        if force or self.send_messages:
            self.email_sender.send(to_email=self.email_recipients[0], subject=subject, message=message)
            logger.debug('sending message:"{}"'.format(message))
        else:
            logger.debug('message not sent:"{}"'.format(message))
