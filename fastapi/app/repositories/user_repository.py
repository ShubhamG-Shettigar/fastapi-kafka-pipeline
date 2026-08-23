from app.db.postgres import get_connection

def get_user_by_username(username: str):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT id, username, password FROM auth_users WHERE username = %s
            """,(username,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()