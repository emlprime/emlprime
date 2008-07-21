from taskmaster.common.tests import CommonTestCase
from taskmaster.story.models import Story
from taskmaster.settings import STORIES_PER_PAGE

from django.core import management

class TestStory(CommonTestCase):
    def setUp(self):
        CommonTestCase.setUp(self)

    def test_createStory(self):
        """ Alice wants to create a new story.

        she should...
        """
        alice = self.alice
        # view the backlog page
        templates_used = ["story/backlog.html", "base.html"]
        doc = alice.clicks_a_link("/story/backlog/", templates_used=templates_used)

        # submit the form no values entered
        doc = alice.submits_a_form(doc, "create")
        alice.sees_a_submit_button(doc, "create")

        # see an error telling them that the name is required
        alice.sees_an_error_message(doc, "name: * This field is required.")

        # submit the form with just a name
        minimal_data = {"name": "Alice does some...thing"}
        alice.submits_a_form(doc, "create", minimal_data, verbose=False)

        # see the story display with the name and a point value of 1 as well as a delete link
        doc = alice.clicks_a_link("/story/backlog/")
        minimal_story = Story.objects.get(name = minimal_data["name"])
        story_card = doc.find(id=minimal_story.get_css_id())
        
        self.verify_story_form(
            minimal_story,
            story_card,
            minimal_data["name"],
            "",
            minimal_story.get_absolute_url()
            )

        # submit the form with all values filled in
        maximal_data = {"name": "Take over the world", "description": "1. Collect underpants.\n2....\n3.World Domination!"}
        alice.submits_a_form(doc, "create", maximal_data, verbose=False)
        
        # see the story display with all values matching those that were filled in
        doc = alice.clicks_a_link("/story/backlog/")
        maximal_story = Story.objects.get(name = maximal_data["name"])
        story_card = doc.find(id=maximal_story.get_css_id())
        self.verify_story_form(
            maximal_story,
            story_card,
            maximal_data["name"],
            maximal_data["description"],
            maximal_story.get_absolute_url()
            )

        # submit a change to the maximal story
        change_data = {"name": "Same thing we do every night", "description": "What is that Brain?"}
        detail_change_data = self.build_story_data(maximal_story, change_data)
        alice.submits_a_form(doc, maximal_story.get_css_id(), detail_change_data, verbose=False)
        
        doc = alice.clicks_a_link("/story/backlog/")
        change_story = Story.objects.get(name = change_data["name"])
        story_card = doc.find(id=change_story.get_css_id())
        self.verify_story_form(
            change_story,
            story_card,
            change_data["name"],
            change_data["description"],
            change_story.get_absolute_url()
            )
        
        # see two stories in the backlog
        stories = Story.objects.all().iterator()
        story_to_delete = stories.next()
        story_to_remain = stories.next()

        templates_used = ["story/confirm_delete.html", "base.html"]
        doc = alice.clicks_a_link(story_to_delete.get_absolute_url() + "delete/")
        alice.sees_a_confirm_message(doc, "Are you sure you want to delete '%s'" % minimal_story.name)

        # submit a post to delete one of the stories
        self.failUnlessEqual(Story.objects.count(), 2)
        form_css_id = "delete_" + story_to_delete.get_css_id()
        alice.submits_a_form(doc, form_css_id, verbose=False)

        # see the deleted story gone
        stories = Story.objects.all()
        self.failUnlessEqual(stories.count(), 1)
        self.failUnlessEqual(story_to_remain, stories[0])

    def test_large_set(self):
        """ Alice wants to create a large set of stories

        She should...
        """
        alice = self.alice
        # submit the create for about 50 times
        doc = alice.clicks_a_link("/story/backlog/")
        self.generate_stories(doc, 50)

        doc = alice.clicks_a_link("/story/backlog/")

        # verify that there are 50/STORIES_PER_PAGE - 2 (first and last) pages available and STORIES_PER_PAGE stories visible
        story_count = Story.objects.count()
        
        page_count = (story_count / STORIES_PER_PAGE)
        # -2 to account for first and last
        self.failUnlessEqual(len(doc.find("ul", "page_numbers").findAll("a")) - 2 , page_count)
        # -1 to account for the creation form
        self.failUnlessEqual(len(doc.findAll("div", "story")) - 1 , STORIES_PER_PAGE)

    def test_prioritization(self):
        """ Alice has stories in the order 1,2,3,4 and wants them in the order 3, 1, 4, 2

        She should
        """
        doc = self.alice.clicks_a_link("/story/backlog/")
        self.generate_stories(doc, 4)
        story_1 = Story.objects.get(id=1)
        story_2 = Story.objects.get(id=2)
        story_3 = Story.objects.get(id=3)
        story_4 = Story.objects.get(id=4)
        doc = self.alice.clicks_a_link("/story/backlog/")
        """
        see all four of her cards on the page in the 1, 2, 3, 4 order
        see an insert marker after 4 that says "Click [Insert at Marker] to insert a story here"
        see [Move Insert Point Here] button before 1, between 1 and 2, 2 and 3, 4 and 4
        """
        order_test = ['m', 1, 'm', 2, 'm', 3, 'm', 4, 'i']
        self.verify_order(order_test)
        """
        see that clicking the [Move Insert Point Here] between 1 and 2 moves the insert position between 2 and 3.
        see that the insert position after 4 now says [Move Insert Point Here]
        """
        self.alice.clicks_a_link("/story/backlog/set_insertion_point/2/")
        
        order_test = ['m', 1, 'i', 2, 'm', 3, 'm', 4, 'm']
        self.verify_order(order_test)
        
        # click the [Insert at Marker] button on Story 4
        # see the order become 1, 4, 2, 3
        # see the "Click [Insert at Marker] to insert a story here" between the 4 and 2 card
        self.alice.submits_a_form(doc, "%s_insert_at_marker" % story_4.get_css_id())
        order_test = ['m', 1, 'm', 4, 'i', 2, 'm', 3, 'm']
        self.verify_order(order_test)

        # see that clicking the [Move Insert Point Here] before 1 moves the insert position before 1
        self.alice.clicks_a_link("/story/backlog/set_insertion_point/1/")
        order_test = ['i', 1, 'm', 4, 'm', 2, 'm', 3, 'm']
        self.verify_order(order_test)

        # see that clicking [Insert at Marker] moves the stories to 3, 1, 4, 2
        self.alice.submits_a_form(doc, "%s_insert_at_marker" % story_3.get_css_id())
        order_test = ['m', 3, 'i', 1, 'm', 4, 'm', 2, 'm']
        self.verify_order(order_test)
        
        # click the [Move Insert Point Here] marker after Story 2
        # see the "Click [Insert at Marker] to insert a story here" after Story 2
        self.alice.clicks_a_link("/story/backlog/set_insertion_point/")
        order_test = ['m', 3, 'm', 1, 'm', 4, 'm', 2, 'i']
        self.verify_order(order_test)

        # see that clicking [Insert at Marker] on 2 doesn't move anything
        self.alice.submits_a_form(doc, "%s_insert_at_marker" % story_2.get_css_id())
        order_test = ['m', 3, 'm', 1, 'm', 4, 'm', 2, 'i']
        self.verify_order(order_test)

    def test_create_a_sprint(self):
        """ Alice wants to create_a_sprint
    
        She should...
        """
        self.generate_stories(self.alice.clicks_a_link("/story/backlog/"), 10)
        [s.assign() for s in Story.objects.backlog()[:2]]
        
        # click the "create a sprint link" from the backlog
        doc = self.alice.clicks_a_link("/story/sprint/create/")
        
        # submit a blank sprint form and see an error requiring a non-unique name and date range
        errors = {"name": "This field is required.", "start_date": "This field is required."}
        doc = self.alice.submits_a_form(doc, "create", errors=errors)

        # submit a valid sprint form
        values = {"name": "Doing stuff", "start_date": "2008-01-01", "duration_in_weeks": "2"}
        doc = self.alice.submits_a_form(doc, "create", values)

        # see the sprint creation page with two columns
        backlog_rows = self.scrape_list_for_rows(doc, "backlog")
        sprint_rows = self.scrape_list_for_rows(doc, "sprint")
        
        self.failUnless(backlog_rows, "There was no visible backlog column")
        self.failUnless(sprint_rows, "There was no visible sprint column")

        # one backlog column with all the available unassigned stories
        self.failUnlessEqual(len(backlog_rows), Story.objects.backlog().count())

        # one for the sprint with all of the available assigned stories
        self.failUnlessEqual(len(sprint_rows), Story.objects.sprint().count())

        # An input for total sprint points and average daily velocity
        self.failUnless(doc.find(id="total_sprint_points"), "Could not find total_sprint_points in :%s" % doc)
        self.failUnless(doc.find(id="average_daily_velocity"), "Could not find average_daily_velocity in :%s" % doc)

        # the sprint rows should be in ascending priority order
        highest_priority = 0
        for row in sprint_rows:
            story_id = int(row.div["id"].split("_")[1])
            story = Story.objects.get(id=story_id)
            self.failUnless(story.priority >= highest_priority, "The stories are out of order")
            highest_priority = story.priority

    def test_assign_a_story_to_the_sprint(self):
        """ Alice wants to assign a story to the current sprint from the backlog

        She should...
        """
        self.generate_stories(self.alice.clicks_a_link("/story/backlog/"), 10)

        # click the "create a sprint link" from the backlog
        doc = self.alice.clicks_a_link("/story/sprint/create/")
        
        # submit a valid sprint form
        values = {"name": "Doing stuff", "start_date": "2008-01-01", "duration_in_weeks": "2"}
        self.alice.submits_a_form(doc, "create", values)

        # click the assign sprint link from the backlog page
        doc = self.alice.clicks_a_link("/story/backlog/")
        assign_sprint_link = doc.find(id="assign_sprint_link")
        self.failUnless(assign_sprint_link, "Could not find a link to assign the sprint in %s" % doc)
        
        doc = self.alice.clicks_a_link(assign_sprint_link["href"])

        # see the sprint assignment page with two columns
        story_to_assign = Story.objects.backlog()[0]
        backlog = doc.find(id="backlog")
        backlog_rows = self.scrape_list_for_rows(doc, "backlog")
        
        self.failUnless(backlog_rows, "There was no visible backlog column")
        story_row = backlog.find(id=story_to_assign.get_css_id())
        self.failUnless(story_row, "Selected story was not found in the backlog: %s" % backlog)
        
        # click on the first story's assign link to make it the current story
        assign_link = story_row.find("a", "assign_link")
        self.failUnless(assign_link, "Selected story did not have an assign link: %s" % story_row)
        doc = self.alice.clicks_a_link(assign_link["href"])
        
        # see the story she clicked show up as the current story in a special div
        current_story = doc.find(id="current_story")
        self.failUnless(current_story, "Could not find a current_story in the document: %s" % doc)
        self.failUnless(current_story.find(id=story_to_assign.get_css_id()), "The selected story was not the current story")

        # press the [cancel] button to see the story back in the backlog
        cancel_link = doc.find(id="cancel_assignment")
        self.failUnless(cancel_link, "Could not find a cancel button in the document: %s" % doc)
        doc = self.alice.clicks_a_link(cancel_link["href"])
        backlog = doc.find(id="backlog")
        self.failUnless(backlog.find(id=story_to_assign.get_css_id()), "Selected story was not found in the backlog: %s" % backlog)
        
        # click the first story again and then click [add to sprint] to add it to the sprint
        doc = self.alice.clicks_a_link(assign_link["href"])
        assign_form = doc.find(id="assign_form")
        self.failUnless(assign_form, "Could not find an assignment form in the document: %s" % doc)
        add_to_sprint_button = assign_form.find(id="add_to_sprint")
        self.failUnless(add_to_sprint_button, "Could not find an [add to sprint] button in the assign form: %s" % assign_form)
        doc = self.alice.submits_a_form(doc, "assign")
        # see the story in the sprint area
        sprint = doc.find(id="sprint")
        self.failUnless(sprint, "Could not find a sprint column in the document: %s" % doc)
        self.failUnless(sprint.find(id=story_to_assign.get_css_id()), "Selected story was not found in the sprint: %s" % sprint)

    def verify_order(self, order_test):
        doc = self.alice.clicks_a_link("/story/backlog/")
        story_list = self.scrape_story_list(doc)
        def build_order_list(story_list):
            order_display = []
            for element in story_list:
                token = None
                if "Move Insert Point Here" in str(element):
                    token = "m"
                if "Click [Insert at Marker] to insert a story here" in str(element):
                    token = "i"
                if not token:
                    token = int(element.find("div")["id"].split("_")[1])
                order_display.append(token)
            return order_display
            
        self.failUnlessEqual(build_order_list(story_list), order_test)
        
    def generate_stories(self, doc, number_of_stories=1):
        """ generate number_of_stories stories
        """
        data_template = {"name": "Story #%d", "description": "Description of story #%d"}
        for i in xrange(number_of_stories):
            data = dict([(key, value % (i+1)) for key, value in data_template.items()])
            self.alice.submits_a_form(doc, "create", data, follow_redirects=False)
        
    def build_story_data(self, story, data={}):
        """ scrape data from the HTML
        """
        css_id = story.get_css_id()
        new_data = {}
        for key, value in data.items():
            new_data["%s-%s" % (css_id, key)] = value
        return new_data

    def scrape_story_list(self, doc):
        """ given a doc, scrape the list of stories and insertion points
        """
        story_list = doc.find(id="story_list").findAll("li")
        return story_list
                

    def scrape_list_for_rows(self, doc, css_id):
        """ given a doc, scrape the list
        """
        return doc.find(id=css_id).findAll("li")

    def verify_story_form(self, story, story_card, name, description, absolute_url):
        """ Verify that the story details are being displayed properly in the detail form

        This is a helper function that will scrape the values from the form in the HTML
        """
        alice = self.alice
        detail_form = story_card.find("form")
        # verify that the detail form submits to the correct url
        self.failUnlessEqual(
            detail_form['action'],
            absolute_url,
            "The action for the detail form does not submit to (%s)" % absolute_url
            )
        
        # find the basic display fields
        prefix = story.get_css_id()
        alice.sees_an_input(story_card, "%s-name" % prefix, name)
        alice.sees_a_textarea(story_card, "%s-description" % prefix, description)

        # find the delete link
        alice.sees_a_delete_button(story_card, absolute_url)
        

