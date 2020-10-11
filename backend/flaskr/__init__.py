import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={


        '/questions': {'origins': '*'},
        '/categories': {'origins': '*'},
        '/categories/<int:id>/questions': {'origins': '*'},
        '/questions/<int:id>': {'origins': '*'},
        '/questionSearch': {'origins': '*'},
        '/quizzes': {'origins': '*'},

    })

    @ app.after_request
    def afterReq(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, application/json')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, DELETE')
        return response

    def paginateQuestions(questions, request):
        page = request.args.get('page', 1, type=int)
        startingIndex = (page - 1) * QUESTIONS_PER_PAGE
        endingIndex = startingIndex + QUESTIONS_PER_PAGE
        formattedQuestions = []
        for question in questions:
            formattedQuestions.append(question.format())
        categories = Category.query.order_by(Category.id).all()

        return jsonify({
            'success': True,
            'questions':
            formattedQuestions[startingIndex:endingIndex],
            'total_questions':
            len(formattedQuestions[startingIndex:endingIndex]),
            'categories':
            {category.id: category.type for category in categories},
            'current_category': 'all'}), 200

    # JSON RESPONSE IS SUFFICIENT, NO NEED TO RAISE ERROR, DOCUMENTED
    @ app.route('/questionSearch', methods=['POST'])
    def searchQuestion():
        searchTerm = request.get_json()['searchTerm']
        questions = Question.query.filter(
            Question.question.ilike('%' + searchTerm + '%')).all()
        formattedQuestions = []
        for q in questions:
            formattedQuestions.append(q.format())
        return jsonify({'success': True,
                        'questions': formattedQuestions,
                        'total_questions': len(formattedQuestions)}),  200

    # CHECKED FOR SUCCESS AND FAILURE, DOCUMENTED
    @ app.route('/questions', methods=['POST'])
    def postQuestions():
        try:
            req = request.get_json()
            question = req['question']
            answer = req['answer']
            difficulty = req['difficulty']
            category = req['category']
            question = Question(
                question=question,
                answer=answer,
                category=category, difficulty=difficulty)
            question.insert()
        except:
            abort(400)
        return jsonify({'success': True}), 200

    # CHECKED FOR SUCCESS, FAILURE NOT APPLICABLE, DOCUMENTED
    @ app.route('/questions', methods=['GET'])
    def getQuestions():
        questions = Question.query.all()
        questionsJSON = paginateQuestions(questions, request)
        return questionsJSON

    # CHECKED FOR SUCCESS AND FAILURE, DOCUMENTED
    @ app.route('/questions/<int:id>', methods=['DELETE'])
    def delQuestions(id):
        try:
            question = Question.query.get(id)
            question.delete()
            return jsonify({'success': True}), 200
        except:
            abort(422)

    # CHECKED FOR SUCCESS, FAILURE NOT APPLICABLE, DOCUMENTED
    @ app.route('/categories', methods=['GET'])
    def getCategories():
        categories = Category.query.order_by(Category.id).all()
        formattedCategories = {}
        for category in categories:
            formattedCategories[int(category.id)] = category.type
        return jsonify(
            {
                'success': True,
                'categories': formattedCategories
            }), 200

    def paginateCattedQuestions(questions, id):
        category = None
        try:
            category = Category.query.get(id).type

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions':
                len(Question.query.filter_by(category=id).all()),
                'current_category': category
            }), 200
        except:
            abort(404)

    # CHECKED FOR SUCCESS AND FAILURE, DOCUMENTED
    @ app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def getQuestionsCat(cat_id):
        questions = Question.query.filter_by(category=(cat_id))
        questionsJSON = paginateCattedQuestions(questions, cat_id)
        return questionsJSON

    # RELATED TO FRONT-END, CHECKED FOR SUCCESS AND FAILURE
    @ app.route('/quizzes', methods=['POST'])
    def quizQuestions():
        req = request.get_json()
        quizCategory = req.get('quiz_category')
        previousQuestions = req.get('previous_questions')
        if int(quizCategory['id']) > len(Category.query.all()):
            abort(404)
        questions = None
        if len(Question
               .query
               .filter_by(category=int(quizCategory['id']))
               .all()) == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category=int(quizCategory['id']))

        formattedQuestions = []
        for q in questions:
            if (not(q.id in previousQuestions)):
                formattedQuestions.append(q.format())

        if len(formattedQuestions) == 0:
            return jsonify(
                {'success': True, 'question': False}), 200
        else:
            return jsonify(
                {'success': True, 'question':
                 formattedQuestions[random.randint(
                     0, len(formattedQuestions) - 1)],
                 }), 200

    @ app.errorhandler(404)
    def notFound(error):
        return jsonify(
            {'success': False,
             'error-message': 'Resource not found', 'status-code': 404}), 404

    @ app.errorhandler(405)
    def methodNotAllowed(error):
        return jsonify(
            {'success': False,
             'error-message': 'Method not allowed. Use appropriate method',
             'status-code': 405}), 405

    @ app.errorhandler(400)
    def badRequest(error):
        return jsonify(
            {'success': False,
             'error-message': 'Bad Request.',
             'status-code': 400}), 400

    @ app.errorhandler(500)  # WILL NOT RUN IN DEBUG MODE
    def internalServerError(error):
        return jsonify(
            {'success': False,
             'error-message': 'It\'s not your fault.',
             'status-code': 500}), 500

    @ app.errorhandler(422)
    def unproccessable(error):
        return jsonify(
            {'success': False,
             'error-message':
             'Your request is syntactically correct, but unprocessable',
             'status-code': 422}), 422

    return app
