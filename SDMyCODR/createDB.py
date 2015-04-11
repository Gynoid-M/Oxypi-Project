import MySQLdb


DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'marina'
DB_NAME = 'ibis_database'

datos = [DB_HOST,DB_USER,DB_PASS,DB_NAME]
conn = MySQLdb.Connect(*datos)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS DATOS")
sql = """ CREATE TABLE DATOS(
            FECHA CHAR(50),
            SPO2 INT,
            RPM INT) """
                        
		
cursor.execute(sql)