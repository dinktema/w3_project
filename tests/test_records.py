import pytest

from helpers.values_processing import find_record_in_table, check_errors
from pages.sql_coding_mode import SQLCodingPage

endpoint = '/sql/trysql.asp?filename=trysql_select_all'


def test_fi(setup):
    page = SQLCodingPage(setup)
    page.enter_request("SELECT * FROM Customers WHERE ContactName = 'Giovanni Rovelli';")
    page.run_sql()
    table = page.get_result()
    check_errors(table)
    record = find_record_in_table(table, {'ContactName': 'Giovanni Rovelli'})
    assert len(record) == 1
    assert record[0]['Address'] == 'Via Ludovico il Moro 22'


def test_sec(setup):
    page = SQLCodingPage(setup)
    page.enter_request("SELECT * FROM Customers WHERE City = 'London';")
    page.run_sql()
    table = page.get_result()
    check_errors(table)
    record = find_record_in_table(table, {'City': 'London'})
    assert len(table) == 6
    assert len(record) == 6


def test_thi(setup):
    page = SQLCodingPage(setup)
    page.enter_request("INSERT INTO Customers (CustomerName, City, Country)"
                       " VALUES ('Cardinal', 'Stavanger', 'Norway');")
    page.run_sql()
    table = page.get_result()
    check_errors(table)
    record = find_record_in_table(table, {'City': 'Stavanger', 'CustomerName': 'Cardinal'})
    assert len(record) == 1
    assert record[0]['City'] == 'Stavanger' and \
           record[0]['Country'] == 'Norway' and \
           record[0]['CustomerName'] == 'Cardinal'


def test_four(setup):
    page = SQLCodingPage(setup)
    page.enter_request("UPDATE Customers "
                       "SET City = 'Frankfurt', Country = 'Germany', "
                       "CustomerName = 'Santa Alfred', ContactName = 'Dirty Alfred',"
                       " Address = 'Obere Str. 57', PostalCode = '000131'"
                       " WHERE CustomerName = 'Cardinal';")
    page.run_sql()
    table = page.get_result()
    check_errors(table)
    record = find_record_in_table(table, {'City': 'Frankfurt', 'CustomerName': 'Santa Alfred'})
    assert len(record) == 1
    assert record[0]['City'] == 'Stavanger' and \
           record[0]['Country'] == 'Norway' and \
           record[0]['Address'] == 'Obere Str. 57' and \
           record[0]['PostalCode'] == '000131' and \
           record[0]['ContactName'] == 'Dirty Alfred' and \
           record[0]['CustomerName'] == 'Cardinal'


@pytest.mark.parametrize("value, expected", [(" ", "Error in SQL:\nInvalid SQL statement; expected DELETE,"
                                                   " INSERT, PROCEDURE, SELECT, or UPDATE."),
                                             ("SELECT CustomerID FROM Customers WHERE CustomerName LIKE 'an%';",
                                                [{'CustomerID': '2'},
                                                 {'CustomerID': '3'}])
                                             ])
def test_fifth(setup, value, expected):
    page = SQLCodingPage(setup)
    page.enter_request(value)
    page.run_sql()
    table = page.get_result()
    assert table == expected

