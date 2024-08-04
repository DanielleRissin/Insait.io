import os
import pytest
import psycopg2
from unittest.mock import patch
from services.db.db_handler import create_db, insert_data

# Set environment variables for testing
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'test_db'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASS'] = 'password'
os.environ['DB_PORT'] = '5432'
os.environ['TABLE_NAME'] = 'test_data'

hostname = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
pwd = os.getenv('DB_PASS')
port_id = os.getenv('DB_PORT')
table_name = os.getenv('TABLE_NAME')


@pytest.fixture(scope='module')
def db_conn():
    """Set up and tear down the test database."""
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    create_db(table_name, conn)
    yield conn
    conn.close()


@pytest.fixture
def mock_db_conn(mocker):
    """Mock the database connection for FlaskServer."""
    mock_conn = mocker.patch('services.db.db_handler.psycopg2.connect')
    return mock_conn


def test_create_db(db_conn):
    """Test that the table is created successfully."""
    with db_conn.cursor() as cur:
        cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');")
        assert cur.fetchone()[0] is True


def test_insert_data(db_conn):
    """Test inserting data into the table."""
    id = 1
    question = "What is the capital of France?"
    response = "Paris"
    insert_data(id, question, response, table_name, db_conn)

    with db_conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table_name} WHERE id = %s;", (id,))
        result = cur.fetchone()
        assert result is not None
        assert result[1] == question
        assert result[2] == response
