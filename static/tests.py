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
        alice = self.alice
        urls = ["/work/", "/us/", "/play/"]
        expected_titles = ["work", "us", "play"]
        expected_titles.sort()
        # see all three navigation titles on each page
        for url in urls:
            doc = self.alice.clicks_a_link(url)
            links = [("/work/","/media/images/work.png"), ("/us/","/media/images/us.png"), ("/play/", "/media/images/play.png")]
            navigation = doc.find(id="navigation")
            displayed_links = navigation.findAll("a")
            for href, src in links:
                if href != url:
                    alice.sees_a_link(navigation, href, src)
            # see links to all three sections except to the current page
            current_page_is_linked = False
            for link in displayed_links:
                self.failUnless(url not in link["href"], "%s should not be a link on its own page" % url)
        
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
        # see the initial conversation, sprint cycle, and approval cycle portions of the project diagram
        initial_conversation = doc.find(id="initial_conversation")
        self.failUnless(initial_conversation, "Could not find %s" % initial_conversation)
        sprint_cycle = doc.find(id="sprint_cycle")
        self.failUnless(sprint_cycle, "Could not find %s" % sprint_cycle)
        approval_cycle = doc.find(id="approval_cycle")
        self.failUnless(approval_cycle, "Could not find %s" % approval_cycle)
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
        mug_shot = doc.find(id="mug_shot")
        self.failUnless(mug_shot, "Could not find %s" % mug_shot)
        personal_info = doc.find(id="personal_info")
        self.failUnless(personal_info, "Could not find %s" % personal_info)
        experience = doc.find(id="experience")
        self.failUnless(experience, "Could not find %s" % experience)
        personality = doc.find(id="personality")
        self.failUnless(personality, "Could not find %s" % personality)
        hobbies = doc.find(id="hobbies")
        self.failUnless(hobbies, "Could not find %s" % hobbies)
        # see the name, email, and favorite bribe in the personal info section
        name = doc.find(id="personal_info").find(id="name")
        self.failUnless(name, "Could not find %s" % name)
        email = doc.find(id="personal_info").find(id="contact_email")
        self.failUnless(email, "Could not find %s" % email)
        favorite_bribe = doc.find(id="personal_info").find(id="favorite_bribe")
        self.failUnless(favorite_bribe, "Could not find %s" % favorite_bribe)
        # see the languages, skills, and finished projects in the experience div
        languages = doc.find(id="experience").find(id="languages")
        self.failUnless(languages, "Could not find %s" % languages)
        skills = doc.find(id="experience").find(id="skills")
        self.failUnless(skills, "Could not find %s" % skills)
        finished_projects = doc.find(id="experience").find(id="finished_projects")
        self.failUnless(finished_projects, "Could not find %s" % finished_projects)

    def test_play_page(self):
        """ Alice goes to www.emlprime.com and clicks the link to the play page

        she should...
        """
        alice = self.alice
        # see the play page displayed
        templates_used = ["play.html"]
        doc = alice.clicks_a_link("/play/", templates_used=templates_used)
        # see the game background and the four colors
        green = doc.find(id="game").find(id="green")
        self.failUnless(green, "Could not find green")
        red = doc.find(id="game").find(id="red")
        self.failUnless(red, "Could not find red")
        blue = doc.find(id="game").find(id="blue")
        self.failUnless(blue, "Could not find blue")
        yellow = doc.find(id="game").find(id="yellow")
        self.failUnless(yellow, "Could not find yellow")
        response = alice.client.get("/play/get_answer_key/")
        displayed_list = simplejson.loads(response.content)

        self.failUnlessEqual(type(displayed_list), list)
        self.failUnlessEqual(len(displayed_list), 50)
