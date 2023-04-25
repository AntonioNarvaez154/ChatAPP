from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import ChanelMessage, ChanelUser, Chanel
from django.http import HttpResponse, Http404, JsonResponse
from .forms import FormMessages
from django.views.generic.edit import FormMixin

class Inbox(View):
    def get(self, request):

        inbox = Chanel.objects.filter(chaneluser__user__in=[request.user.id])

        context = {
            "inbox":inbox
        }
        return render(request, 'inbox.html', context)

class ChanelFormMixin(FormMixin):
    form_class = FormMessages
    #success_url = "./"

    def get_success_url(self):
        return self.request.path

    
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            raise PermissionDenied
        
        form = self.get_form()
        if form.is_valid():
            chanel = self.get_object()
            user = self.request.user
            message = form.cleaned_data.get("message")
            chanel_obj = ChanelMessage.objects.create(chanel=chanel, user=user, text=message)

            if self.request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({
                    'message': chanel_obj.text,
                    'username': chanel_obj.user.username                
                            }, status=201)

            return super().form_valid(form)

        else:

            if self.request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse({"Error":form.errors}, status=400)
            
            return super().form_invalid(form)

class ChanelDetailView(LoginRequiredMixin, ChanelFormMixin, DetailView):
    template_name= 'Dm/chanel_detail.html'
    queryset = Chanel.objects.all()

    def get_context_data(self, *args, ** kwargs):
        context = super().get_context_data(*args, **kwargs)

        obj = context['object']
        print(obj)

        # if self.request.user not in obj.users.all():
        #     raise PermissionDenied

        context['if_chanel_member'] = self.request.user in obj.users.all()

        return context

    # def get_queryset(self):
    #     usser = self.request.user
    #     username = usser.username

    #     qs = Chanel.objects.all().filter_by_username(username)
    #     return qs

class DetailMs(LoginRequiredMixin, ChanelFormMixin, DetailView):

    template_name = 'Dm/chanel_detail.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        my_username = self.request.user.username
        chanel, _ = Chanel.objects.get_or_create_chanel_ms(my_username, username)
        
        if username == my_username:
            my_chanel, _ = Chanel.objects.get_or_create_user_chanel_actual(self.request.user)

            return my_chanel
        
        if chanel == None:
            raise Http404

        return chanel



def private_messages(request, username, *args, **kwargs):

    if not request.user.is_authenticated:
        return HttpResponse("Prohibido")

    my_username = request.user.username


    chanel, created = Chanel.objects.get_or_create_chanel_ms(my_username, username)

    if created:
        print("Fue creado!")

    User_Chanel = chanel.chaneluser_set.all().values("user__username")
    print(User_Chanel)
    message_chanel = chanel.chanelmessage_set.all()
    print(message_chanel.values("text"))

    return HttpResponse(f"Chanel - {chanel.id}")

