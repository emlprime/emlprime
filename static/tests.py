from emlprime.common.tests import CommonTestCase
from emlprime.static.models import Project

from django.core import mail, management
from django.conf import settings
from django.utils import simplejson

class TestStatic(CommonTestCase):
    def setUp(self):
        CommonTestCase.setUp(self)

    def test_navigation(self):
        """ Alice visits each page.

        She should...
        """
        pass
        #alice = self.alice
        #urls = ["/work/", "/us/", "/play/"]
        #expected_titles = ["work", "us", "play"]
        #expected_titles.sort()
        ## see all three navigation titles on each page
        #for url in urls:
        #    doc = self.alice.clicks_a_link(url)
        #    links = [("/work/","/media/images/work.png"), ("/us/","/media/images/us.png"), ("/play/", "/media/images/play.png")]
        #    navigation = doc.find(id="navigation")
        #    displayed_links = navigation.findAll("a")
        #    for href, src in links:
        #        if href != url:
        #            alice.sees_a_link(navigation, href, src)
        #    # see links to all three sections except to the current page
        #    current_page_is_linked = False
        #    for link in displayed_links:
        #        self.failUnless(url not in link["href"], "%s should not be a link on its own page" % url)
        
    def test_home_page(self):
        """ Alice goes to www.emlprime.com

        she should...
        """
        alice = self.alice
        # see the homepage
        templates_used = ["index.html", "base.html"]
        doc = alice.clicks_a_link("/", templates_used=templates_used)

        # see the footer with email and phone from settings and the current year copyright
        footer = doc.find(id="footer")
        for key, value in settings.FOOTER_DATA.items():
            span = footer.find(id=key)
            self.alice.sees_a_string(span, value)

    def test_work_page(self):
        """ Alice goes to www.emlprime.com and follows the link to the work page

        she should...
        """
        alice = self.alice
        # see the page
        templates_used = ["work.html"]
        doc = alice.clicks_a_link("/work/", templates_used=templates_used)
        # submit a project request using the form
        self.alice.sees_a_form(doc, "project")
        self.alice.submits_a_form(doc, "project", {'name':'test', 'email':'test@emlprime.com', 'description':'test project'})
        self.failUnlessEqual(Project.objects.get().name, 'test')
        # check that email is sent
        # print "outbox:", mail.outbox[0].subject
        # print "outbox:", mail.outbox[0].message()

    def test_workflow_page(self):
        """ Alice goes to www.emlprime.com/work and clicks on the link to the sample workflow
        
        she should...
        """
        alice = self.alice
        # see the page
        templates_used = ["sample_workflow.html"]
        doc = alice.clicks_a_link("/work/sample_workflow/", templates_used=templates_used)
        # see the divs for the initial stage, sprint cycle, and approval cycle
        elements = ["workflow_initial_stage", "workflow_sprint_cycle", "workflow_approval_cycle"]
        # see the great idea, transformation, and initial sprint divs inside the initial stage
        elements += ["great_idea", "transformation", "initial_sprint"]

        # see the assign sprint, write tests, write code, update burndown, and present stories inside the sprint cycle
        elements += ["assign_sprint_tasks", "write_tests","write_code","update_burndown", "present_stories"]

        # see the story approval, get paid, add ideas, groom backlog, and design next sprint inside the approval cycle
        elements += ["story_approval", "get_paid", "design_next_sprint"]

        for element in elements:
            alice.sees_an_element(doc, id=element)
        # see a link on the great idea div that links back to the work page
        link = doc.find(id="workflow_initial_stage").find(href="/work/")
        self.failUnless(link, "could not find link from workflow back to project form")

    def test_us_page(self):
        """ Alice goes to www.emlprime.com and follows the link to the us page

        she should...
        """
        alice = self.alice
        # see the page
        templates_used = ["us.html"]
        doc = alice.clicks_a_link("/us/", templates_used=templates_used)
        # see peter, laura, and alice
        elements = ["peter", "laura", "alice"]
        #click on peter, laura, and alice's .__dict__ links to see their description pages
        for element in elements:
            doc=alice.clicks_a_link("/us/%s/" % element)
            alice.sees_an_element(doc, id="portfolio")
            doc=alice.clicks_a_link("/us/")
        # see __str__, img, type, dir, doc, and __dict__ in each person's section
        elements += ["__str__", "img",  "type", "dir", "doc", ".__dict__"]
        for element in elements:
            alice.sees_an_element(doc, id=element)
        


    def test_play_page(self):
        """ Alice goes to www.emlprime.com and clicks the link to the play page

        she should...
        """
        alice = self.alice
        # see the play page displayed
        templates_used = ["play.html"]
        doc = alice.clicks_a_link("/play/", templates_used=templates_used)

    def test_blog(self):
        """ Alice goes to the play page and selects the blog link

        she should...
        """
        alice = self.alice
        # see the play page displayed
        templates_used = ["blog.html"]
        doc = alice.clicks_a_link("/play/blog/", templates_used=templates_used)

    def test_play_page(self):
        """ Alice goes to the play page and selects the comic link

        she should...
        """
        alice = self.alice
        # see the play page displayed
        templates_used = ["comic.html"]
        doc = alice.clicks_a_link("/play/comic/", templates_used=templates_used)

    def test_game_page(self):
        """Alice goes to the play page and selects the game link
        
        she should...
        """
        alice = self.alice
        #see the page
        templates_used = ["game.html"]
        doc = alice.clicks_a_link("/play/game/", templates_used=templates_used)
        # see the game background and the four colors
        elements = ["game", "green", "red", "blue", "yellow"]
        for element in elements:
            alice.sees_an_element(doc, id=element)
        # tests the answer key list provided to jquery
        response = alice.client.get("/play/get_answer_key/")
        displayed_list = simplejson.loads(response.content)
        self.failUnlessEqual(type(displayed_list), list)
        self.failUnlessEqual(len(displayed_list), 50)
