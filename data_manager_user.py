from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_users(cursor):
    query = """
        SELECT users.id,
        users.alias,
        users.username,
        users.submission_time,
        users.reputation,
        count(distinct a.id) as answer_count,
        count(distinct q.id) as question_count,
        count(distinct c.id) as comment_count
        FROM users
        LEFT JOIN answer a on users.id = a.users_id
        LEFT JOIN question q on users.id = q.users_id
        LEFT JOIN comment c on users.id = c.users_id
        GROUP BY users.id;
        """
    cursor.execute(query)
    return cursor.fetchall()
