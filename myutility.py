from datetime import datetime


def init_answer_and_question(new_item, length_item, q, question_id=0):
    if q == "a":
        dict_answers = dict()
        dict_answers['id'] = str(len(length_item) + 1)
        time = datetime.now()
        submission_time = int(datetime.timestamp(time))
        dict_answers['submission_time'] = str(submission_time)
        dict_answers['vote_number'] = "0"
        dict_answers['question_id'] = question_id
        for k, v in new_item.items():
            dict_answers[k] = v
        return dict_answers

    elif q == "q":
        dict_question = dict()
        dict_question['id'] = str(len(length_item) + 1)
        time = datetime.now()
        submission_time = int(datetime.timestamp(time))
        dict_question['submission_time'] = str(submission_time)
        dict_question['view_number'] = "0"
        dict_question['vote_number'] = "0"
        for k, v in new_item.items():
            dict_question[k] = v
        return  dict_question
    else:
        pass


def add_view(item):
    pass


def add_vote(item, id, question_id):
    vote = int(item['vote_number'])
    return vote



