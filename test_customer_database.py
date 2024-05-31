from sqlite3 import IntegrityError, Connection

import pytest

from customer_database import Customer


@pytest.fixture(scope="function")  # Scope de la fixture, par default function
def customer_without_table():
    """
    Connection to in memory database using the Customer class

       :return: An instantiated Customer class
    """
    customer = Customer()  # Avant le test, c'est le setup
    yield customer  # Un yield évite de sortir de la fonction
    customer.con.close()  # Après le test, le teardown


@pytest.fixture(scope="function")
def customer_with_table(customer_without_table):
    """
    Connection to in memory database using the Customer class returned the table
    has been created.

       :param customer_without_table: The customer_without_table fixture
       :return: An instantiated Customer class
    """
    customer_without_table.create_table()
    return customer_without_table


def test_instantiation(customer_without_table):
    """
    Test the instance of the Customer has an attribute instance of a
    sqlite3.Connection.

       :param customer_without_table: Fixture of a virgin connection
    """
    assert isinstance(customer_without_table.con, Connection)


def test_customer_table_creation(customer_without_table):
    """
    Test the customer_without_table database, the CREATE instruction and SQL validity of the
    definition of the table.

       :param customer_without_table: Fixture of a virgin connection
    """
    try:
        customer_without_table.create_table()
    except Exception as e:
        pytest.fail("The table creation failed: %s" % e)


def test_add_customer(customer_with_table):
    """
    Test the customer_with_table database, the INSERT instruction and SQL validity of the
    definition of the table.

       :param customer_with_table: Fixture of a newly created empty table.
    """
    try:
        customer_with_table.insert(1, "christophe@in-france.fr")
    except Exception as e:
        pytest.fail("The customer insertion failed: %s" % e)


def test_customer_uniqueness(customer_with_table):
    """
    Test the same customer ID cannot be added twice therefore they are unique.

      :param customer_with_table: Fixture of a newly created empty table.
    """
    customer_id = 1
    email = "christophe@in-france.fr"
    customer_with_table.insert(customer_id, email)
    with pytest.raises(IntegrityError):
        customer_with_table.insert(customer_id, email)


def test_customer_id_cannot_be_null(customer_with_table):
    """
    Test the customer id cannot be NULL.

       :param customer_with_table: Fixture of a newly created empty table.
    """
    with pytest.raises(IntegrityError):
        customer_with_table.insert(None, "christophe@in-france.fr")


def test_customer_email_cannot_be_null(customer_with_table):
    """
    Test the customer email cannot be NULL.

       :param customer_with_table: Fixture of a newly created empty table.
    """
    with pytest.raises(IntegrityError):
        customer_with_table.insert(1, None)
