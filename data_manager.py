from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_comment(cursor):
    query = """
        SELECT *
        FROM comment
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_answers(cursor):
    query = """
        SELECT *
        FROM answer
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def update_question_views(cursor,question_id,new_views):
    query = f"""
        UPDATE question
        SET view_number = '{new_views}'
        WHERE id = '{question_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def update_question_vote_plus(cursor,question):
    vote = int(question['vote_number']) + 1
    query = f"""
        UPDATE question
        SET vote_number = '{vote}'
        WHERE id = '{question['id']}'
        """
    cursor.execute(query)

@database_common.connection_handler
def update_question_vote_minus(cursor,question):
    vote = int(question['vote_number']) - 1
    query = f"""
        UPDATE question
        SET vote_number = '{vote}'
        WHERE id = '{question['id']}'
        """
    cursor.execute(query)

@database_common.connection_handler
def update_answer_vote_plus(cursor,answer):
    vote = int(answer['vote_number']) + 1
    query = f"""
        UPDATE answer
        SET vote_number = '{vote}'
        WHERE id = '{answer['id']}'
        """
    cursor.execute(query)

@database_common.connection_handler
def update_answer_vote_minus(cursor,answer):
    vote = int(answer['vote_number']) - 1
    query = f"""
        UPDATE answer
        SET vote_number = '{vote}'
        WHERE id = '{answer['id']}'
        """
    cursor.execute(query)



@database_common.connection_handler
def add_answer(cursor,new_answer):
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)     
        VALUES ('{new_answer['submission_time']}', '{new_answer['vote_number']}', '{new_answer["question_id"]}','{new_answer['message']}','{new_answer["image"]}')
        """
    cursor.execute(query)

@database_common.connection_handler
def add_question(cursor,new_question):
    query = f"""
        INSERT INTO question ( submission_time, view_number, vote_number, title, message, image)   
        VALUES ('{new_question['submission_time']}', '{new_question['view_number']}', '{new_question["vote_number"]}','{new_question['title']}','{new_question['message']}','{new_question["image"]}')
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_question(cursor,question_id):
    query = f"""
        DELETE
        FROM question
        WHERE id = '{question_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_answer(cursor,answer_id):
    query = f"""
        DELETE
        FROM answer
        WHERE id = '{answer_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_answers(cursor,question_id):
    query = f"""
        DELETE
        FROM answer
        WHERE question_id = '{question_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def edit_question(cursor,question_id, edit_question, image_file):
    query = f"""
        UPDATE question
        SET  title = '{edit_question['title']}', message = '{edit_question['message']}', image = '{image_file}'
        WHERE id = '{question_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def add_comment_answer(cursor,answer_id,new_message,time):
    query = f"""
        INSERT INTO comment ( answer_id, message, submission_time)
        VALUES ('{answer_id}','{new_message}','{time}' )
        """
    cursor.execute(query)

@database_common.connection_handler
def add_comment_question(cursor,question_id,new_message,time):
    query = f"""
        INSERT INTO comment ( question_id, message, submission_time)
        VALUES ('{question_id}','{new_message}','{time}' )
        """
    cursor.execute(query)