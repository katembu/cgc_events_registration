import re
from events.models import *


def process_sms(text, mobileno):
    'Check if more than two events are ACTIVE '
    active_events = Events.objects.filter(status=Events.STATUS_ACTIVE).count()
    if active_events > 1:
        extra_token = True
    else:
        extra_token = False

    tokens = re.split(r'\s+', text)

    if extra_token & (len(tokens) <= 2):
        return "Invalid Format: Reply with FIRSTNAME LASTNAME EVENTCODE"

    if (not extra_token) & (len(tokens) < 2):
        return "Invalid Format: Reply with FIRSTNAME LASTNAME"

    if extra_token:
        #check if event ID exist
        event_id = tokens[-1]
        tokens.pop(-1)
        #return(event_id)
        try:
            event = Events.objects.filter(status=Events.STATUS_ACTIVE, pk=event_id)[0]
        except:
            return "Invalid Events Code. Reply with correct event Code"

    else:
        event = Events.objects.filter(status=Events.STATUS_ACTIVE)[0]

    #GET NAMES 
    first_name = tokens.pop(0).upper()
    last_name = ' '.join(tokens).upper()

    p = Participants()
    p.first_name = first_name
    p.last_name = last_name
    p.mobile = mobileno
    p.event = event
    p.save()

    return "Thank you %s %s. You've Been registered for %s to "\
           "be held on %s " % (first_name, last_name, event.event_name,
                               event.start_date.strftime("%d-%m-%Y %H:%M"))
