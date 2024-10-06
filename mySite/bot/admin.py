from django.contrib import admin
from .models import User,Ticket

class UserAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'phone_number', 'passkey')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('user__username', 'phone_number')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user__user__username', 'status', 'issue')
    search_fields = ('user__user__username', 'status')
    list_filter = ('user__user__username', 'status')

admin.site.register(User, UserAdmin)
admin.site.register(Ticket, TicketAdmin)