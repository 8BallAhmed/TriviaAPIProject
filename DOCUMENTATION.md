This is the official Documentation for Trivia API, an API.

This API Contains the following:

1- Categories: A List of Categories, under which questions exist.

2- Questions: A List of Questions, which exist under a specific category


The only methods this API accepts are the following: ['GET', 'POST', 'DELETE']


GET is used to fetch questions, categories, or questions which fall under a specific category.
DELETE is used to delete a specific question from the Database.
POST is used to Search for questions, add questions into the database, and fetch one question from a specific endpoint that was designed for Trivia quizzes.

Requests in this documentation are ordered by method:

		1-GET
		2-POST
		3-DELETE

Each endpoint is showcased with detail to what it receives, and what it returns when it gets a specific request. The requests are demonstrated first,
then the response is shown.

In case of an error happening, the endpoint will return an object with the following keys:

		1-'success': Evaluates to false
		2-'error-message': describes what error occured, and why
		3-'status-code': returns the status code of the error, which can be one of the following: [400, 404, 405, 422, 500]



*** GET END POINTS ***




____________________________________________________________________________________________________________________________________________



GET '/categories'
	- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

	- Request Arguments: None

	- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

	- Returns a key 'success', which evaluates to True or False depending on the success of the GET Operation 

	-Examples:

		[ GET '/categories' ]



===============================================================


{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

===============================================================




____________________________________________________________________________________________________________________________________________



GET '/questions'
	-Fetches a dictionary of Categories, identical to the one in /categories

	-Fetches a list, containing 10 dictionaries maximum (Paginated, each page has 10 questions). Each dictionary represents a question. Contains the following data:
			
			1- 'id': Question ID
			2- 'question': The question itself
			3- 'answer': The answer for the question
			4- 'difficulty': Difficulty of the question, range(1:5)
			5- 'category': Category ID. You can use the category dictionary to identify which category the question falls under.

	-Fetches a success Key, which evaluates to True or False depending on the success of the request.

	-Fetches a key 'total_questions', which lists the number of questions on the current page.

	-Fetches a key 'current_category', which specifies which category your questions fall under, 'all' for all categories.

	-Request Arguments: page
			
			1- page, example: '/questions?page2'

				Returns a list of 10 questions, at max. Questions are paginated, with every 10 questions making up a page.

	-Examples:

			[ GET '/questions' ]
				


===============================================================

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "all", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
]
  "success": true, 
  "total_questions": 2
}
			



===============================================================


____________________________________________________________________________________________________________________________________________



GET '/categories/<int:id>/questions

		-Identical to questions, but fetches questions under a specific category. Questions are not paginated.
		
		-Examples:

			[ GET '/categories/2/questions' ]



===============================================================




{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}



===============================================================



*** DELETE END POINTS***


____________________________________________________________________________________________________________________________________________



DELETE '/questions/<int:id?/

		-Receives Integer ID, deletes the question with the specified ID.

		-Returns a JSON object as a response, with key 'success' evaluating to true if the deletion was successful.


		-Examples:
			
				[ DELETE '/questions/3' ]:



===============================================================


{
   'success': true
}

===============================================================

*** POST END POINTS***
____________________________________________________________________________________________________________________________________________



POST '/questions'
	
		-Receives a JSON object with the following keys:

			1-'question': String, contains the question to be added
			2-'answer': String, contains the answer to be added
			3-'difficulty': Integer, contains the question's difficulty, ranging from 1 to 5
			4-'category': Integer, contains the ID of the category under which the question belongs.	


	 	-Returns a JSON object as a response, with key 'success' evaluating to true if the deletion was successful.


		-Examples:
			
				[ POST'/questions/' ]

	REQUEST BODY:

		{
		   'question': 'How many planets are there in the solar system?',
		   'answer': 8,
		   'difficulty': 2,
		   'category': 1, (1 is Science)
		}



===============================================================


{
   'success': true
}

===============================================================



____________________________________________________________________________________________________________________________________________




POST '/questionSearch'



		-Receives a JSON object with the following keys:

			1-'searchTerm': String, contains the phrase to be searched for


	 	-Returns a JSON object as a response, containing the questions which meet the search criteria, their quantity, and a 'success' key evaluating to true if the search was 		 successful




		-Examples:
			
				[ POST'/questionSearch' ]


		REQUEST BODY:

		{
		   'searchTerm': 'Maya Angelou',
		}



===============================================================


{
   'success': true,
   'questions': [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
],
   'total_questions': 1 
}

===============================================================



____________________________________________________________________________________________________________________________________________



POST '/quizzes'



		-Receives a JSON object with the following keys:

			1-'quiz_category': JSON Object with keys 'type' containing the type of the category, and 'id' containing its ID, contains the phrase to be searched for.
			2-'previous_questions': Array, containing IDs of previous questions.

		-Returns a JSON object with two values:

			1- 'success': Evaluates to true if the request was successful.
			2- 'question': returns one question, under the specific category which was sent with the request. If there are no questions remaining, it returns false. 
				***[previous_questions is checked before sending a question as a response, to make sure that said question is not one which was asked before.]***
			     	       


		-Examples:
			
				[ POST'/quizzes' ]


		REQUEST BODY:

		{
		   'quiz_category': {'type': 'Science', 'id': 1},
		   'previous_questions': [2, 3, 4]
		}




===============================================================


{
   'success': true,
   'questions: {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
}

===============================================================





*** END OF DOCUMENTATION ***
	