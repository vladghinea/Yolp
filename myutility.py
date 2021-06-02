from datetime import datetime
import data_handler
import data_manager
import os
from operator import itemgetter


ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'

ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'answers', 'title', 'message', 'image']


def submission_to_time(submission_time):

    time = datetime.fromtimestamp(submission_time)
    return time.strftime("%B %d, %Y")


def init_answer_and_question(new_item, length_item, item_type, image_filename, question_id=0):
    if item_type == "a":
        dict_answers = dict()
        # dict_answers['id'] = str(len(length_item)+1)
        time = datetime.now()
        # dict_answers['submission_time'] = time
        dict_answers['submission_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        dict_answers['vote_number'] = "0"
        dict_answers['question_id'] = question_id
        for k, v in new_item.items():
            dict_answers[k] = v
        dict_answers['image'] = image_filename
        return dict_answers

    elif item_type == "q":
        dict_question = dict()

        time = datetime.now()
        # dict_question['id'] = str(len(length_item))
        dict_question['submission_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        dict_question['view_number'] = "0"
        dict_question['vote_number'] = "0"
        # dict_question['answers'] = "0"
        for k, v in new_item.items():
            dict_question[k] = v.capitalize()
        dict_question['image'] = image_filename
        return  dict_question
    else:
        pass

def edit_question_and_answer(new_item, length_item, item_type, id):
    if item_type == 'q':
        for question in length_item:
            if question['id'] == id:
                question['title'] = new_item['title']
                question['message'] = new_item['message']
                if 'image' in new_item:
                    question['image'] = new_item['image']
        return length_item
    elif item_type == 'a':
        pass


def sorting(order, questions):
    if order =='message':
        ordered_questions = sorted(questions, key=itemgetter('answers'))
    else:
        ordered_questions = sorted(questions, key=itemgetter(order))
    return ordered_questions


def add_vote(request_args):
    if request_args['type_vote'] == 'question':
        questions = data_manager.get_questions()
        for question in questions:
            if question["id"] == int(request_args['id']):
                if request_args["operation"] == "plus":
                    data_manager.update_question_vote_plus(question)
                elif request_args["operation"] == "minus":
                    data_manager.update_question_vote_minus(question)

        return "/list"
    elif request_args['type_vote'] == 'answer':
        answers = data_manager.get_answers()
        for answer in answers:
            if answer['id'] == int(request_args['id']):
                if request_args["operation"] == "plus":
                    print("am intrat aici?")
                    data_manager.update_answer_vote_plus(answer)
                elif request_args["operation"] == "minus":
                    data_manager.update_answer_vote_minus(answer)
        return f"/question/{request_args['question_id']}"


def allowed_image_files(filename, allowed_extensions):
    if not '.' in filename:
        return False
    ext = filename.rsplit('.',1)[1]
    if ext.upper() in allowed_extensions:
        return True
    else:
        return False


def field_message_in_questions(questions, answers):

    for question in questions:
        for answer in answers:
            if answer['question_id'] == question['id']:
                question['answers'] = int(question['answers']) + 1
    return questions



