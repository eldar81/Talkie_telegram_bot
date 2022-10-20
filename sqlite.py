"""Code for operating SQLite database
This was my very first Python project so database structure and operations with data are written very bad
So do not think that such database structure is good example :)"""

import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name TEXT NOT NULL,
            Nickname TEXT,
            Bio_name TEXT,
            Bio_gender int,
            Bio_age int,
            Bio_hobby TEXT,
            Bio_companion_requirements int,
            is_ignore int DEFAULT 0 NOT NULL,
            is_banned int DEFAULT 0 NOT NULL,
            is_bot_banned int DEFAULT 0 NOT NULL,
            is_bot_paused int DEFAULT 0 NOT NULL,
            Send_to_Matches int,
            in_work int DEFAULT 0 NOT NULL,
            id_date int,
            meetings_done int DEFAULT 0 NOT NULL,
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)


    def create_table_match_gen(self):
        sql = """
        CREATE TABLE Match_gen (
            id_date TEXT NOT NULL,
            id int NOT NULL,
            date int,
            age int,
            gender int,
            req int,
            list_of_matches TEXT,
            amount_of_matches int,
            match int,
            id1_id2_date TEXT,
            PRIMARY KEY (id_date)
            );
"""
        self.execute(sql, commit=True)

    def create_table_final_matches(self):
        sql = """
            CREATE TABLE Matches (
                id1_id2_date TEXT NOT NULL,
                id1 int,
                id2 int,
                date int,
                notification_1 int,
                notification_2 int,
                get_task1 int,
                get_task2 int,
                task int,
                was_contact_1 int,
                was_contact_2 int,
                why_was_not_contact_1 int,
                why_was_not_contact_2 int,
                why_did_not_write_1 int,
                why_did_not_write_2 int,
                comment_why_did_not_write_1 TEXT,
                comment_why_did_not_write_2 TEXT,
                change_companion_1 int,
                change_companion_2 int,
                meeting_agreed_1 int,
                meeting_agreed_2 int,
                meeting_done_1 int,
                meeting_done_2 int,
                rate_meeting_1 int,
                rate_meeting_2 int,
                comment_meeting_1 TEXT,
                comment_meeting_2 TEXT,
                want_more_1 int,
                want_more_2 int,
                write_again_1 int,
                write_again_2 int,
                PRIMARY KEY (id1_id2_date)
                );
    """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, nickname: str):
        sql = """
        INSERT INTO Users(id, Name, Nickname) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, nickname), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_gen_matches(self):
        sql = """SELECT * FROM Match_gen"""
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_anketa(self, id, Bio_name, Bio_age, Bio_gender, Bio_hobby, Bio_companion_requirements):
        sql = f"""
        UPDATE Users SET Bio_name=?, Bio_age=?, Bio_gender=?, Bio_hobby=?, Bio_companion_requirements=? WHERE id=?
        """
        return self.execute(sql, parameters=(Bio_name, Bio_age, Bio_gender,
                                             Bio_hobby, Bio_companion_requirements, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


    def update_user_name(self, id, Bio_name):
        sql = f"""
        UPDATE Users SET Bio_name=? WHERE id=?
        """
        return self.execute(sql, parameters=(Bio_name, id), commit=True)


    def update_user_age(self, id, Bio_age):
        sql = f"""
        UPDATE Users SET Bio_age=? WHERE id=?
        """
        return self.execute(sql, parameters=(Bio_age, id), commit=True)

    def update_user_gender(self, id, Bio_gender):
        sql = f"""
        UPDATE Users SET Bio_gender=? WHERE id=?
        """
        return self.execute(sql, parameters=(Bio_gender, id), commit=True)


    def update_user_hobby(self, id, Bio_hobby):
        sql = f"""
        UPDATE Users SET Bio_hobby=? WHERE id=?
        """
        return self.execute(sql, parameters=(Bio_hobby, id), commit=True)


    def update_user_compreq(self, id, Bio_companion_requirements):
        sql = f"""
        UPDATE Users SET Bio_companion_requirements=? WHERE id=?
        """
        return self.execute(sql, parameters=(Bio_companion_requirements, id), commit=True)


    def update_user_send_to_Mathes(self, id):
        sql = f"""
         UPDATE Users SET Send_to_Matches=? WHERE id=?
         """
        return self.execute(sql, parameters=(1, id), commit=True)


    def update_user_id_date(self, id, date):
        sql = f"""
         UPDATE Users SET id_date=? WHERE id=?
         """
        return self.execute(sql, parameters=(date, id), commit=True)

    def transfer_users_to_Match_gen(self, id):
        sql = f"""
        INSERT INTO Match_gen(id_date, id, age, gender, req) SELECT id_date, 
        id, Bio_age, Bio_gender, Bio_companion_requirements FROM Users WHERE id=?
        """
        return self.execute(sql, parameters=id, commit=True)

    def set_date_to_transfered_users(self, date, id_date):
        sql = f"""
                 UPDATE Match_gen SET date=? WHERE id_date=?
                 """
        return self.execute(sql, parameters=(date, id_date), commit=True)


    def set_list_of_matches(self, list, id_date):
        sql = f"""
                 UPDATE Match_gen SET list_of_matches=? WHERE id_date=?
                 """
        return self.execute(sql, parameters=(list, id_date), commit=True)


    def set_amount_of_matches(self, amount, id_date):
        sql = f"""
                 UPDATE Match_gen SET amount_of_matches=? WHERE id_date=?
                 """
        return self.execute(sql, parameters=(amount, id_date), commit=True)


    def set_match(self, match, id_date):
        sql = f"""UPDATE Match_gen SET match=? WHERE id_date=?"""
        return self.execute(sql, parameters=(match, id_date), commit=True)


    def select_user_match(self, id_date):
        sql = f"""SELECT match FROM Match_gen WHERE id_date=?"""
        return self.execute(sql, parameters=id_date, fetchone=True)


    def transfer_matches_to_Match(self, id_date):
        sql = f"""
        INSERT INTO Matches(id1_id2_date, id1, id2, date) SELECT 
        id1_id2_date, id, match, date FROM Match_gen WHERE id_date=?
        """
        return self.execute(sql, parameters=id_date, commit=True)


    def set_id1_id2_date(self, id1_id2_date, id_date):
        sql = f"""UPDATE Match_gen SET id1_id2_date=? WHERE id_date=?"""
        return self.execute(sql, parameters=(id1_id2_date, id_date), commit=True)


    def select_all_matches(self):
        sql = """SELECT * FROM Matches"""
        return self.execute(sql, fetchall=True)


    def set_notification_1(self, id):
        sql = f"""UPDATE Matches SET notification_1=? WHERE id1=?"""
        return self.execute(sql, parameters=(1, id), commit=True)


    def set_notification_2(self, id):
        sql = f"""UPDATE Matches SET notification_2=? WHERE id2=?"""
        return self.execute(sql, parameters=(1, id), commit=True)


    def set_get_task1(self, id1_id2_date):
        sql = f"""UPDATE Matches SET get_task1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(1, id1_id2_date), commit=True)


    def set_get_task2(self, id1_id2_date):
        sql = f"""UPDATE Matches SET get_task2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(1, id1_id2_date), commit=True)


    def select_ids_from_matches(self, id):
        sql = f"""SELECT match FROM Match_gen WHERE id=?"""
        return self.execute(sql, parameters=id, fetchone=True)


    def update_in_work(self, id):
        sql = f"""UPDATE Users SET in_work=1 WHERE id=?"""
        return self.execute(sql, parameters=(id), commit=True)

    def select_match_for_task(self, id):
        sql = """SELECT * FROM Matches WHERE (id1=? or id2=?) 
        and date = (SELECT MAX(date) FROM Matches WHERE id1=? or id2=?)"""
        return self.execute(sql, parameters=(id, id, id, id), fetchall=True)


    def select_task_id(self, id1_id2_date):
        sql = f"""SELECT task FROM Matches WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=id1_id2_date, fetchone=True)

    def update_task(self, task_id, id1_id2_date):
        sql = f"""UPDATE Matches SET task=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(task_id, id1_id2_date), commit=True)


    def update_was_contact1(self, contact_status, id1_id2_date):
        sql = f"""UPDATE Matches SET was_contact_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(contact_status, id1_id2_date), commit=True)


    def update_was_contact2(self, contact_status, id1_id2_date):
        sql = f"""UPDATE Matches SET was_contact_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(contact_status, id1_id2_date), commit=True)


    def update_meeting_agreed_1(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET meeting_agreed_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_meeting_agreed_2(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET meeting_agreed_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_meeting_done_1(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET meeting_done_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_meeting_done_2(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET meeting_done_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_rate_meeting_1(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET rate_meeting_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_rate_meeting_2(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET rate_meeting_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)


    def update_want_more_1(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET want_more_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_want_more_2(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET want_more_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_in_work_0(self, id):
        sql = f"""UPDATE Users SET in_work=0 WHERE id=?"""
        return self.execute(sql, parameters=(id), commit=True)

    def update_is_bot_paused(self, status, id):
        sql = f"""UPDATE Users SET is_bot_paused=? WHERE id=?"""
        return self.execute(sql, parameters=(status, id), commit=True)

    def update_comment_meeting_1(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET comment_meeting_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_comment_meeting_2(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET comment_meeting_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_why_was_not_contact_1(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET why_was_not_contact_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_why_was_not_contact_2(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET why_was_not_contact_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_why_did_not_write_1(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET why_did_not_write_1=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def update_why_did_not_write_2(self, meeting_status, id1_id2_date):
        sql = f"""UPDATE Matches SET why_did_not_write_2=? WHERE id1_id2_date=?"""
        return self.execute(sql, parameters=(meeting_status, id1_id2_date), commit=True)

    def sql_update_function(self, table_in_db, column_in_table, parameter_in_column, where_column, where_parameter):
        sql = f"""UPDATE {table_in_db} SET {column_in_table}=? WHERE {where_column}=?"""
        return self.execute(sql, parameters=(parameter_in_column, where_parameter), commit=True)

def logger(statement):
    print(f"""
____     
Executing: 
{statement}
____
""")
