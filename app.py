import datetime
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for
import os
import myutility
import data_manager


app = Flask(__name__)

vlad = '/home/vlad/projects/ask-mate-3-python-vladghinea/static/images/uploads/'
lamine = '/home/keitkalon/projects/web/ask-mate-3-python-vladghinea/static/images/uploads'
home = os.path.join(app.root_path, 'static/images/uploads')
app.config['IMAGE_UPLOADS'] = vlad
app.config['ALLOWED_IMAGE_EXTENSION'] = ['PNG', 'JPG', 'JPEG']

@app.route("/")
@app.route("/list")
def list_page():
    data_manager.count_no_null()
    questions = data_manager.get_questions()
    if request.path == '/':
        if request.args:
            order = request.args['order']
            questions = myutility.sorting(order, questions)
            if 'type' in request.args.keys():
                if request.args['type'] == 'desc':
                    questions = questions[::-1]
        else:
            questions = questions[::-1]
        show_question = questions[:5]
        return render_template("list.html", questions=show_question)
    else:
        if request.args:
            order = request.args['order']
            questions = myutility.sorting(order, questions)
            if 'type' in request.args.keys():
                if request.args['type'] == 'desc':
                    questions = questions[::-1]
        else:
            questions = questions[::-1]
        return render_template("list.html", questions=questions)


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    comment_id = int(comment_id)
    question_id = 0
    comments = data_manager.get_comment()
    for comment in comments:
        if comment["id"] == comment_id:
            question_id = comment["question_id"]
            if question_id is None:
                answers = data_manager.get_answers()
                for answer in answers:
                    if answer['id'] == comment['answer_id']:
                        question_id = answer["question_id"]
    data_manager.delete_comment(comment_id)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    question_id = int(question_id)
    answers = data_manager.get_answers()
    for answer in answers:
        if answer['question_id'] == question_id:
            data_manager.delete_answer_comment(answer['id'])
    data_manager.delete_question_tag_id(question_id)
    data_manager.delete_question_comment(question_id)
    data_manager.delete_answers(question_id)
    data_manager.delete_question(question_id)
    return redirect("/list")

@app.route('/answer/<answer_id>/delete')
def delete_answer_page(answer_id):
    answer_id= int(answer_id)
    question_id = 0
    answers = data_manager.get_answers()
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer["question_id"]
            data_manager.delete_answer_comment(answer_id)
            data_manager.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/comment/<comment_id>/edit', methods=["GET","POST"])
def edit_comment_page(comment_id):
    comment_id = int(comment_id)
    if request.method == 'POST':
        edit_comment = request.form
        question_id = request.args['question_id']
        if question_id == "None":
            answers = data_manager.get_answers()
            answer_id = request.args['answer_id']
            for answer in answers:
                if answer['id'] == int(answer_id):
                    question_id = answer['question_id']
        data_manager.edit_comment(edit_comment,comment_id)
        return redirect(f'/question/{question_id}')
    if request.method == "GET":
        comments = data_manager.get_comment()
        for comment in comments:
            if comment['id'] == comment_id:
                return render_template('edit_comment.html', comment=comment, comment_id=comment_id )


@app.route('/answer/<answer_id>/edit', methods=['GET','POST'])
def edit_answer_page(answer_id):
    answer_id =int(answer_id)
    if request.method == 'POST':
        edit_answer = request.form
        question_id = request.args['question_id']
        image_file = ""
        if request.files["image"].filename != "":
            image = request.files['image']
            if not myutility.allowed_image_files(image.filename, app.config['ALLOWED_IMAGE_EXTENSION']):
                print("file doesn't have the right extension")
                return redirect(f'/answer/{answer_id}')
            image_file = image.filename
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
        data_manager.edit_answer(answer_id, edit_answer, image_file)
        return redirect(f'/question/{question_id}')
    if request.method == "GET":
        answers = data_manager.get_answers()
        for answer in answers:
            if answer['id'] == answer_id:
                return render_template('edit_answer.html', answer=answer, answer_id=answer_id )


@app.route('/question/<question_id>/edit', methods=['GET','POST'])
def edit_question_page(question_id):
    question_id = int(question_id)
    if request.method == 'POST':
        edit_question = request.form
        image_file = ""
        if request.files["image"].filename != "":
            image = request.files['image']
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

@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_tag(question_id):
    questions = data_manager.get_questions()
    if request.method =="GET":
        for question in questions:
            if question['id'] == int(question_id):
                return render_template("add_tag.html" , question=question)
    else:
        new_tag = request.form['tag']
        data_manager.add_new_tag(new_tag)
        tags = data_manager.get_tags()
        id_tag = tags[-1]['id']
        data_manager.add_tags_id(question_id,id_tag)
        return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id,tag_id):
    data_manager.delete_question_tag(tag_id)
    data_manager.delete_tag(tag_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def question_page(question_id):
    question_id = int(question_id)
    comments = data_manager.get_comment()
    questions = data_manager.get_questions()
    answers = data_manager.get_answers()
    all_tags = data_manager.get_tags()
    tag_ids = data_manager.get_questions_tag()
    show_comments_questions = []
    show_comments_answers = []
    show_question = {}
    show_answer = []
    show_tags =[]
    if request.method == "POST":
        for answer in answers:
            if answer['question_id'] == question_id:
                show_answer.append(answer)
        new_answer = request.form
        image_filename = ""
        if request.files["image"].filename != "":
            image = request.files['image']
            if image:
                image_filename = image.filename
                image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
        dict_answers = myutility.init_answer_and_question(new_answer, "a", image_filename, question_id)
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
                for comment in comments:
                    if answer['id'] == comment['answer_id']:
                        show_comments_answers.append(comment)
                show_answer.append(answer)
        for comment in comments:
            if comment['question_id'] == question_id:
                show_comments_questions.append(comment)
        for tag in tag_ids:
            if tag['question_id'] == question_id:
                for name_tag in all_tags:
                    if tag['tag_id'] == name_tag['id']:
                        show_tags.append(name_tag)

        return render_template("question.html", question=show_question, answers=show_answer, comments_question=show_comments_questions, comments_answers=show_comments_answers, tags=show_tags)


@app.route("/add-question")
def add_question_page():
    return render_template('add_question.html')


@app.route("/add", methods=['POST'])
def add():
    image_filename = ""
    new = request.form
    new_dict = myutility.init_answer_and_question(new, "q", image_filename)
    if request.files["image"].filename != "":
        image = request.files['image']
        if not myutility.allowed_image_files( image.filename, app.config['ALLOWED_IMAGE_EXTENSION']):
            return redirect(f"/question/{new_dict['id']}")
        image_filename = image.filename
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
        new_dict['image'] = image_filename
    data_manager.add_question(new_dict)
    questions = data_manager.get_questions()
    return redirect(f"/question/{questions[-1]['id']}")


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer_page(question_id):
    question_id = int(question_id)
    questions = data_manager.get_questions()
    for question in questions:
        if question['id'] == question_id:
            show_question = question
    return render_template('answer.html', question=show_question)


@app.route('/add_vote')
def add_vote_page():
    request_args = request.args
    print(request_args)
    direction = myutility.add_vote(request_args)
    central = str(int(request_args['id']))
    return redirect(direction+"#"+central)


@app.route('/question/<question_id>/new-comment', methods=['GET','POST'])
def add_question_comment(question_id):
    new_message = request.form['new_comment_q']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_manager.add_comment_question(question_id, new_message, time)
    return redirect(url_for("question_page", question_id=question_id))


@app.route('/answer/<answer_id>/new-comment' , methods=['GET','POST'])
def add_answer_comment(answer_id):
    new_message = request.form['new_comment_a']
    question_id = request.args['question_id']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_manager.add_comment_answer(answer_id,new_message,time)
    return redirect(url_for("question_page", question_id=question_id))


@app.route('/search', methods=["POST"])
def search():
    word = request.form['search'].lower()
    questions = data_manager.get_search_questions(word)
    answers = data_manager.get_search_answers(word)
    show_question=[]
    if answers:
        for answer in answers:
            all_questions = data_manager.get_questions()
            for question in all_questions:
                if answer["question_id"] == question['id']:
                    show_question.append(question)
    for qst in questions:
        if qst not in show_question:
            show_question.append(qst)
    return render_template("list_search.html", questions=show_question, answers=answers, word=word)


if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = "/static/images"
    app.run()
