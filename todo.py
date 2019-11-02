import click
import dateparser
from task import Task
import sqlite3
import os
import pandas as pd


def setup():
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE tasks
             (id INTEGER NOT NULL PRIMARY KEY,
             date datetime,
             task text NOT NULL,
             project_name text NOT NULL,
             habit BIT NOT NULL,
             increment INTEGER,
             completed BIT NOT NULL,
             FOREIGN KEY (project_name) references projects(project_name)
             );
             ''')
    c.execute('''
                CREATE TABLE projects
                (id INTEGER NOT NULL PRIMARY KEY,
                date datetime,
                project_name text NOT NULL)
            ''')
    c.execute('''CREATE TABLE tracker
                (date datetime PRIMARY KEY,
                count INTEGER);''')
    c.execute('''
                INSERT INTO projects (project_name) VALUES(?)
            ''', ('General', ))
    conn.commit()
    conn.close()


def add_db(task):
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''INSERT INTO tasks(date, task, project_name, habit, increment, completed) VALUES(?, ?, ?, ?, ?, ?)
             ''', (task.date, task.name, task.proj, task.habit, task.increment, False))
    conn.commit()
    conn.close()


def remove_db(task):
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''DELETE FROM tasks WHERE task = ?;
             ''', (task, ))
    conn.commit()
    conn.close()


def increment_count():
    check_current_count()
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''UPDATE tracker SET count = count + 1
                where date = date('now')
             ''')
    conn.commit()
    conn.close()


def decrement_count():
    check_current_count()
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''UPDATE tracker SET count = count - 1
                where date = date('now')
             ''')
    conn.commit()
    conn.close()


def check_current_count():
    conn = sqlite3.connect("todolist.db")
    pron = pd.read_sql("SELECT * FROM tracker where date = date('now')", conn)
    if pron.empty:
        c = conn.cursor()
        c.execute('''INSERT INTO tracker VALUES(date('now'), 0)
                 ''')
        conn.commit()
        conn.close()


@click.group()
def todo():
    pass


@click.command()
@click.option('--date', prompt="Date for todo task", help='Date when task is due, can be in words, ie tomorrow')
@click.option('--todo', prompt="What is your task?", help='Task to be completed')
@click.option('--project', default='General', help='Project task belongs to, default is general')
@click.option('--habit', is_flag=True, help='Is this a habit?')
def add(date, todo, project, habit):
    date = dateparser.parse(date)
    task = Task(date, todo)
    task.proj = project
    if habit:
        increment = click.prompt("How often do you want to do your habit?")
        task.habit = 1
        task.increment = increment
        add_db(task)
    else:
        task.habit = 0
        task.increment = None
        add_db(task)


@click.command()
@click.option('--todo', prompt='Which task do you want to remove?', help='Task to be removed')
def remove(todo):
    remove_db(todo)


@click.command()
@click.option('--day', 'period', flag_value='day', help='tasks for the day')
@click.option('--week', 'period', flag_value='week', help='tasks for the week')
@click.option('--month', 'period', flag_value='month', help='tasks for the month')
@click.argument('date', required=False)
def get(period, date):
    conn = sqlite3.connect("todolist.db")
    if not date:
        print(pd.read_sql('''SELECT * FROM tasks''', con=conn, index_col="id"))
    else:
        if period == 'day':
            print(pd.read_sql("SELECT * FROM tasks where date >= date(?) and date < date(?, '+1 days')",
                              params=[date, date], con=conn, index_col="id"))
        elif period == 'month':
            print(pd.read_sql("SELECT * FROM tasks where date >= date(?) and date < date(?, '+31 days')",
                              params=[date, date], con=conn, index_col="id"))
        else:
            print(pd.read_sql("SELECT * FROM tasks where date >= date(?) and date < date(?, '+7 days')",
                              params=[date, date], con=conn, index_col="id"))


@click.command()
def get_rec():
    conn = sqlite3.connect("todolist.db")
    rec_list = pd.read_sql("SELECT * FROM tasks where date >= date('now') and date < date('now', '+1 days') and completed = 0",
                           con=conn, index_col="id")
    if len(rec_list) >= 10:
        print(rec_list)
    else:
        rec_list_2 = pd.read_sql("SELECT * FROM tasks where date >= date('now', '+1 days') and date < date('now', '+2 days') and completed = 0 LIMIT ?;",
                                 params=[10 - len(rec_list)], con=conn, index_col="id")
        if len(rec_list_2) == 10 - len(rec_list):
            print(rec_list, rec_list_2)
        else:
            rec_list_3 = pd.read_sql("SELECT * FROM tasks where date >= date('now', '+2 days') or date is null LIMIT ?;",
                                     params=[10 - len(rec_list) - len(rec_list_2)], con=conn, index_col="id")
            print(pd.concat([rec_list, rec_list_2, rec_list_3]))


@click.command()
@click.option('--name', prompt="What is your project name?", help='name of the project')
@click.option('--date', default=None, help='date when project is due')
def add_proj(name, date):
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''INSERT INTO projects(date, project_name) VALUES(?, ?)
             ''', (date, name, ))
    conn.commit()
    conn.close()


@click.command()
def remove_proj(name):
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''DELETE FROM projects WHERE task = ?;
             ''', (name, ))
    conn.commit()
    conn.close()


@click.command()
def get_proj():
    conn = sqlite3.connect("todolist.db")
    print(pd.read_sql('''SELECT * FROM projects''', con=conn, index_col="id"))


@click.command()
@click.option('--task', prompt='What task did you complete?', help='task that is completed')
def complete(task):
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    completed = c.execute(
        '''SELECT completed FROM tasks where task = ?''', (task, )).fetchall()[0][0]
    if completed:
        increment_count()
    else:
        decrement_count()
    c.execute('''
        UPDATE tasks
        SET completed = 1 - completed
        WHERE task = ?;
    ''', (task, ))
    conn.commit()
    conn.close()


@click.command()
def clear():
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''
        DELETE FROM tasks WHERE completed = 1;
    ''')
    conn.commit()
    conn.close()


todo.add_command(add)
todo.add_command(remove)
todo.add_command(add_proj)
todo.add_command(remove_proj)
todo.add_command(get)
todo.add_command(get_proj)
todo.add_command(complete)
todo.add_command(clear)
todo.add_command(get_rec)


if __name__ == '__main__':
    if not os.path.isfile("todolist.db"):
        setup()
    todo()
