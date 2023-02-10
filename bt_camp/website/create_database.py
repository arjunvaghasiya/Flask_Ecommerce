import psycopg2

#establishing the connection
def create_database():
    try:
        
        conn = psycopg2.connect(
        database="postgres", user='postgres', password='abc123', host='127.0.0.1', port= '5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        sql = '''CREATE database ecommerce''';
        cursor.execute(sql)
        print("Database created successfully........")
        conn.close()
        return print("Database created successfully........")
    
    except:
        return print('already exist')
    
