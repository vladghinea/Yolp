from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

@database_common.connection_handler
def count_no_null(cursor):
    query = """
        UPDATE comment
        SET edited_count = '0'
        WHERE edited_count is null 
        """
    cursor.execute(query)

@database_common.connection_handler
def get_tags(cursor):
    query = """
        SELECT *
        FROM tag
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_questions_tag(cursor):
    query = """
            SELECT *
            FROM question_tag
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_questions(cursor):
    query = """
        SELECT question.id,question.submission_time,question.vote_number,question.view_number,question.title,question.message,question.image,users.alias
        FROM question
        INNER JOIN users on question.users_id = users.id
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_users(cursor):
    query = """
        SELECT *
        FROM users
        """
    cursor.execute(query)
    return cursor.fetchall()




@database_common.connection_handler
def get_comment(cursor):
    query = """
        SELECT comment.id,comment.question_id,comment.answer_id,comment.users_id,comment.message,comment.submission_time,comment.edited_count,users.alias
        FROM comment
        INNER JOIN users on users.id = comment.users_id
        ORDER BY comment.submission_time DESC"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_answers(cursor):
    query = """
        SELECT answer.id,answer.submission_time,answer.vote_number,answer.question_id,answer.users_id,answer.message,answer.image,users.alias
        FROM answer
        INNER JOIN users on users.id = answer.users_id
        ORDER BY answer.id"""
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
def add_user(cursor,username,alias,hash_password):
    query = f"""
        INSERT INTO users (submission_time, alias, username, password, admin, reputation)     
        VALUES (date_trunc('second', now()::timestamp), '{alias}', '{username}','{hash_password}',False,0)
        """
    cursor.execute(query)


@database_common.connection_handler
def add_answer(cursor,new_answer):
    new_message = new_answer['message'].replace("'", "''")
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image,users_id)     
        VALUES ('{new_answer['submission_time']}', '{new_answer['vote_number']}', '{new_answer["question_id"]}','{new_message}','{new_answer["image"]}','{new_answer["users_id"]}')
        """
    cursor.execute(query)

@database_common.connection_handler
def add_question(cursor,new_question):
    new_message = new_question['message'].replace("'", "''")
    new_title = new_question['title'].replace("'", "''")
    query = f"""
        INSERT INTO question ( submission_time, view_number, vote_number, title, message, image,users_id)   
        VALUES ('{new_question['submission_time']}', '{new_question['view_number']}', '{new_question["vote_number"]}','{new_title}','{new_message}','{new_question["image"]}','{new_question["users_id"]}')
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
def delete_comment(cursor,comment_id):
    query = f"""
        DELETE
        FROM comment
        WHERE id = '{comment_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_answer_comment(cursor,answer_id):
    query = f"""
        DELETE
        FROM comment
        WHERE answer_id = '{answer_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_question_comment(cursor,question_id):
    query = f"""
        DELETE
        FROM comment
        WHERE question_id = '{question_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def edit_comment(cursor, edit_comment,comment_id):
    new_message = edit_comment['message'].replace("'", "''")
    query = f"""
            UPDATE comment
            SET  message = '{new_message}' ,submission_time = date_trunc('second', now()::timestamp),edited_count = edited_count + 1
            WHERE id = '{comment_id}'
            """
    cursor.execute(query)

@database_common.connection_handler
def edit_question(cursor,question_id, edit_question, image_file):
    new_message = edit_question['message'].replace("'", "''")
    new_title = edit_question['title'].replace("'", "''")
    query = f"""
        UPDATE question
        SET  title = '{new_title}', message = '{new_message}', image = '{image_file}'
        WHERE id = '{question_id}'
        """
    cursor.execute(query)


@database_common.connection_handler
def edit_answer(cursor,answer_id, edit_answer, image_file):
    new_message = edit_answer['message'].replace("'", "''")
    query = f"""
        UPDATE answer
        SET  message = '{new_message}', image = '{image_file}'
        WHERE id = '{answer_id}'
        """
    cursor.execute(query)


@database_common.connection_handler
def add_comment_answer(cursor,answer_id,new_message,time,users_id):
    n_message = new_message.replace("'","''")
    query = f"""
        INSERT INTO comment ( answer_id, message, submission_time, edited_count,users_id)
        VALUES ('{answer_id}','{n_message}','{time}' ,'0','{users_id}')
        """
    cursor.execute(query)

@database_common.connection_handler
def add_comment_question(cursor,question_id,new_message,time,users_id):
    n_message = new_message.replace("'", "''")
    query = f"""
        INSERT INTO comment ( question_id, message, submission_time, edited_count,users_id)
        VALUES ('{question_id}','{n_message}','{time}','0','{users_id}' )
        """
    cursor.execute(query)

@database_common.connection_handler
def add_new_tag(cursor,tag):
    new_tag = tag.replace("'", "''")
    query = f"""
        INSERT INTO tag (name)
        VALUES ('{new_tag}')
        """
    cursor.execute(query)

@database_common.connection_handler
def add_tags_id(cursor,question_id,tag_id):
    query = f"""
        INSERT INTO question_tag (question_id, tag_id)
        VALUES ('{question_id}','{tag_id}')
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_tag(cursor,tag_id):
    query = f"""
        DELETE
        FROM tag
        WHERE id = '{tag_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_question_tag(cursor,tag_id):
    query = f"""
        DELETE
        FROM question_tag
        WHERE tag_id = '{tag_id}'
        """
    cursor.execute(query)

@database_common.connection_handler
def delete_question_tag_id(cursor,question_id):
    query = f"""
        DELETE
        FROM question_tag
        WHERE question_id = '{question_id}'
        """
    cursor.execute(query)


@database_common.connection_handler
def get_search_questions(cursor,word):
    query = f"""
        SELECT *
        FROM question 
        WHERE LOWER(question.message)  LIKE '%{word}%' or LOWER(question.title) LIKE '%{word}%'
        ORDER BY question.id
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_search_answers(cursor,word):
    query = f"""
        SELECT *
        FROM answer 
        WHERE LOWER(answer.message)  LIKE '%{word}%' 
        ORDER BY answer.id
        """
    cursor.execute(query)
    return cursor.fetchall()