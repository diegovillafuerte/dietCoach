from dbOperations import create_connection, close_connection, create_meal_table

conn = create_connection()

create_meal_table(conn)

close_connection(conn)