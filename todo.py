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
             task text NOT NULL);
             ''')
    conn.commit()
    conn.close()


def add_db(task):
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''INSERT INTO tasks(date, task) VALUES(?, ?)
             ''', (task.date, task.name))
    conn.commit()
    conn.close()


def remove_db(task):
    conn = sqlite3.connect("todolist.db")
    c = conn.cursor()
    c.execute('''DELETE FROM tasks WHERE task = ?;
             ''', (task, ))
    conn.commit()
    conn.close()


@click.group()
def todo():
    pass


@click.command()
@click.option('--date', prompt="Date for todo task")
@click.option('--todo', prompt="What is your task?")
def add(date, todo):
    date = dateparser.parse(date)
    task = Task(date, todo)
    add_db(task)


@click.command()
@click.option('--todo', prompt='Which task do you want to remove?')
def remove(todo):
    remove_db(todo)


@click.command()
def get():
    conn = sqlite3.connect("todolist.db")
    print(pd.read_sql('''SELECT * FROM tasks''', con=conn, index_col="id"))


todo.add_command(add)
todo.add_command(remove)
todo.add_command(get)


if __name__ == '__main__':
    if not os.path.isfile("todolist.db"):
        setup()
    todo()
