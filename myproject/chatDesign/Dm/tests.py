from django.test import TestCase

from .models import ChanelMessage, ChanelUser, Chanel

from django.contrib.auth import get_user_model

User = get_user_model()

class ChanelTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create(username='antonio', password='tony')
        self.user_b = User.objects.create(username='dosusuario', password='hola')
        self.user_c = User.objects.create(username='userC', password='mundo')

    def test_usuario_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 3)

    def test_each_chanel_user(self):
        qs = User.objects.all()
        for usuario in qs:
            chanel_obj = Chanel.objects.create()
            chanel_obj.users.add(usuario)

        chanel_qs = Chanel.objects.all()
        self.assertEqual(chanel_qs.count(), 3)
        chanel_qs_1 = chanel_qs.only_one()
        self.assertEqual(chanel_qs_1.count(), chanel_qs.count())

    def test_two_users(self):
        chanel_obj = Chanel.objects.create()
        ChanelUser.objects.create(user=self.user_a, chanel=chanel_obj)
        ChanelUser.objects.create(user=self.user_b, chanel=chanel_obj)

        chanel_obj2 = Chanel.objects.create()
        ChanelUser.objects.create(user=self.user_c, chanel=chanel_obj2)

        qs = Chanel.objects.all()
        self.assertEqual(qs.count(), 2)
        only_two = qs.only_two()
        self.assertEqual(only_two.count(), 1)