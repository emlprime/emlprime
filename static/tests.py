from emlprime.common.tests import CommonTestCase
from emlprime.static.models import Project, Blog, Comic

from datetime import date

from django.core import mail, management
from django.conf import settings
from django.utils import simplejson

class TestCreation(CommonTestCase):

    def setUp(self):
        CommonTestCase.setUp(self)

    def test_projectCreation(self):
        """ Tests the creation of a project object
        """
        project = Project()
        self.failUnless(AssertionError)
        project = Project(name="test", description="test_description", email="email@host.com")
        self.failUnlessEqual(project.name, "test")
        self.failUnlessEqual(project.description, "test_description")
        self.failUnlessEqual(project.email, "email@host.com")

    def test_blogCreation(self):
        """ Tests the creation of a blog object
        """
        blog = Blog()
        self.failUnless(AssertionError)
        blog = Blog(title="test", entry="test_entry", date=date(2008, 12, 17))
        self.failUnlessEqual(blog.title, "test")
        self.failUnlessEqual(blog.entry, "test_entry")
        self.failUnlessEqual(blog.date, date(2008, 12, 17))

    def test_comicCreation(self):
        """ Tests the creation of a comic object
        """
        comic = Comic()
        self.failUnless(AssertionError)
        comic = Comic(title="test", comic="test_comic.gif", date=date(2008, 12, 17))
        self.failUnlessEqual(comic.title, "test")
        self.failUnlessEqual(comic.comic, "test_comic.gif")
        self.failUnlessEqual(comic.date, date(2008, 12, 17))

class TestStatic(CommonTestCase):
    def setUp(self):
        CommonTestCase.setUp(self)

    def test_navigation(self):
        """ Alice visits each page.

        She should...
        """
        alice = self.alice
        urls = ["/work/", "/us/", "/play/", "/", "/us/peter/", "/us/laura/", "/us/alice/", "/work/rates/", "/work/sample_workflow/"]
        # see all three navigation titles on each page
        for url in urls:
            self.alice.clicks_a_link(url)

        
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

    def test_comic_page(self):
        """ Alice goes to the play page and selects the comic link

        she should...
        """
        alice = self.alice

        for i in range(5):
            Comic.objects.create(title="Comic %d" % (i + 1), date=date(2008, 1, i + 1))

        latest_comic = Comic.objects.latest()
        first_comic = Comic.objects.get(title="Comic 1")

        # see the play page displayed
        templates_used = ["comic.html"]

        doc = alice.clicks_a_link("/play/comic/", templates_used=templates_used)
        alice.sees_an_element(doc, element="img", id="comic_%d" % latest_comic.id)

        doc = alice.clicks_a_link("/play/comic/%s/" % first_comic.id, templates_used=templates_used)
        alice.sees_an_element(doc, element="img", id="comic_%d" % first_comic.id)

        # sees a link to the first comic
        alice.sees_a_link(doc, href="/play/comic/%s/" % first_comic.id)

        # next and previous
        alice.sees_a_link(doc, href="/play/comic/%s/" % first_comic.id)
        alice.sees_a_link(doc, href="/play/comic/%s/" % first_comic.id)

        # sees a link to the latest comic
        alice.sees_a_link(doc, href="/play/comic/%s/" % first_comic.id)

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
