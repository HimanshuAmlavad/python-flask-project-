from datetime import datetime, timedelta
from uuid import uuid4

from mysql import connector


class Database:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.mydb = connector.connect(
            host="localhost", user="root", password="Amlavad@2002"
        )

        self.mycursor = self.mydb.cursor()

        self.mycursor.execute("create database if not exists authentication;")
        self.mycursor.execute("use authentication")
        self.mycursor.execute(
            """
        create table if not exists user(
            id int primary key not null auto_increment,
            user_id  varchar(36) unique not null,
            user_email varchar(50) unique not null,
            user_password varchar(50)
        );
        """
        )

        self.mycursor.execute(
            """ 
        CREATE TABLE IF NOT EXISTS reset_password (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            user_id int not null,
            reset_token VARCHAR(150) NOT NULL,
            token_expiry TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        );
        """
        )

    def check_email(self):
        query = "SELECT user_email FROM user WHERE user_email = %s;"
        value = (self.email,)

        self.mycursor.execute(query, value)
        result = self.mycursor.fetchone()
        if result:
            if result[0] == self.email:
                return True
        return False

    def insert_detail(self):
        user_id = str(uuid4())

        query = (
            "INSERT INTO user(user_id, user_email, user_password) VALUES(%s, %s, %s);"
        )
        value = (user_id, self.email, self.password)

        self.mycursor.execute(query, value)
        self.mydb.commit()
        print(self.mycursor.execute("SELECT * FROM user;"))

    def check_password(self):
        query = "SELECT user_password FROM user WHERE user_password = %s"
        value = (self.password,)

        self.mycursor.execute(query, value)
        result = self.mycursor.fetchone()

        if result[0] == self.password:
            return True
        return False

    def reset_password(self, token):

        expiry = datetime.now() + timedelta(hours=1)
        query = "select id from user where user_email=%s;"
        values = (self.email,)
        self.mycursor.execute(query, values)
        result = self.mycursor.fetchone()
        if not result:
            print("id not fatched")
            return None

        user_table_id = result[0]
        query = "INSERT INTO reset_password(user_id, reset_token, token_expiry) VALUES(%s,%s,%s);"
        values = (user_table_id, token, expiry)
        self.mycursor.execute(query, values)
        self.mydb.commit()
        return True

    def verify_token(self, token):
        # Get token and its expiry time if token matches
        query = "SELECT token_expiry FROM reset_password WHERE reset_token = %s"
        values = (token,)
        self.mycursor.execute(query, values)
        result = self.mycursor.fetchone()

        if result:
            stored_time = result[0]  # Get stored expiry time
            current_time = datetime.now()
            time_difference = stored_time - current_time

            # Check if time difference is less than 1 hour
            if time_difference.total_seconds() > 0:
                return True
       
        return False
    
    def update_password(self, token):
        try:
            # Get user_id using token
            query = """
            SELECT user_id FROM reset_password 
            WHERE reset_token = %s AND token_expiry > NOW()
            """
            self.mycursor.execute(query, (token,))
            result = self.mycursor.fetchone()
            
            if result:
                user_id = result[0]
                # Update password
                update_query = "UPDATE user SET user_password = %s WHERE id = %s"
                self.mycursor.execute(update_query, (self.password, user_id))
                
                # Delete used token
                delete_query = "DELETE FROM reset_password WHERE reset_token = %s"
                self.mycursor.execute(delete_query, (token,))
                
                self.mydb.commit()
                return True
                
            return False
            
        except Exception as e:
            print(f"Error updating password: {e}")
            return False

    # def show_details(self):
    #     print(self.mycursor.execute("select * from user;"))


if __name__ == "__main__":
    initilise = Database(email="jagat69133@prorsd.com", password="him")
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
