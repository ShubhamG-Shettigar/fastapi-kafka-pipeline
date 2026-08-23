from app.db.postgres import get_connection

def get_orders_by_user(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT
                order_id,
                customer_name,
                amount,
                event_id
            FROM orders
            WHERE user_id = %s
            ORDER BY id;
            """,
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()