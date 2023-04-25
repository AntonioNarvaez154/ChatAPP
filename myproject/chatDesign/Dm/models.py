from django.db import models
from django.conf import settings
from django.db.models import Count
from django.apps import apps

import uuid

User = settings.AUTH_USER_MODEL

class ModelBase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChanelMessage(ModelBase):
    chanel = models.ForeignKey("Chanel", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)  
    text = models.TextField()

class ChanelUser(ModelBase):
    chanel = models.ForeignKey("Chanel", null = True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class ChanelQuerySet(models.QuerySet):

    def only_one(self):
        return self.annotate(num_users = Count("users")).filter(num_users=1)

    def only_two(self):
        return self.annotate(num_users = Count("users")).filter(num_users=2)
    
    def filter_by_username(self, username):
        return self.filter(chaneluser__user__username=username)


class ChanelManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        return ChanelQuerySet(self.model, using=self._db)
    
    def filter_ms_by_private(self, username_a, username_b):
        return self.get_queryset().only_two().filter_by_username(username_a). filter_by_username(username_b)


    def get_or_create_user_chanel_actual(self, user):
        qs = self.get_queryset().only_one().filter_by_username(user.username)
        if qs.exists():
            return qs.order_by("time").first, False
        
        chanel_obj = Chanel.objects.create()
        ChanelUser.objects.create(usser=user, chanel=chanel_obj)
        return chanel_obj, True


    def get_or_create_chanel_ms(self, username_a, username_b):
        qs = self.filter_ms_by_private(username_a, username_b)
        if qs.exists():
            #devuelve el objeto y verifica si se creo o no
            return qs.order_by("time").first(), False
        

        User = apps.get_model("auth", model_name='User') 
        user_a, user_b = None, None

        try:
            user_a = User.objects.get(username=username_a)
        except User.DoesNotExist:
            return None, False

        try:
            user_b = User.objects.get(username=username_b)
        except User.DoesNotExist:
            return None, False

        if user_a == None or user_b == None:
            return None,False

        obj_chanel = Chanel.objects.create()

        chanel_user_a = ChanelUser(user= user_a, chanel=obj_chanel)
        chanel_user_b = ChanelUser(user= user_b, chanel=obj_chanel)

        ChanelUser.objects.bulk_create([chanel_user_a, chanel_user_b])
        return obj_chanel, True


class Chanel(ModelBase):
    users = models.ManyToManyField(User, blank=True, through = ChanelUser)

    objects = ChanelManager()
    