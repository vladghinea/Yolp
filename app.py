from flask import Flask, render_template, redirect, request, url_for
import os
import data_handler
import myutility

ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'

ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_page():
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    questions = questions[::-1]
    return render_template("list.html", questions=questions, q_header=QUESTIONS_HEADER)


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    answers = data_handler.get_data(ANSWERS_FILE_PATH)
    for question in questions:
        if question['id'] == question_id:
            for answer in answers:
                if answer['question_id'] == question_id:
                    answers.remove(answer)
            questions.remove(question)
    return redirect("/list")



@app.route("/question/<question_id>", methods=['GET', 'POST'])
def question_page(question_id):
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    answers = data_handler.get_data(ANSWERS_FILE_PATH)
    show_question = {}
    show_answer = []
    if request.method == "POST":
        for answer in answers:
            if answer['question_id'] == question_id:
                show_answer.append(answer)

        new_answer = request.form
        dict_answers = myutility.init_answer_and_question(new_answer, show_answer, "a", question_id)
        show_answer.append(dict_answers)
        answers.append(dict_answers)
        data_handler.write_data(ANSWERS_FILE_PATH, answers, ANSWERS_HEADER)

        return redirect(url_for("question_page", question_id=question_id))
    else:
        for question in questions:
            if question['id'] == question_id:
                show_question = question

        for answer in answers:
            if answer['question_id'] == question_id:
                show_answer.append(answer)

        return render_template("question.html", question=show_question, answers=show_answer, q_header=QUESTIONS_HEADER)


@app.route("/add-question")
def add_question_page():
    return render_template('add_question.html')


@app.route("/add", methods=['POST'])
def add():
    old_data = data_handler.get_data(QUESTIONS_FILE_PATH)
    new = request.form
    new_dict = myutility.init_answer_and_question(new, old_data, "q")
    old_data.append(new_dict)
    data_handler.write_data(QUESTIONS_FILE_PATH, old_data, QUESTIONS_HEADER)

    return redirect(f"/question/{new_dict['id']}")


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer_page(question_id):
    print("refresh pe pagina new-answer")
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    for question in questions:
        if question['id'] == question_id:
            show_question = question

    return render_template('answer.html', question=show_question)


if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = "/static/images"
    app.run()

