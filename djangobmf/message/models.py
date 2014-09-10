#!/usr/bin/python
# ex:set fileencoding=utf-8:


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.base import ContentFile
from django.utils.text import slugify

from ..settings import BASE_MODULE
from ..utils import get_model_from_cfg

import uuid
import logging
import email
from email.parser import Parser

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Message(models.Model):
    """
    Model which informs users about changes in the history
    """
   #user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=False, null=True)
    parent = models.ForeignKey("self", blank=True, null=True)

   #mailbox
    obj_ct = models.ForeignKey(ContentType, related_name=False, null=True)
    obj_id = models.PositiveIntegerField(null=True)
    obj = GenericForeignKey('obj_ct', 'obj_id')

    subject = models.CharField(_("Topic"), max_length=255, blank=False, null=True)
    message_id = models.CharField(_("Message ID"), max_length=255, blank=True, null=True, editable=False)
   #from_header = models.CharField(
   #    max_length=255,
   #)
   #to_header = models.TextField()
   #outgoing = models.BooleanField(
   #    default=False,
   #    blank=True,
   #)

    body = models.TextField()
    encoded = models.BooleanField(
        default=False,
        help_text='True if the e-mail body is Base64 encoded'
    )
    document = models.ForeignKey(BASE_MODULE["DOCUMENT"], null=True, blank=True)

    processed = models.DateTimeField(
        auto_now_add=True
    )
    read = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
    )

    def erpget_project(self):
        return None

    def erpget_customer(self):
        return None

   #created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False,)
   #changed = models.DateTimeField(_("Changed"), auto_now=True, editable=False,)

   #mailbox = models.ForeignKey(Mailbox, related_name='messages')
   #in_reply_to = models.ForeignKey(
   #    'django_mailbox.Message',
   #    related_name='replies',
   #    blank=True,
   #    null=True,
   #)

    class Meta:
        ordering = ('-processed',)
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        get_latest_by = "processed"
        default_permissions=()

    def __str__(self):
        return self.subject

    @classmethod
    def from_email(self, fileobj):
        """
        generates a message object from an file object (email)
        """
        raw = fileobj.read()
        message = email.message_from_string(raw)
        if not message:
            logger.warning("Message not processable.")
            return None
        Document = get_model_from_cfg('DOCUMENT')

        file = ContentFile(raw)

        if message['subject']:
            file.name = 'mail-%s.eml' % slugify(message['subject'].decode('utf-8', 'replace'))
        else:
            file.name = 'mail.eml'

        document = Document(file=file)
        document.save()

        object = self()
        object.document = document
        object.save()

        return object


   #@property
   #def address(self):
   #    """Property allowing one to get the relevant address(es).

   #    In earlier versions of this library, the model had an `address` field
   #    storing the e-mail address from which a message was received.  During
   #    later refactorings, it became clear that perhaps storing sent messages
   #    would also be useful, so the address field was replaced with two
   #    separate fields.

   #    """
   #    addresses = []
   #    addresses = self.to_addresses + self.from_address
   #    return addresses

   #@property
   #def from_address(self):
   #    if self.from_header:
   #        return [parseaddr(self.from_header)[1].lower()]
   #    else:
   #        return []

   #@property
   #def to_addresses(self):
   #    addresses = []
   #    for address in self.to_header.split(','):
   #        if address:
   #            addresses.append(
   #                parseaddr(
   #                    address
   #                )[1].lower()
   #            )
   #    return addresses

   #def reply(self, message):
   #    """Sends a message as a reply to this message instance.

   #    Although Django's e-mail processing will set both Message-ID
   #    and Date upon generating the e-mail message, we will not be able
   #    to retrieve that information through normal channels, so we must
   #    pre-set it.

   #    """
   #    if self.mailbox.from_email:
   #        message.from_email = self.mailbox.from_email
   #    else:
   #        message.from_email = settings.DEFAULT_FROM_EMAIL
   #    message.extra_headers['Message-ID'] = make_msgid()
   #    message.extra_headers['Date'] = formatdate()
   #    message.extra_headers['In-Reply-To'] = self.message_id
   #    message.send()
   #    return self.mailbox.record_outgoing_message(
   #        email.message_from_string(
   #            message.message().as_string()
   #        )
   #    )

   #@property
   #def text(self):
   #    return self.get_text_body()

   #def get_text_body(self):
   #    def get_body_from_message(message):
   #        body = ''
   #        for part in message.walk():
   #            if (
   #                part.get_content_maintype() == 'text'
   #                and part.get_content_subtype() == 'plain'
   #            ):
   #                charset = part.get_content_charset()
   #                this_part = part.get_payload(decode=True)
   #                if charset:
   #                    this_part = this_part.decode(charset, 'replace')

   #                body += this_part
   #        return body

   #    return get_body_from_message(
   #        self.get_email_object()
   #    ).replace('=\n', '').strip()

   #def _rehydrate(self, msg):
   #    new = EmailMessage()
   #    if msg.is_multipart():
   #        for header, value in msg.items():
   #            new[header] = value
   #        for part in msg.get_payload():
   #            new.attach(
   #                self._rehydrate(part)
   #            )
   #    elif ATTACHMENT_INTERPOLATION_HEADER in msg.keys():
   #        try:
   #            attachment = MessageAttachment.objects.get(
   #                pk=msg[ATTACHMENT_INTERPOLATION_HEADER]
   #            )
   #            for header, value in attachment.items():
   #                new[header] = value
   #            encoding = new['Content-Transfer-Encoding']
   #            if encoding and encoding.lower() == 'quoted-printable':
   #                # Cannot use `email.encoders.encode_quopri due to
   #                # bug 14360: http://bugs.python.org/issue14360
   #                output = six.BytesIO()
   #                encode_quopri(
   #                    six.BytesIO(
   #                        attachment.document.read()
   #                    ),
   #                    output,
   #                    quotetabs=True,
   #                    header=False,
   #                )
   #                new.set_payload(
   #                    output.getvalue().decode().replace(' ', '=20')
   #                )
   #                del new['Content-Transfer-Encoding']
   #                new['Content-Transfer-Encoding'] = 'quoted-printable'
   #            else:
   #                new.set_payload(
   #                    attachment.document.read()
   #                )
   #                del new['Content-Transfer-Encoding']
   #                encode_base64(new)
   #        except MessageAttachment.DoesNotExist:
   #            new[ALTERED_MESSAGE_HEADER] = (
   #                'Missing; Attachment %s not found' % (
   #                    msg[ATTACHMENT_INTERPOLATION_HEADER]
   #                )
   #            )
   #            new.set_payload('')
   #    else:
   #        for header, value in msg.items():
   #            new[header] = value
   #        new.set_payload(
   #            msg.get_payload()
   #        )
   #    return new

   #def get_body(self):
   #    if self.encoded:
   #        return base64.b64decode(self.body.encode('ascii'))
   #    return self.body.encode('utf-8')

   #def set_body(self, body):
   #    if six.PY3:
   #        body = body.encode('utf-8')
   #    self.encoded = True
   #    self.body = base64.b64encode(body).decode('ascii')

   #def get_email_object(self):
   #    """ Returns an `email.message.Message` instance for this message."""
   #    body = self.get_body()
   #    if six.PY3:
   #        flat = email.message_from_bytes(body)
   #    else:
   #        flat = email.message_from_string(body)
   #    return self._rehydrate(flat)

   #def delete(self, *args, **kwargs):
   #    for attachment in self.attachments.all():
   #        # This attachment is attached only to this message.
   #        attachment.delete()
   #    return super(Message, self).delete(*args, **kwargs)

   #def __unicode__(self):
   #    return self.subject
