import mysql.connector
from tkinter import messagebox

def get_connection():
    """Establish and return database connection"""
    try:
        connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='restaurant_management'
        )
        return connect
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    """Execute a query and return results if fetch=True"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        else:
            conn.commit()
            cursor.close()
            conn.close()
            return True
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Error: {err}")
        if conn:
            conn.close()
        return None