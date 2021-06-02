from flask import Flask, render_template, redirect, request, url_for
import os
import data_handler
import myutility
import data_manager

ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'

ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']




app = Flask(__name__)

vlad = '/home/vlad/projects/ask-mate-2-python-vladghinea/static/images/uploads/'
lamine = '/home/keitkalon/projects/web/ask-mate-2-python-vladghinea/static/images/uploads'
home = os.path.join(app.root_path, 'static/images/uploads')
app.config['IMAGE_UPLOADS'] = lamine
app.config['ALLOWED_IMAGE_EXTENSION'] = ['PNG', 'JPG', 'JPEG']

@app.route("/")
@app.route("/list")
def list_page():                                                #REFACUT
    questions = data_manager.get_questions()
    if request.args:
        order = request.args['order']
        questions = myutility.sorting(order, questions)
        print(questions)
        if 'type' in request.args.keys():
            if request.args['type'] == 'desc':
                questions = questions[::-1]
    else:
        questions = questions[::-1]
            

    return render_template("list.html", questions=questions, q_header=QUESTIONS_HEADER)



@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    question_id = int(question_id)
    data_manager.delete_question(question_id)
    data_manager.delete_answer(question_id)
    return redirect("/list")


@app.route('/question/<question_id>/edit', methods=['GET','POST'])
def edit_question_page(question_id):
    question_id = int(question_id)
    if request.method == 'POST':
        edit_question = request.form

        image_file = ""
        if request.files:
            image = request.files['image']
            if image.filename == '':
                print('image must have a name')
                return redirect(f'/question/{question_id}')
            if not myutility.allowed_image_files(image.filename, app.config['ALLOWED_IMAGE_EXTENSION']):
                print("file doesn't have the right extension")
                return redirect(f'/question/{question_id}')
            image_file = image.filename
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
        data_manager.edit_question(question_id, edit_question, image_file)

        return redirect(f'/question/{question_id}')

    elif request.method == 'GET':
        questions= data_manager.get_questions()
        for question in questions:
            if question['id'] == question_id:
                return render_template('edit_question.html', question=question, question_id=question_id )


@app.route("/question/<question_id>", methods=['GET', 'POST'])   # REFACUT
def question_page(question_id):
    question_id = int(question_id)
    questions = data_manager.get_questions()
    answers = data_manager.get_answers()
    show_question = {}
    show_answer = []
    if request.method == "POST":

        for answer in answers:

            if answer['question_id'] == question_id:
                show_answer.append(answer)
        new_answer = request.form
        image_filename = ""
        if request.files:
            image = request.files['image']
            if image:

                image_filename = image.filename
                image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))

        dict_answers = myutility.init_answer_and_question(new_answer, answers, "a", image_filename, question_id)

        data_manager.add_answer(dict_answers)

        return redirect(url_for("question_page", question_id=question_id))

    else:
        for question in questions:
            if question['id'] == question_id:
                new_views = str(int(question["view_number"]) + 1)
                data_manager.update_question_views(question_id,int(new_views))
                question['view_number'] = new_views
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
    image_filename = ""
    old_data = data_manager.get_questions()
    new = request.form
    new_dict = myutility.init_answer_and_question(new, old_data, "q", image_filename)
    print(f"reqest.file: {request.files}")
    image_frame=0

    # if request.files:
    if 'file' in request.files:
        image = request.files['image']


        if image.filename == '':
            print('image must have a name')
            return redirect(f"/question/{new_dict['id']}")

        if not myutility.allowed_image_files( image.filename, app.config['ALLOWED_IMAGE_EXTENSION']):
            print("file doesn't have the right extension")
            return redirect(f"/question/{new_dict['id']}")

        image_frame = 1
        image_filename = image.filename
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
        new_dict['image'] = image_filename
    print(new_dict)
    print(f"{old_data[-1]['id']}")
    data_manager.add_question(new_dict)
    return redirect(f"/question/{new_dict['id']}")


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer_page(question_id):
    question_id = int(question_id)
    questions = data_manager.get_questions()
    for question in questions:
        if question['id'] == question_id:
            show_question = question
    return render_template('answer.html', question=show_question)


@app.route('/answer/<answer_id>/delete')
def delete_answer_page(answer_id):
    questions = data_handler.get_data(QUESTIONS_FILE_PATH)
    question_id = 0
    answers = data_handler.get_data(ANSWERS_FILE_PATH)
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer["question_id"]
            for question in questions:
                if question["id"] == answer['question_id']:
                    question['answers'] = int(question['answers']) - 1
            data_handler.write_data(QUESTIONS_FILE_PATH, questions, QUESTIONS_HEADER)
            answers.remove(answer)

    data_handler.write_data(ANSWERS_FILE_PATH,answers,ANSWERS_HEADER)
    return redirect(f'/question/{question_id}')


@app.route('/add_vote')
def add_vote_page():
    request_args = request.args
    print(request_args)
    direction = myutility.add_vote(request_args)
    central = str(int(request_args['name']))
    return redirect(direction+"#"+central)



if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = "/static/images"
    app.run()
