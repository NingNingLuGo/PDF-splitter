import streamlit as st
import mysql.connector
import pandas as pd

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

def delete_row(row_id):
    connection = create_connection()
    cursor = connection.cursor()

    delete_query = '''
    DELETE FROM info_table WHERE id = %s
    '''
    values = (row_id,)
    cursor.execute(delete_query, values)
    connection.commit()
    cursor.close()
    connection.close()

def main():
    
    st.title("Table Data")

    # 获取数据
    table_data = fetch_data()

    # 将数据转换为Pandas DataFrame
    df = pd.DataFrame(table_data, columns=['Name', 'Age', 'ID'])

    # 在Streamlit中显示DataFrame
    st.dataframe(df)
    st.title("Login Form")

    name = st.text_input("Name")
    age = st.number_input("Age", value=0, min_value=0, step=1, format="%d")

    if st.button("Submit"):
        insert_data(name, age)
        st.success("Data inserted successfully!")

        # 刷新应用
        st.rerun()

    # 删除行
    selected_id = st.number_input("Enter the ID of the row to delete", value=0, min_value=0, max_value=df['ID'].max(), step=1, format="%d")
    
    if st.button("Delete Row"):
        delete_row(selected_id)
        st.success("Row deleted successfully!")

        # 刷新应用
        st.rerun()


if __name__ == '__main__':
    create_table()
    main()
