#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.core.management.base import BaseCommand

import logging
import sys

from ...message.models import Message

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    command = "Receive incoming mail via stdin"

    def handle(self, *args, **options):
        message = Message.from_email(sys.stdin)
        if message:
           #logger.info("Message received from %s" % message['from'])
            logger.info("Message received")
        else:
            logger.warning("Message not processable.")
