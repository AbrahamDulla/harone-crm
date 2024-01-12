from mariadb import connect, Error

def get_database_connection():
    try:
        connection = connect(
            host="localhost",
            port=3300,
            user="root",
            password="ziye245680",
            database="harone_crm"
        )
        return connection
    except Error as e:
        raise Exception("Failed to connect to the database.")

def close_database_connection(connection):
    connection.close()