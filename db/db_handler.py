import psycopg2
import os

hostname = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
pwd = os.getenv('DB_PASS')
port_id = os.getenv('DB_PORT')
def create_db(table_name, conn):
    connect_par = conn
    curser_arg = None
    try:
        connect_par = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)
        curser_arg = connect_par.cursor()
        curser_arg.execute(f"DROP TABLE IF EXISTS {table_name}")
        creat_script = f''' CREATE TABLE IF NOT EXISTS {table_name}(
                    id          int PRIMARY KEY,
                    question    varchar,
                    answer      varchar)'''
        curser_arg.execute(creat_script)

        connect_par.commit()
    except Exception as error:
        print(error)
    finally:
        if (curser_arg is not None):
            curser_arg.close()
        if connect_par is not None:
            connect_par.close()


def insert_data(id, question,response, table_name, conn):
    connect_par = conn
    curser_arg = None
    try:
        print("Question: " + question)
        print("Answer: " + response)
        connect_par = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)
        curser_arg = connect_par.cursor()
        # Check if table exists
        curser_arg.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = '{table_name}'
            );
        """)
        exists = curser_arg.fetchone()[0]

        if not exists:
            raise Exception(f"Table {table_name} does not exist.")
        insert_script = f' INSERT INTO {table_name} (id,question,answer) VALUES(%s,%s,%s)'
        insert_value = (id, question, response)
        curser_arg.execute(insert_script, insert_value)

        connect_par.commit()

    except Exception as error:
        print(error)
    finally:
        if (curser_arg is not None):
            curser_arg.close()
        if connect_par is not None:
            connect_par.close()


