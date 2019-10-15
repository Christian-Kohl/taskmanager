import click
from tasks import Task


@click.group()
def task():
    pass

# Command to create a new task, or project
@click.command()
@click.option('--date', default="today")
@click.argument('task', nargs=-1)
def new(date, task):
    click.echo(date)
    click.echo(task)
    # t = Task(date, task)
    click.echo("Hello!")


# Returns the tasks for that day, if one is given, otherwise month, year, or other tasks also work, if not, then a summary is given of all tasks that are to be check_completed
# Maybe extend this to also work for whole projects, or extend it to work :D
@click.command()
def get():
    click.echo("Gello!")

# Returns a summary for the day, including recommended tasks
@click.command()
def summary():
    click.echo("This is a summary")


@click.Command
@click.argument('task')
def complete(task):
    task_list = dict()
    if task in task_list:
        task.complete()
    else:
        click.echo("That doesn't seem to be a task")


@click.Command
@click.argument('task')
def delete(task):
    task_list = dict()
    if task in task_list:
        task_list["task"] = None
    else:
        click.echo("That doesn't seem to be a task")


task.add_command(new)
task.add_command(get)
task.add_command(summary)

if __name__ == '__main__':
    task()
