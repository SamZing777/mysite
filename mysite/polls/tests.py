import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from.models import Question


class QuestionModelTests(TestCase):
    
    # returns False for questions whos publication date is greater than 1
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    # returns False for questions whos publication date is greater than 1
        
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        
    
def create_question(question_text, days):
    
    """
        Create question with given question text and publish the given number of days
        offset to now (negative for questions published in the past, positive for 
        questions that have yet to be published).
    """
    
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        
        # display message if no question exist
        
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available.", False)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_past_question(self):
        
        # questions with publication date in the past are displayed on the index page
        
        create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])
        
    def test_future_question(self):
        
        # question with publication date are not displayed on the index page
        
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('index'))
        self.assertContains(response, "No polls are available.", False)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    
class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        
        # detail view of test case of question with a publication date in future returns 404
        
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('detail', args=(future_question.id,))
        response = self.client.get(url)
        self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        
        # detail view for a question with a published date in the past displays the question's text
        
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
