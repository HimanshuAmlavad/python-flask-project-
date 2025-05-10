from mysql import connector
from uuid import uuid4

class db_function:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.mydb = connector.connect(host = "localhost", user ="root", password = "Amlavad@2002")

        self.mycursor = self.mydb.cursor()

        self.mycursor.execute("create database if not exists authentication;")
        self.mycursor.execute("use authentication")
        self.mycursor.execute("""
        create table if not exists user(
            id int primary key not null auto_increment,
            user_id  varchar(36) unique not null,
            user_email varchar(50) unique not null,
            user_password varchar(50)
        );
        """)
    def check_email(self):
        query = "SELECT user_email FROM user WHERE user_email = %s;"    
        value =(self.email,)

        self.mycursor.execute(query,value)
        result = self.mycursor.fetchone()
        if result:
            if result[0] == self.email:
                return True
        return False
    
    def insert_detail(self):
        user_id = str(uuid4())

        query = "INSERT INTO user(user_id, user_email, user_password) VALUES(%s, %s, %s);"
        value =  (user_id, self.email, self.password)

        self.mycursor.execute(query,value)
        self.mydb.commit()
        print( self.mycursor.execute("SELECT * FROM user;"))

    def check_password(self):
        query = "SELECT user_password FROM user WHERE user_password = %s"
        value = (self.password,)

        self.mycursor.execute(query,value)
        result = self.mycursor.fetchone()

        if result[0] == self.password:
            return True
        return False
    # def show_details(self):
    #     print(self.mycursor.execute("select * from user;"))




if __name__ == "__main__":
    initilise = db_function(email="jagat69133@prorsd.com", password="him")
    # initilise.show_database()
    initilise.show_details()
    

    # def show_database(self):
    #     print("data base")
    #     self.mycursor.execute('SHOW databases')
    #     for db in self.mycursor.fetchall():
    #         print(db)
    #     print("tables")
    #     self.mycursor.execute('SHOW TABLES')
    #     for table in self.mycursor.fetchall():
    #         print(table)