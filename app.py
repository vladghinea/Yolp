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

@app.route("/question/<question_id>", methods=['GET', 'POST'])
def question_page(question_id):
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    answers = data_handler.get_data(ANSWERS_FILE_PATH)
    show_question = {}
    show_answer = []
    if request.method == "GET":

        for question in questions:
            if question['id'] == question_id:
                show_question = question

        for answer in answers:
            if answer['question_id'] == question_id:
                show_answer.append(answer)


        return render_template("question.html", question=show_question, answers=show_answer ,q_header=QUESTIONS_HEADER )
    else:
        dict_answers= {}
        for ans in show_answer:
            print(ans)

        for question in questions:
            if question['id'] == question_id:
                show_question = question

        for answer in answers:
            if answer['question_id'] == question_id:
                show_answer.append(answer)

        new_answer = request.form


        dict_answers['id']= str(len(show_answer)+1)
        dict_answers['submission_time'] = ""
        dict_answers['vote_number'] = ""
        dict_answers['question_id'] = question_id
        for k, v in new_answer.items():
            dict_answers[k] = v
        dict_answers['image'] = ""
        show_answer.append(dict_answers)
        answers.append(dict_answers)
        data_handler.write_data(ANSWERS_FILE_PATH,answers,ANSWERS_HEADER)

        return render_template("question.html", question=show_question, answers=show_answer, q_header=QUESTIONS_HEADER)

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
    return redirect(f"/question/{new_dict['id']}")

@app.route('/question/<question_id>/new-answer', methods=['GET','POST'])
def answer_page(question_id):
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    for question in questions:
        if question['id'] == question_id:
            show_question= question

    return render_template('answer.html', question=show_question)



if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = "/static/images"
    app.run()

