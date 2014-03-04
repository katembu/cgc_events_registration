from django.db import models
from django.utils.translation import ugettext as _


class Events(models.Model):
    class Meta:
        verbose_name = _(u"Event")
        verbose_name = _(u"Events")

    STATUS_ACTIVE = 'active'
    STATUS_CANCELLED = 'cancelled'
    STATUS_ENDED = 'ended'
    STATUS_MOVED = 'moved'
    STATUS_INACTIVE = 'INACTIVE'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, _(u"Active")),
        (STATUS_CANCELLED, _(u"Cancelled")),
        (STATUS_ENDED, _(u"Ended")),
        (STATUS_MOVED, _(u"Moved")),
        (STATUS_INACTIVE, _(u"Inactive")))

    event_name = models.CharField(_(u"Name"), blank=True, null=True,
                                  max_length=100)
    capacity = models.IntegerField(_(u"Capacity"), blank=True, null=True,
                                  max_length=100)
    start_date = models.DateTimeField(_(u"Start Time"))
    end_date = models.DateTimeField(_(u"End Time"), blank=True, null=True,
                                  max_length=100)
    status = models.CharField(_(u"status"), max_length=32,
                              choices=STATUS_CHOICES,
                              default=STATUS_INACTIVE)
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True,
                                      help_text=_(u"When the record " \
                                                   "was created"),
                                    db_index=True)

    def __unicode__(self):
        return  u"%s " % self.event_name

class Participants(models.Model):
    class Meta:
        verbose_name = _(u"Participant")
        verbose_name = _(u"Participants")

    STATUS_ATTENDED = 1
    STATUS_NEVERSHOWED = 0

    STATUS_CHOICES = (
        (STATUS_ATTENDED, _(u"Attended")),
        (STATUS_NEVERSHOWED, _(u"Never Showed Up")))

    first_name = models.CharField(_(u"First Name"), blank=True, null=True,
                                  max_length=200)
    last_name = models.CharField(_(u"Last Name"), blank=True, null=True,
                                  max_length=200)
    mobile = models.CharField(_(u"Mobile Number"), blank=True, null=True,
                                  max_length=100)
    email = models.EmailField(_(u"Email"), blank=True, null=True)
    dob = models.DateField(_(u"Date of Birth"), blank=True, null=True)
    event = models.ForeignKey(Events)
    code = models.CharField(_(u"registration Code"), blank=True, null=True,
                                  max_length=100)
    status = models.SmallIntegerField(_(u"Status"), choices=STATUS_CHOICES,
                              default=STATUS_NEVERSHOWED)
    created_on = models.DateTimeField(_(u"Created on"), auto_now_add=True,
                                      help_text=_(u"When the  record " \
                                                   "was created"),
                                    db_index=True)

    def fullname(self):
        return u"%(firstname)s %(lastname)s" % \
                {'firstname': self.first_name, 'lastname': self.last_name}

    def __unicode__(self):
        return  u"%(name)s - %(mobile)s" % \
                {'name': self.fullname(), 'mobile': self.mobile}


class OutgoingManager(models.Manager):
    '''
    A custom manager for LoggedMessage that limits query sets to
    outgoing messages only.
    '''

    def get_query_set(self):
        return super(OutgoingManager, self).get_query_set() \
                .filter(direction=LoggedMessage.DIRECTION_OUTGOING)


class IncomingManager(models.Manager):
    '''
    A custom manager for LoggedMessage that limits query sets to
    incoming messages only.
    '''

    def get_query_set(self):
        return super(IncomingManager, self).get_query_set() \
                        .filter(direction=LoggedMessage.DIRECTION_INCOMING)


class LoggedMessage(models.Model):
    '''
    LoggedMessage model with the following fields:
        date        - date of the message
        direction   - DIRECTION_INCOMING or DIRECTION_OUTGOING
        text        - text of the message
        identity    - identity (ie. phone number) of the message (a string)
        status      - stores message status, (success, error, parse_error, etc)
        response_to - recursive foreignkey to self. Only used for outgoing
                      messages. Points to the LoggedMessage to which the
                      outgoing message is a response.

    Besides the default manager (objects) this model has to custom managers
    for your convenience:
        LoggedMessage.incoming.all()
        LoggedMessage.outgoing.all()
    '''

    class Meta:
        '''
        Django Meta class to set the translatable verbose_names and to create
        permissions. The can_view permission is used by rapidsms to determine
        whether a user can see the tab. can_respond determines if a user
        can respond to a message from the log view.
        '''
        verbose_name = _(u"logged message")
        verbose_name = _(u"logged messages")
        ordering = ['-date', 'direction']
        permissions = (
            ("can_view", _(u"Can view")),
            ("can_respond", _(u"Can respond")),
        )

    DIRECTION_INCOMING = 'I'
    DIRECTION_OUTGOING = 'O'

    DIRECTION_CHOICES = (
        (DIRECTION_INCOMING, _(u"Incoming")),
        (DIRECTION_OUTGOING, _(u"Outgoing")))

    #Outgoing STATUS types:
    STATUS_SUCCESS = 'success'
    STATUS_WARNING = 'warning'
    STATUS_ERROR = 'error'
    STATUS_INFO = 'info'
    STATUS_ALERT = 'alert'
    STATUS_REMINDER = 'reminder'
    STATUS_LOGGER_RESPONSE = 'from_logger'
    STATUS_SYSTEM_ERROR = 'system_error'

    #Incoming STATUS types:
    STATUS_SUCCESS = 'success'
    STATUS_MIXED = 'mixed'
    STATUS_PARSE_ERRROR = 'parse_error'
    STATUS_BAD_VALUE = 'bad_value'
    STATUS_INAPPLICABLE = 'inapplicable'
    STATUS_NOT_ALLOWED = 'not_allowed'

    STATUS_CHOICES = (
        (STATUS_SUCCESS, _(u"Success")),
        (STATUS_WARNING, _(u"Warning")),
        (STATUS_ERROR, _(u"Error")),
        (STATUS_INFO, _(u"Info")),
        (STATUS_ALERT, _(u"Alert")),
        (STATUS_REMINDER, _(u"Reminder")),
        (STATUS_LOGGER_RESPONSE, _(u"Response from logger")),
        (STATUS_SYSTEM_ERROR, _(u"System error")),

        (STATUS_MIXED, _(u"Mixed")),
        (STATUS_PARSE_ERRROR, _(u"Parse Error")),
        (STATUS_BAD_VALUE, _(u"Bad Value")),
        (STATUS_INAPPLICABLE, _(u"Inapplicable")),
        (STATUS_NOT_ALLOWED, _(u"Not Allowed")))

    date = models.DateTimeField(_(u"date"), auto_now_add=True)
    direction = models.CharField(_(u"type"), max_length=1,
                                 choices=DIRECTION_CHOICES,
                                 default=DIRECTION_OUTGOING)
    text = models.TextField(_(u"text"))
    identity = models.CharField(_(u"identity"), max_length=100)
    status = models.CharField(_(u"status"), max_length=32,
                              choices=STATUS_CHOICES, blank=True, null=True)

    response_to = models.ForeignKey('self', verbose_name=_(u"response to"),
                                    related_name='response', blank=True,
                                    null=True)

    #Setup a default manager
    objects = models.Manager()

    # Setup custom managers.  These allow you to do:
    #    LoggedMessage.incoming.all()
    # or
    #    LoggedMessage.outgoing.all()
    incoming = IncomingManager()
    outgoing = OutgoingManager()

    def is_incoming(self):
        '''
        Returns true if this is the log of an incoming message, else false
        '''
        return self.direction == self.DIRECTION_INCOMING

    def __unicode__(self):
        return  u"%(direction)s - %(ident)s - %(text)s" % \
                 {'direction': self.get_direction_display(),
                  'ident': self.identity,
                  'text': self.text}
