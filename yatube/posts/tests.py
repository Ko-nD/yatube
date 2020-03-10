from django.test import TestCase, override_settings
from django.core import mail
from django.urls import reverse
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
import tempfile
from django.conf import settings

from .models import User, Group, Post



class EmailTest(TestCase):
    def test_email_send(self):
        self.client.post('/auth/signup/', {'username': 'terminator', 'email': 'rocki@gmail.com', \
            'password1': 'skynetMyLove', 'password2': 'skynetMyLove'})

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(mail.outbox[0].subject,'Подтверждение регистрации Yatube')


@override_settings(CACHES=settings.TEST_CACHE)
class TestUserActions(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="TestUser", password="mrRobot")
        self.client.login(username='TestUser', password='mrRobot')

        self.user2 = User.objects.create_user(username="TestUser2", password="mrRobot")

    def test_new_profile(self):
        self.client.post('/auth/signup/', {'username': 'terminator', 'email': 'rocki@gmail.com', \
            'password1': 'skynetMyLove', 'password2': 'skynetMyLove'})

        response = self.client.get('/terminator/')

        self.assertEqual(response.status_code, 200)

    # проверка постов
    def test_new_post(self):
        response = self.client.post(reverse('new_post'), {'text': 'Пост создан'})
        self.assertContains(response, 'Ваша запись была успешно опубликована!')

    def test_new_post_logout(self):
        self.client.logout()

        response = self.client.post('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_publish_post(self):
        text = 'Создаём пост через тест'
        self.client.post(reverse('new_post'), {'text': 'Создаём пост через тест'})

        test_urls = [
            '',
            '/TestUser/',
            '/TestUser/1/',
        ]

        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, text)

    def test_edit_post(self):
        self.client.post(reverse('new_post'), {'text': 'Создаём пост через тест'})

        text = 'Отредактировал пост'
        self.client.post(reverse('post_edit', args=['TestUser', 1]), {'text': text})

        test_urls = [
            '',
            '/TestUser/',
            '/TestUser/1/',
        ]

        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, text)

    def test_delete_post(self):
        text = 'Удалим этот пост'
        self.client.post(reverse('new_post'), {'text': text})

        self.client.get(reverse('post_delete', args=['TestUser', 1]))

        response1 = self.client.get('')
        self.assertNotContains(response1, text)

        response2 = self.client.get('/TestUser/')
        self.assertNotContains(response2, text)

        response3 = self.client.get('/TestUser/1/')
        self.assertEqual(response3.status_code, 404)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_add_image(self):
        self.group = Group.objects.create(title='TestGroup', slug='testgroup', description='Test')
        with open('posts/test_media/image.png', 'rb') as fp:
            self.client.post('/new/', {'group': '1', 'text': 'Test', 'image': fp})

        test_urls = [
            '',
            '/TestUser/',
            '/TestUser/1/',
            '/group/testgroup/'
        ]

        for url in test_urls:
            response = self.client.get(url)
            self.assertContains(response, '<img')

        with open('posts/test_media/not_image.txt', 'rb') as fp:
            response = self.client.post( '/new/', {'group': '1', 'text': 'Dont publish', 'image': fp})
        response = self.client.get('')
        self.assertNotContains(response, 'Dont publish')

    # проверка подписок
    def test_follow_unfollow(self):
        # подписка
        self.client.get('/TestUser2/follow/')
        response = self.client.get('/TestUser/')
        self.assertEqual(response.context['follows'], 1)

        # отписка 
        self.client.get('/TestUser2/unfollow/')
        response = self.client.get('/TestUser/')
        self.assertEqual(response.context['follows'], 0)
    
    def test_follow_feed(self):
        # если подписан отображается
        self.post = Post.objects.create(text='Подписан', author=self.user2)
        self.client.get('/TestUser2/follow/')
        response = self.client.get('/follow/')
        self.assertContains(response, 'Подписан')
        
        # если не подписан - не отображается
        self.client.get('/TestUser2/unfollow/')
        response = self.client.get('/follow/')
        self.assertNotContains(response, 'Подписан')

    def test_add_comment(self):
        # авторизированный пользователь может комментировать
        self.client.post('/new/', {'text': 'Test'})
        self.client.post('/TestUser/1/comment/', {'text': 'авторизован'})
        response = self.client.get('/TestUser/1/')
        self.assertContains(response, 'авторизован')

        # неавторизированный пользователь не может комментировать
        self.client.logout()
        self.client.post('/TestUser/1/comment/', {'text': 'не авторизован'})
        response = self.client.get('/TestUser/1/')
        self.assertNotContains(response, 'не авторизован')


class TestServer(TestCase):
    def test_cache(self):
        key = make_template_fragment_key('index_page', [1])
        self.assertFalse(cache.get(key))
        self.client.get('')
        self.assertTrue(cache.get(key))

    def test_get_404(self):
        response = self.client.get('/404/')
        self.assertEqual(response.status_code, 404)
