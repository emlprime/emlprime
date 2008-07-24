from emlprime.common.tests import CommonTestCase

from django.core import management
from django.conf import settings

class TestStory(CommonTestCase):
    def setUp(self):
        CommonTestCase.setUp(self)

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
        # see the navigation links
        work = doc.find(src="/media/images/work.png")
        self.failUnless(work, "Could not find %s" % work.png)
        work_link = doc.find(id="navigation").find(href="/work/")
        self.failUnless(work_link, "Could not find link to %s" % work)
        us = doc.find(src="/media/images/us.png")
        self.failUnless(us, "Could not find %s" % us.png)
        us_link = doc.find(id="navigation").find(href="/us/")
        self.failUnless(us_link, "Could not find link to %s" % us)
        play = doc.find(src="/media/images/play.png")
        self.failUnless(play, "Could not find %s" % play.png)
        play_link = doc.find(id="navigation").find(href="/play/")
        self.failUnless(play_link, "Could not find link to %s" % play)
        # see the mission statement and work, us, and play snippets
        mission_statement = doc.find(id="mission_statement")
        self.failUnless(mission_statement, "Could not find %s" % mission_statement)
        work_snippet = doc.find(id="work_snippet")
        self.failUnless(work_snippet, "Could not find %s" % work_snippet)
        us_snippet = doc.find(id="us_snippet")
        self.failUnless(us_snippet, "Could not find %s" % us_snippet)
        play_snippet = doc.find(id="play_snippet")
        self.failUnless(play_snippet, "Could not find %s" % play_snippet)
        # see the footer with email and phone from settings and the current year copyright
        email = doc.find(id="footer").find(id="email")
        self.failUnless(email, "Could not find email")
        self.failUnlessEqual(email.a.string, settings.FOOTER_DATA["email"])
        phone_number = doc.find(id="footer").find(id="phone_number")
        self.failUnless(phone_number, "Could not find phone_number")
        self.failUnlessEqual(phone_number.p.string, settings.FOOTER_DATA["phone_number"])
        copyright = doc.find(id="footer").find(id="copyright")
        self.failUnless(copyright, "Could not find play_snippet")
        self.failUnlessEqual(copyright.p.string, settings.FOOTER_DATA["copyright"])


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
        self.alice.sees_a_submit_button(doc, "project")
        self.alice.submits_a_form(doc, "project", {'name':'test', 'email':'test@emlprime.com', 'description':'test project'})
        self.failUnlessEqual(Project.objects.get().name, 'test')

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
        role = doc.find(id="role")
        self.failUnless(role, "Could not find %s" % role)
        personality = doc.find(id="personality")
        self.failUnless(personality, "Could not find %s" % personality)
        hobbies = doc.find(id="hobbies")
        self.failUnless(hobbies, "Could not find %s" % hobbies)
        # see the name, email, and favorite bribe in the personal info section
        name = doc.find(id="personal_info").find(id="name")
        self.failUnless(name, "Could not find %s" % name)
        email = doc.find(id="personal_info").find(id="email")
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
        # see the roles outlined in the role div
        testing = doc.find(id="role").find(id="testing")
        self.failUnless(testing, "Could not find %s" % testing)
        design = doc.find(id="role").find(id="design")
        self.failUnless(design, "Could not find %s" % design)
        customer_relations = doc.find(id="role").find(id="customer_relations")
        self.failUnless(customer_relations, "Could not find %s" % customer_relations)
        coding = doc.find(id="role").find(id="coding")
        self.failUnless(coding, "Could not find %s" % coding)
        communication = doc.find(id="role").find(id="communication")
        self.failUnless(communication, "Could not find %s" % communication)

