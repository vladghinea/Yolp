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
def add_answer(cursor,new_answer):
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)     
        VALUES ('{new_answer['submission_time']}', '{new_answer['vote_number']}', '{new_answer["question_id"]}','{new_answer['message']}','{new_answer["image"]}')
        """
    cursor.execute(query)