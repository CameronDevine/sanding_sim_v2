from .datalog import DataLog


class Sim(DataLog):
    test_article = "curved"
    control = "force"

    def __init__(self):
        super().__init__()
