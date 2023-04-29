import pymssql
import pytest

server = "EPBYMINW03C8"
password = "Password1234_6"
user = "TestLogin"
db = "TRN"
port = 1433

#conn = pymssql.connect(server=server, user=user, password=password, database=db, port=port)
#cursor = conn.cursor(as_dict=True)

@pytest.fixture
def conn():
    conn = pymssql.connect(server=server, user=user, password=password, database=db, port=port)
    yield conn

@pytest.fixture
def cursor(conn):
    cursor = conn.cursor(as_dict=True)
    yield cursor
    conn.rollback()

def test_Row_Count_countries(cursor):
    cursor.execute('select * from TRN.hr.countries;')
    rs = cursor.fetchall()
    assert len(rs) == 25

def test_No_Duplicated_Rows_Countries(cursor):
    cursor.execute('select count(*) as Count from (select * from TRN.hr.countries) test EXCEPT select count(*) as Count from (select distinct * from TRN.hr.countries) test2;')
    rs = cursor.fetchall()
    assert len(rs) == 0

def test_Columns_Number_Jobs(cursor):
    cursor.execute("""select * from TRN.INFORMATION_SCHEMA.COLUMNS where table_name = 'jobs';""")
    rs = cursor.fetchall()
    assert len(rs) == 4

def test_Sum_Numeric_Fields_Jobs(cursor):
    cursor.execute('select CAST(sum(min_salary) as INT) as min, CAST(sum(max_salary) as INT) as max from TRN.hr.jobs;')
    rs = cursor.fetchall()
    assert rs == [{'max': 251000, 'min': 124800}]

def test_No_Nulls_City_Column_Of_Locations_Table(cursor):
    cursor.execute('select * from TRN.hr.locations where city is null;')
    rs = cursor.fetchall()
    assert len(rs) == 0

def test_Data_Types_Locations_Table_Correct(cursor):
    cursor.execute("""SELECT column_name, data_type FROM TRN.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'locations';""")
    rs = cursor.fetchall()
    assert rs == [{'column_name': 'location_id', 'data_type': 'int'}, {'column_name': 'street_address', 'data_type': 'varchar'}, {'column_name': 'postal_code', 'data_type': 'varchar'}, {'column_name': 'city', 'data_type': 'varchar'}, {'column_name': 'state_province', 'data_type': 'varchar'}, {'column_name': 'country_id', 'data_type': 'char'}]