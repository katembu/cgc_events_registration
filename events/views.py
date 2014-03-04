from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import json
from events.models import LoggedMessage
from utils import process_sms

@csrf_exempt
def incomingsms(request):
    #self.debug('Request: %s' % request.POST)
    if  request.method == 'POST':
        data = request.POST

        params = ','.join('%s=%s' % (k, request.POST[k]) for k in sorted(request.POST.keys()))
        '''
            if self.password is not None:
                secure_key = sha.new(','.join((self.url, params, self.password))).digest()
                if base64.b64decode(request.META.get('HTTP_X_REQUEST_SIGNATURE', '')) != secure_key:
                    return HttpResponseForbidden(json.dumps({'error': {'message': 'Bad password'}}))
        '''
        print params
        action = data.get('action', '')
        if action == 'incoming':
            sender = data.get('from', '')
            sms = data.get('message', '')
            'LOG SMS INTO INCOMING SMS DATABASES'
            logged = LoggedMessage()
            logged.direction = LoggedMessage.DIRECTION_INCOMING
            logged.text = sms
            logged.identity = sender
            logged.status = LoggedMessage.STATUS_INFO
            logged.save()

            l = process_sms(sms, sender)  
            print "pass"
            '''OutGoing Log Respond'''
            ll = LoggedMessage()
            ll.direction = LoggedMessage.DIRECTION_OUTGOING
            ll.text = l
            ll.identity = sender
            ll.response_to = logged
            ll.save()

            events = [{'event': 'send', 'messages': [{'to': sender, 'message': l }]}]
            return HttpResponse(json.dumps({'events': events}), content_type='application/json')

        elif action == 'outgoing':
            HttpResponseForbidden(json.dumps({'error': {'message': 'Bad password'}}))
        else:
            HttpResponseForbidden(json.dumps({'error': {'message': 'Bad password'}}))
            #events = [{'event': 'send', 'messages': [{'to': '0716122488', 'message': "No Action you"}]}]
            #return HttpResponse(json.dumps({'events': events}), content_type='application/json')
            #events = [{'event': 'send', 'messages': [{'to': sender, 'message': "Thank you"}]}]
            #return HttpResponse(json.dumps({'events': events}), content_type='application/json')
    else:
        HttpResponseForbidden(json.dumps({'error': {'message': 'Bad password'}}))
