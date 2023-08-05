from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import syngo
from syngo.models import Captcha


class SyngoTest(TestCase):
    def test_syngo(self):
        User = get_user_model()
        user = User.objects.create(username="toto", password="toto")

        # Test register
        self.assertEqual(len(syngo.list_accounts()), 1)
        self.assertEqual(syngo.register(user).status_code, 201)
        self.assertEqual(syngo.register(user).status_code, 200)
        self.assertEqual(syngo.register(user).status_code, 200)
        self.assertEqual(len(syngo.list_accounts()), 2)

        # Test shadow_ban
        self.assertEqual(syngo.list_accounts()[1]["shadow_banned"], 0)
        syngo.shadow_ban(user)
        self.assertEqual(syngo.list_accounts()[1]["shadow_banned"], 1)
        syngo.shadow_ban(user, unban=True)
        self.assertEqual(syngo.list_accounts()[1]["shadow_banned"], 0)

        # Test deactivate
        syngo.deactivate(user)
        self.assertEqual(len(syngo.list_accounts()), 1)

        # Test registration token
        ret = syngo.registration_token().json()
        self.assertEqual(len(ret["token"]), 16)
        self.assertEqual(ret["uses_allowed"], 1)
        self.assertEqual(ret["completed"], 0)

        # Test views
        r = self.client.get(reverse("syngo:generate"))
        generated = Captcha.objects.last()
        self.assertEqual(generated.get_absolute_url(), r.url)

        get = self.client.get(r.url)
        self.assertIn(generated.image.url, get.content.decode())

        ko = self.client.post(r.url, {"guess": "toto"})
        self.assertIn(generated.image.url, ko.content.decode())

        ok = self.client.post(r.url, {"guess": generated.secret})
        self.assertIn("Success !", ok.content.decode())
