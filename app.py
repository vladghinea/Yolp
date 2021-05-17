from flask import Flask, render_template, redirect, request
import os
import data_handler

ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'

ANSWERS_HEADER = ['id','submission_time','vote_number','question_id','message','image']
QUESTIONS_HEADER = ['id','submission_time','view_number','vote_number','title','message','image']



app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_page():
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    questions = questions[::-1]
    return render_template("list.html", questions=questions, q_header=QUESTIONS_HEADER )

@app.route("/question/<question_id>")
def question_page(question_id):
    show_question= {}
    show_answer= []
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    answers = data_handler.get_data(ANSWERS_FILE_PATH)
    for question in questions:
        if question['id'] == question_id:
            show_question = question
    for answer in answers:
        if answer['question_id'] == question_id:
            show_answer.append(answer)
    return render_template("question.html", question=show_question, answers=show_answer ,q_header=QUESTIONS_HEADER )

@app.route("/add-question")
def add_question_page():
    return render_template('add_question.html')




@app.route("/add", methods=['POST'])
def add():
    old_data = data_handler.get_data(QUESTIONS_FILE_PATH)
    new_dict={}
    new_data = request.form
    new_dict['id'] = str(len(old_data) + 1)
    new_dict['submission_time'] = ""
    new_dict['view_number'] = ""
    new_dict['vote_number'] = ""
    for k, v in new_data.items():
        new_dict[k] = v
    old_data.append(new_dict)
    for item in old_data:
        print(item)
    data_handler.write_data(QUESTIONS_FILE_PATH ,old_data, QUESTIONS_HEADER)
    # new_image = request.files['image']
    # new_image.save('./static/images')
    return redirect("/question/{{old_data['id']}}")





if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = "/static/images"
    app.run()

