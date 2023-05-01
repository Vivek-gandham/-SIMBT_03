from flask import Flask, request, jsonify
from random import randint

app = Flask(__name__)

# Sample question bank
questions = {
    "category1": [
        {
            "question": "What is the capital of France?",
            "choices": ["Paris", "Rome", "London"],
            "answer": "Paris"
        },
        {
            "question": "What is the tallest mammal?",
            "choices": ["Elephant", "Giraffe", "Horse"],
            "answer": "Giraffe"
        }
    ],
    "category2": [
        {
            "question": "What is the smallest planet in our solar system?",
            "choices": ["Venus", "Mercury", "Mars"],
            "answer": "Mercury"
        },
        {
            "question": "What is the largest country in the world?",
            "choices": ["Russia", "USA", "China"],
            "answer": "Russia"
        }
    ]
}

# User scores
scores = {}

# Route for getting quiz questions
@app.route('/quiz', methods=['POST'])
def get_quiz():
    category = request.json['category']
    num_questions = request.json['num_questions']
    
    if category not in questions:
        return jsonify({'error': 'Invalid category.'}), 400
    
    if num_questions > len(questions[category]):
        return jsonify({'error': 'Not enough questions in category.'}), 400
    
    # Get random questions from category
    quiz_questions = []
    question_indexes = set()
    while len(quiz_questions) < num_questions:
        index = randint(0, len(questions[category]) - 1)
        if index not in question_indexes:
            question_indexes.add(index)
            quiz_questions.append(questions[category][index])
    
    return jsonify({'questions': quiz_questions})

# Route for submitting quiz answers
@app.route('/submit', methods=['POST'])
def submit_quiz():
    category = request.json['category']
    user_id = request.json['user_id']
    answers = request.json['answers']
    
    if category not in questions:
        return jsonify({'error': 'Invalid category.'}), 400
    
    if user_id not in scores:
        scores[user_id] = {
            'category': category,
            'num_correct': 0,
            'num_total': len(questions[category])
        }
    
    user_score = scores[user_id]
    
    # Calculate score
    for i, answer in enumerate(answers):
        if answer == questions[category][i]['answer']:
            user_score['num_correct'] += 1
    
    return jsonify({'score': user_score['num_correct'], 'total': user_score['num_total']})

# Route for getting leaderboard
@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    sorted_scores = sorted(scores.items(), key=lambda x: x[1]['num_correct'], reverse=True)
    leaderboard = []
    for i, score in enumerate(sorted_scores):
        leaderboard.append({
            'rank': i + 1,
            'user_id': score[0],
            'score': score[1]['num_correct'],
            'total': score[1]['num_total']
        })
    return jsonify({'leaderboard': leaderboard})
