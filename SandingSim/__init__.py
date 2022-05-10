from .datalog import DataLog


class Sim(DataLog):
    control = "force"

    def __init__(self):
        super().__init__()
        self.set_test_article("flat")
