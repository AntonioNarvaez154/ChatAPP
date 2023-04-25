from django.urls import path, re_path

from .views import (
    private_messages,
    DetailMs,
    ChanelDetailView,
    Inbox
)

UUID_CHANEL_REGEX = r'chanel/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'

urlpatterns = [

    re_path(UUID_CHANEL_REGEX, ChanelDetailView.as_view()),

    path("dm/<str:username>",private_messages),
    path("ms/<str:username>", DetailMs.as_view(), name="detailms"),
    
    path("",Inbox.as_view(), name="inbox"),
]