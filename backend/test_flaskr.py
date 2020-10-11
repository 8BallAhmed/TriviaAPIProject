import os
import unittest
import json

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_path = "postgres://postgres:password@127.0.0.1:5432/" + self.database_name
        setup_db(self.app, self.database_path)

    def tearDown(self):
        pass

        #### GET REQUESTS ###

    def test_getQuestions(self):  # SUCCESS WITH QUESTIONS
        res = self.client().get('/questions')
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(responseData['success'], True)
        self.assertTrue(responseData['questions'])
        self.assertTrue(responseData['total_questions'])
        self.assertTrue(responseData['categories'])

    def test_getQuestionsPage(self):  # SUCCESS, BUT NO QUESTIONS
        res = self.client().get('/questions?page=1000')
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(responseData['success'], True)
        self.assertFalse(responseData['questions'])
        self.assertFalse(responseData['total_questions'])
        self.assertTrue(responseData['categories'])

    def test_getCategories(self):  # SUCCESS, CATEGORIES
        res = self.client().get('/categories')
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(responseData['success'], True)
        self.assertTrue(responseData['categories'])

    def test_getCategoriesFAIL(self):  # FAILURE, CATEGORIES
        res = self.client().post('/categories')
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(responseData['success'], False)

    def test_Q_ByCategory(self):  # SUCCESS, QUESTIONS OF CATEGORY 1
        res = self.client().get('/categories/1/questions')
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(responseData['success'], True)
        self.assertTrue(responseData['questions'])
        self.assertTrue(responseData['total_questions'])
        self.assertTrue(responseData['current_category'])

    def test_Q_ByCategoryFAIL(self):  # FAIL, QUESTIONS OF NON-EXISTENT CATEGORY
        res = self.client().get('/categories/9/questions')
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(responseData['success'], False)

        ### POST REQUESTS ###

    def test_postQuestions(self):  # INSERTING QUESTION INTO DATABASE, SUCCESS
        res = self.client().post('/questions',
                                 json={'question': 'Who is the 40th POTUS?', 'answer': 'Ronald Reagan', 'difficulty': 3, 'category': 4})
        self.assertEqual(res.status_code, 200)
        responseData = json.loads(res.data)
        q = Question.query.filter(
            Question.question == 'Who is the 40th POTUS?').one_or_none()
        self.assertEqual(responseData['success'], True)
        self.assertEqual(q.question, 'Who is the 40th POTUS?')
        self.assertEqual(q.answer, 'Ronald Reagan')
        self.assertEqual(q.difficulty, 3)
        self.assertEqual(q.category, 4)

    # INSERTING QUESTION INTO DATABASE, FAILURE: 400 BAD REQUEST
    def test_postQuestionsFAIL(self):
        res = self.client().post('/questions',
                                 json={'question': 'Who is the 41th POTUS?'})
        self.assertEqual(res.status_code, 400)
        responseData = json.loads(res.data)
        self.assertEqual(responseData['success'], False)

    # DELETE REQUESTS

    # SUCCESSFUL QUESTION DELETION, CHANGE ID TO AN EXISTENT ID IN THE DB TO RUN TEST
    def test_deleteQuestion(self):
        res = self.client().delete('/questions/21')
        self.assertEqual(res.status_code, 200)
        responseData = json.loads(res.data)
        self.assertEqual(responseData['success'], True)
        self.assertEqual(Question.query.get(17), None)

    # FAILED QUESTION DELETION, QUESTION NOT FOUND
    def test_deleteQuestionFAIL(self):
        res = self.client().delete('/questions/10000')
        self.assertEqual(res.status_code, 422)
        responseData = json.loads(res.data)
        self.assertEqual(responseData['success'], False)
        self.assertEqual(Question.query.get(10000), None)

        # QUIZ TEST

    def test_quiz(self):
        res = self.client().post(
            '/quizzes', json={'quiz_category': {'type': 'Science', 'id': 1}, 'previous_questions': [17, 18, 19]})
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(responseData['success'], True)
        self.assertTrue(responseData['question'])

    def test_quizFAIL(self):
        res = self.client().post(
            '/quizzes', json={'quiz_category': {'type': 'Politics', 'id': 8}, 'previous_questions': [17, 18, 19]})
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(responseData['success'], False)

    def test_search(self):
        res = self.client().post('/questionSearch', json={'searchTerm': 'Tom'})
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(responseData['success'], True)
        self.assertTrue(responseData['questions'])
        self.assertTrue(responseData['total_questions'])

    def test_searchFAIL(self):
        res = self.client().patch('/questionSearch',
                                  json={'searchTerm': 'Tom'})
        responseData = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(responseData['success'], False)


if __name__ == '__main__':
    unittest.main()
