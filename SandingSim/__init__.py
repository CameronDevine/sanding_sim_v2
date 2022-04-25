from .datalog import DataLog


class Sim(DataLog):
    test_article_thickness = 0.05
    test_article_radius = 0

    def __init__(self):
        super().__init__()
