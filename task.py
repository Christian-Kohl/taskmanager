import click


@click.command()
@click.option('--project')
@click.option('--habit', prompt='Is it a habit?', is_flag=True,
              help='Whether the task is a habit or not.')
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(habit, count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    if habit:
        click.echo("This is a habit")
    for x in range(count):
        click.echo('Hello %s!' % name)


if __name__ == '__main__':
    hello()
