from django.contrib import admin

from .models import Chanel, ChanelUser, ChanelMessage

class ChanelMessageInline(admin.TabularInline):
    model = ChanelMessage
    extra = 1

class ChanelUserInline(admin.TabularInline):
    model = ChanelUser
    extra = 1


class ChanelAdmin(admin.ModelAdmin):
    inlines = [ChanelMessageInline, ChanelUserInline]

    class Meta:
        model = Chanel

admin.site.register(Chanel, ChanelAdmin)
admin.site.register(ChanelUser)
admin.site.register(ChanelMessage)