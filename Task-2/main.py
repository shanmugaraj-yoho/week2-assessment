import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    database = "week2-assessment",
    user = "postgres",
    password = "root",
    port = "5432"
)

def get_orders(customer_id):

    cursor = conn.cursor()
    query = """
        SELECT *
        FROM load_orders WHERE customer_id::text = %s
        """

    cursor.execute(query, (str(customer_id),))
    rows = cursor.fetchall()
    cursor.close()

    return rows

#Normal input
result = get_orders("1")
print("Normal Input:", result)

#SQL Injection
result = get_orders("1 OR 1=1")
print("Total Rows:", len(result))