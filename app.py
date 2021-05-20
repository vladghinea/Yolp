from flask import Flask, render_template, redirect, request, url_for
import os
import data_handler
import myutility

ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'

ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'answers', 'image']




app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = '/home/keitkalon/projects/web/ask-mate-1-python-keitkalon/static/images/uploads'
app.config['ALLOWED_IMAGE_EXTENSION'] = ['PNG', 'JPG']

@app.route("/")
@app.route("/list")
def list_page():
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    if request.args:
        order = request.args['order']
        questions = myutility.sorting(order, questions)
        print(questions)
        if 'type' in request.args.keys():
            if request.args['type'] == 'desc':
                questions = questions[::-1]

    return render_template("list.html", questions=questions, q_header=QUESTIONS_HEADER)



@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    answers = data_handler.get_data(ANSWERS_FILE_PATH)
    new_answers=[]
    for question in questions:
        if question['id'] == question_id:
            for answer in answers:
                if answer['question_id'] != question_id:
                    new_answers.append(answer)
                    print("intru in answers si stergem pe aia de jos")

            for answer in new_answers:
                if answer['question_id'] > question_id:
                    answer['question_id'] = int(answer['question_id']) - 1
                    print('intru in answers si modificam q_id-ul')
            questions.remove(question)
    data_handler.write_data(QUESTIONS_FILE_PATH, questions, QUESTIONS_HEADER)
    data_handler.write_data(ANSWERS_FILE_PATH, new_answers, ANSWERS_HEADER)
    return redirect("/list")


@app.route('/question/<question_id>/edit', methods=['GET','POST'])
def edit_question_page(question_id):
    if request.method == 'POST':
        questions= data_handler.get_data(QUESTIONS_FILE_PATH)
        edit_question = request.form
        new_questions = myutility.edit_question_and_answer(edit_question,questions,'q',question_id)
        data_handler.write_data(QUESTIONS_FILE_PATH, new_questions, QUESTIONS_HEADER)
        if request.files:
            image = request.files['image']
            if image.filename == '':
                print('image must have a name')
                return redirect(f'/question/{question_id}')
            if not myutility.allowed_image_files(image.filename, app.config['ALLOWED_IMAGE_EXTENSION']):
                print("file doesn't have the right extension")
                return redirect(f'/question/{question_id}')

            new_questions[int(question_id)-1]['image']= image.filename
            data_handler.write_data(QUESTIONS_FILE_PATH, new_questions, QUESTIONS_HEADER)
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
        return redirect(f'/question/{question_id}')

    elif request.method == 'GET':
        questions= data_handler.get_data(QUESTIONS_FILE_PATH)
        for question in questions:
            if question['id'] == question_id:
                return render_template('edit_question.html', question=question, question_id=question_id )


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
        dict_answers = myutility.init_answer_and_question(new_answer, answers, "a", question_id)
        show_answer.append(dict_answers)
        answers.append(dict_answers)
        data_handler.write_data(ANSWERS_FILE_PATH, answers, ANSWERS_HEADER)
        return redirect(url_for("question_page", question_id=question_id))

    else:
        for question in questions:
            if question['id'] == question_id:
                question['view_number'] = str(int(question["view_number"]) + 1)

                data_handler.write_data(QUESTIONS_FILE_PATH, questions, QUESTIONS_HEADER)
                show_question = question

        for answer in answers:
            if answer['question_id'] == question_id:
                show_answer.append(answer)
        print(show_question)

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
    if request.files:
        image = request.files['image']

        if image.filename == '':
            print('image must have a name')
            return redirect(f"/question/{new_dict['id']}")

        if not myutility.allowed_image_files( image.filename, app.config['ALLOWED_IMAGE_EXTENSION']):
            print("file doesn't have the right extension")
            return redirect(f"/question/{new_dict['id']}")

        old_data[-1]['image'] = image.filename
        data_handler.write_data(QUESTIONS_FILE_PATH, old_data, QUESTIONS_HEADER)
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
    return redirect(f"/question/{new_dict['id']}")


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer_page(question_id):
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    for question in questions:
        if question['id'] == question_id:
            show_question = question
    return render_template('answer.html', question=show_question)


@app.route('/answer/<answer_id>/delete')
def delete_answer_page(answer_id):
    question_id = 0
    answers = data_handler.get_data(ANSWERS_FILE_PATH)
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer["question_id"]
            answers.remove(answer)
    data_handler.write_data(ANSWERS_FILE_PATH,answers,ANSWERS_HEADER)
    return redirect(f'/question/{question_id}')


@app.route('/add_vote')
def add_vote_page():
    request_args = request.args
    direction = myutility.add_vote(request_args)
    return redirect(direction)



if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = "/static/images"
    app.run()

