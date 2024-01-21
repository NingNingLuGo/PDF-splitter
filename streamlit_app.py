import streamlit as st
import mysql.connector

db_config = {
    'host': 'db4free.net',
    'user': 'faeng_123',
    'password': 'xwTfB1fz4i',
    'database': 'faeng_123'
}

def create_connection():
    return mysql.connector.connect(**db_config)

def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    table_query = '''
    CREATE TABLE IF NOT EXISTS info_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT NOT NULL
    )
    '''

    cursor.execute(table_query)
    connection.commit()
    cursor.close()
    connection.close()

def insert_data(name, age):
    connection = create_connection()
    cursor = connection.cursor()

    insert_query = '''
    INSERT INTO info_table (name, age) VALUES (%s, %s)
    '''
    values = (name, age)
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

def fetch_data():
    connection = create_connection()
    cursor = connection.cursor()

    select_query = '''
    SELECT * FROM info_table
    '''

    cursor.execute(select_query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data

def main():
    st.title("Login Form")

    name = st.text_input("Name")
    age = st.number_input("Age")

    if st.button("Submit"):
        insert_data(name, age)
        st.success("Data inserted successfully!")

    st.title("Table Data")
    table_data = fetch_data()
    st.table(table_data)

if __name__ == '__main__':
    create_table()
    main()
