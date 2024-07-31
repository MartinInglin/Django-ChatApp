from django.contrib import admin
from .models import Chat, Message

class MessageAdmin(admin.ModelAdmin): #Hier wird festgelegt, welche Felder im Admin-Panel angezeigt / bearbeitet werden können
    fields = ('chat', 'text', 'created_at') #Hier werden die Felder definiert, die bearbeitet werden können
    list_display = ('text', 'created_at') #Hier werden die Spalten definiert, die in der Übersicht angezeigt werden
    search_fields = ('text',) #Dadurch wird ein Suchfeld eingefügt


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
