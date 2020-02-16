import sqlite3

todo_db = 'database.db'
todo_conn = sqlite3.connect(todo_db)

todo_c = todo_conn.cursor()


class Database:
    """A sample Employee class"""

    def __init__(self, need, command, complete, completed):
        self.need = need
        self.command = command
        self.complete = complete
        self.completed = completed

    @property
    def user_one(self):
        return '{} {}'.format(self.need, self.command)


def insert_emp(emp):
    with todo_conn:
        todo_c.execute("INSERT INTO needs VALUES (:need, :command, :complete, :completed)",
                       {'need': emp.need, 'command': emp.command, 'complete': emp.complete, 'completed': emp.completed})


def remove_emp(emp):
    with todo_conn:
        todo_c.execute("DELETE from needs WHERE need= :need AND command = :command",
                       {'need': emp.need, 'command': emp.command})


def view_data():
    with todo_conn:
        todo_c.execute("SELECT * FROM needs")
        zlist = []
        items = todo_c.fetchall()
        for item in items:
            t = str(item[1]).replace('[', '') + " Created By: " + str(item[2]).replace('[',
                                                                                       '') + ":   Completed By: " + str(
                item[3]).replace('[', '')
            zlist.append(f'Needed: {t} ')

        new_string = str(zlist).replace("['", "").replace("]", "").replace("', ' ", '\n').replace("', '", '\n')
        return new_string


def update_complete(emp, completed):
    with todo_conn:
        todo_c.execute("""UPDATE needs SET completed = :completed
                     WHERE need = :need AND command = :command""",
                       {'need': emp.need, 'command': emp.command, 'completed': completed})
