class Task():

    def __init__(self, date, name):
        self.date = date
        self.name = name

    def update_name(self, name):
        self.name = name

    def update_date(self, date):
        self.date = date
