from django.contrib import admin

# Register your models here.
from events.models import *


class LoggedMessageAdmin(admin.ModelAdmin):
    '''
    Custom ModelAdmin to be used for the LoggedMessage field. Enables
    filtering, searching (name and text fields), and the slick built-in
    django date-higherarchy widget.
    '''
    list_display = ('date', '__unicode__')
    list_filter = ['direction', 'date', 'identity']
    #search_fields = ['reporter__first_name', 'reporter__last_name', 'text']
    date_hierarchy = 'date'
admin.site.register(LoggedMessage, LoggedMessageAdmin)


class EventsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'start_date', 'end_date','capacity', 'status')
    list_filter = ['status']
    search_fields = ['event_name', 'status']
admin.site.register(Events, EventsAdmin)

class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','mobile', 'event')
    list_filter = ['mobile']
    search_fields = ['first_name', 'last_name','mobile']
admin.site.register(Participants, ParticipantsAdmin)
