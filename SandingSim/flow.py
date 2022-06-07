from .datalog import DataLog
import random
from .questionnaire import Questionnaire


class Flow(DataLog):
    control_methods = ["force", "depth"]
    test_articles = ["flat", "curved"]

    def __init__(self):
        self.state = 0
        self.control = "force"
        self.states = [
            {"enter": self.start_experiment},
            {"enter": self.start_example},
            {"enter": self.start_trial, "enter_args": (0, 0), "exit": self.end_trial},
            {"enter": self.start_trial, "enter_args": (0, 1), "exit": self.end_trial},
            {
                "enter": self.show_questionnaire,
                "enter_args": ("A", "B"),
                "exit": self.save_responses,
            },
            {"enter": self.start_trial, "enter_args": (1, 0), "exit": self.end_trial},
            {"enter": self.start_trial, "enter_args": (1, 1), "exit": self.end_trial},
            {
                "enter": self.show_questionnaire,
                "enter_args": ("C", "D"),
                "exit": self.save_responses,
            },
        ]
        super().__init__()

    def start_flow(self):
        self.states[self.state]["enter"](*self.states[self.state].get("enter_args", []))

    def next(self):
        if "exit" in self.states[self.state]:
            self.states[self.state]["exit"]()
        self.state += 1
        if self.state >= len(self.states):
            self.state = 0
        self.states[self.state]["enter"](*self.states[self.state].get("enter_args", []))

    def start_experiment(self):
        self.order = [
            self.control_methods[:: random.randrange(-1, 2, 2)] for i in range(2)
        ]
        self.init_data()
        self.next()

    def start_example(self):
        self.control = "force"
        self.set_test_article("flat")
        self.reset()
        self.toolbar.set_buttons(
            {
                "Reset": self.reset,
                "Next": self.next,
            }
        )

    def start_trial(self, experiment, test):
        self.toolbar.set_buttons(
            {
                "Next": self.next,
            }
        )
        self.toolbar.set_info("Test {}".format(index))
        self.control = self.order[experiment][test]
        self.set_test_article(self.test_articles[experiment])
        self.log_next_experiment()
        self.reset()
        self.log_active = True

    def end_trial(self):
        self.log_active = False
        self.toolbar.set_info("")

    def show_questionnaire(self, *labels):
        self.toolbar.set_buttons(
            {
                "Next": self.next,
            }
        )
        self.toolbar.disable()
        self.questionnaire = Questionnaire(
            [
                statement.format(*labels)
                for statement in (
                    "In test {} I was able to produce a better end result than in test {}.",
                    "I was able to complete test {} faster than I was able to complete test {}.",
                    "In test {} I was able to more precisely remove material than in test {}.",
                    "I found sanding in test {} was more intuitive than in test {}.",
                    "I preferred the operation of the sander in test {} over test {}.",
                )
            ]
        )
        self.taskMgr.add(self.check_complete, "Check Complete")

    def check_complete(self, task):
        if self.questionnaire.complete():
            self.toolbar.enable()
            return task.done
        else:
            return task.cont

    def save_responses(self):
        self.save_answers(self.questionnaire.get_answers())
        self.questionnaire.destroy()
