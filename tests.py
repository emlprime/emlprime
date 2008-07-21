from emlprime.common.tests import CommonTestCase

from django.core import management

class TestStory(CommonTestCase):
    def setUp(self):
        CommonTestCase.setUp(self)

    def test_home_page(self):
        """ Alice goes to www.emlprime.com

        she should...
        """
        alice = self.alice
        # see the page with the logo and navigation links
        templates_used = ["home.html", "base.html"]
        doc = alice.clicks_a_link("/", templates_used=templates_used)
        logo = doc.find(id="logo")
        self.failUnlessEqual(logo["alt"], "EMLPrime", "Could not find %s in %s" % EMLPrime, logo))
        work = doc.find(id="work.png")
        us = doc.find(id="us.png")
        play = doc.find(id="play.png")


