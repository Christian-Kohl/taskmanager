class Task():

    def __init__(task_date, task_title):
        self.date = task_date
        self.title = task_title
        # self.desc = task_desc
        self.subtasks = []
        self.completed = False

    def check_completed():
        all([x.completed for x in self.subtasks])
