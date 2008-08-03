from emlprime.common.tests import CommonTestCase
from emlprime.static.models import Project

from django.core import mail, management
from django.conf import settings

class TestStatic(CommonTestCase):
    def setUp(self):
        CommonTestCase.setUp(self)

    def test_navigation(self):
        """ Alice visits each page.

        She should...
        """
        urls = ["/", "/work/", "/us/", "/play/"]
        expected_titles = ["work", "us", "play"]
        expected_titles.sort()
        # see all three navigation titles on each page
        for url in urls:
            doc = self.alice.clicks_a_link(url)
            titles = doc.find(id="navigation").findAll("p")
            print """titles:""", 
            
            displayed_titles = [t.string.lower() if t.string else t.a.string.lower() for t in titles]
            displayed_titles.sort()
            self.failUnlessEqual(displayed_titles, expected_titles)
            # see links to all three sections except to the current page
            for title in titles:
                title_string = t.string.lower() if t.string else t.a.string.lower()
                if title_string in url:
                    self.failUnless(not title.find("a"), "%s should not be a link on its own page" % title_string)
                else:
                    self.failUnless(title.find("a"), "%s should have a link on this page: %s" % (title_string, url))

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
        work_link = doc.find(id="navigation").find(href="/work/")
        self.failUnless(work_link, "Could not find link to %s" % work)
        us = doc.find(src="/media/images/us.png")
        us_link = doc.find(id="navigation").find(href="/us/")
        self.failUnless(us_link, "Could not find link to %s" % us)
        play = doc.find(src="/media/images/play.png")
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
        # check that email is sent
#        print "outbox:", mail.outbox[0].subject
#        print "outbox:", mail.outbox[0].message()

    def test_workflow_page(self):
        """ Alice goes to www.emlprime.com/work and clicks on the link to the sample workflow
        
        she should...
        """
        alice = self.alice
        # see the page
        templates_used = ["sample_workflow.html"]
        doc = alice.clicks_a_link("/work/sample_workflow/", templates_used=templates_used)
        # see the divs for the initial stage, sprint cycle, and approval cycle
        initial_stage=doc.find(id="workflow_initial_stage")
        self.failUnless(initial_stage, "could not find initial stage")
        sprint_cycle=doc.find(id="workflow_sprint_cycle")
        self.failUnless(sprint_cycle, "could not find sprint cycle")
        approval_cycle=doc.find(id="workflow_approval_cycle")
        self.failUnless(approval_cycle, "could not find approval cycle")
        # see the great idea, transformation, and initial sprint divs inside the initial stage
        great_idea=doc.find(id="workflow_initial_stage").find(id="great_idea")
        self.failUnless(great_idea, "could not find great_idea")
        transformation=doc.find(id="workflow_initial_stage").find(id="transformation")
        self.failUnless(transformation, "could not find transformation")
        initial_sprint=doc.find(id="workflow_initial_stage").find(id="initial_sprint")
        self.failUnless(initial_sprint, "could not find initial_sprint")
        # see the assign sprint, write tests, write code, update burndown, and present stories inside the sprint cycle
        assign_sprint_tasks=doc.find(id="workflow_sprint_cycle").find(id="assign_sprint_tasks")
        self.failUnless(assign_sprint_tasks, "could not find assign_sprint_tasks")
        write_tests=doc.find(id="workflow_sprint_cycle").find(id="write_tests")
        self.failUnless(write_tests, "could not find write_tests")
        write_code=doc.find(id="workflow_sprint_cycle").find(id="write_code")
        self.failUnless(write_code, "could not find write_code")
        update_burndown=doc.find(id="workflow_sprint_cycle").find(id="update_burndown")
        self.failUnless(update_burndown, "could not find update_burndown")
        present_stories=doc.find(id="workflow_sprint_cycle").find(id="present_stories")
        self.failUnless(present_stories, "could not find present_stories")
        # see the story approval, get paid, add ideas, groom backlog, and design next sprint inside the approval cycle
        story_approval=doc.find(id="workflow_approval_cycle").find(id="story_approval")
        self.failUnless(story_approval, "could not find story_approval")
        get_paid=doc.find(id="workflow_approval_cycle").find(id="get_paid")
        self.failUnless(get_paid, "could not find get_paid")
        add_ideas=doc.find(id="workflow_approval_cycle").find(id="add_ideas")
        self.failUnless(add_ideas, "could not find add_ideas")
        design_next_sprint=doc.find(id="workflow_approval_cycle").find(id="design_next_sprint")
        self.failUnless(design_next_sprint, "could not find design_next_sprint")
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
        
