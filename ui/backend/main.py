import os
import json

from pathlib import Path
from typing import List
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
# from models import db, Exam, Question

from ml_models import ExamML
from agent.main import evaluate

load_dotenv()
# MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
EVALUATION_FILE_PATH = (Path(__file__).resolve().parent.parent.parent / "data/exam_evaluation.json").resolve()


with open("exam_marking_schema.json", "r") as file:
    json_data = json.load(file)
    EXAM_MARKING_SCHEME = json_data.get("exam_marking_schema", [])


def create_evaluation_file(exam_ml: ExamML,
                           questions_data,
                           exam_marking_scheme:List[List[List]]):
    assert exam_ml.number_of_questions == len(questions_data) == len(exam_marking_scheme), "Length of questions and marking scheme data doesn't match"
    exam_obj = {
        "subject": exam_ml.course_name,
        "number-of-questions": exam_ml.number_of_questions,
        "questions-schema": []
    }

    for i in range(exam_ml.number_of_questions):
        question_data = questions_data[i]

        question = question_data.get("text")
        total_marks = question_data.get("marks")
        relevant_theory = question_data.get("related_theory")
        student_answer = question_data.get("student_answer")
        marking_scheme = exam_marking_scheme[i]

        questions_obj = {
            "question": question,
            "schema": marking_scheme,
            "total-score": total_marks,
            "relevant-theory": relevant_theory,
            "student-answer": student_answer
        }

        exam_obj["questions-schema"].append(questions_obj)

    with open(EVALUATION_FILE_PATH, "w") as file:
        json.dump(exam_obj, file)


def run_evaluation_script():
    evaluate()


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'BTP'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{MYSQL_ROOT_PASSWORD}@localhost/btp'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route('/exams', methods=['POST'])
def create_exam():
    data = request.get_json()
    title = data.get('title')
    duration = data.get('duration')
    description = data.get('description')
    questions_data = data.get('questions', [])

    # exam = Exam(title=title, duration=duration, description=description)
    # db.session.add(exam)
    # db.session.commit()

    # for question_data in questions_data:
    #     question = Question(
    #         exam_id=exam.id,
    #         type=question_data.get('type'),
    #         text=question_data.get('text'),
    #         options=",".join(question_data.get('options', [])),
    #         student_answer=question_data.get('student_answer'),
    #         related_theory=question_data.get('related_theory'),
    #         marks=question_data.get('marks')
    #     )
    #     db.session.add(question)
    # db.session.commit()

    exam_ml = ExamML(title, len(questions_data))
    create_evaluation_file(exam_ml, questions_data, EXAM_MARKING_SCHEME)
    evaluate()

    return jsonify({"message": "Exam created and evaluated successfully"}), 201

@app.route('/exams', methods=['GET'])
def get_exams():
    # exams = Exam.query.all()
    # exams_data = []
    # for exam in exams:
    #     questions = Question.query.filter_by(exam_id=exam.id).all()
    #     questions_data = [
    #         {
    #             "id": question.id,
    #             "type": question.type,
    #             "text": question.text,
    #             "options": question.options.split(',') if question.options else [],
    #             "student_answer": question.student_answer,
    #             "related_theory": question.related_theory,
    #             "marks": question.marks
    #         } for question in questions
    #     ]
    #     exams_data.append({
    #         "id": exam.id,
    #         "title": exam.title,
    #         "duration": exam.duration,
    #         "description": exam.description,
    #         "questions": questions_data
    #     })
    # return jsonify(exams_data), 200

    return jsonify({"message": "Fetching exams..."}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
