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

        # see the page with the logo
        logo = doc.find(id="logo")
        self.failUnlessEqual(logo.find('img')["alt"], "EMLPrime")
        logo_image = doc.find(id="logo").find(src="/media/images/logo.png")
        self.failUnless(logo_image, "Could not find %s" % logo.png)

        # see the mission statement and work, us, and play snippets
        mission_statement = doc.find(id="mission_statement")
        self.failUnless(mission_statement, "Could not find %s" % mission_statement)
        snippets = ["work","us","play"]
        for snippet in snippets:
            self.alice.sees_an_element(doc, "div", snippet)

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
        # see the initial conversation, sprint cycle, and approval cycle portions of the project diagram
        elements = ["mug_shot", "personal_info", "experience", "personality", "hobbies"]
        # see the name, email, and favorite bribe in the personal info section
        elements += ["name", "contact_email",  "favorite_bribe", "languages", "skills", "finished_projects"]
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
        # see the game background and the four colors
        elements = ["game", "green", "red", "blue", "yellow"]
        for element in elements:
            alice.sees_an_element(doc, id=element)
        # tests the answer key list provided to jquery
        response = alice.client.get("/play/get_answer_key/")
        displayed_list = simplejson.loads(response.content)
        self.failUnlessEqual(type(displayed_list), list)
        self.failUnlessEqual(len(displayed_list), 50)
