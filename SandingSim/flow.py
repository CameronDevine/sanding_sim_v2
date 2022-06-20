from .datalog import DataLog
import random
from .questionnaire import Questionnaire
from .sure import Sure
from .comments import Comments
from .slide import Slide, TextSlide


class Flow(DataLog):
    control_methods = ["force", "depth"]
    test_articles = ["flat", "curved"]

    def __init__(self):
        self.state = 0
        self.control = "force"
        self.states = [
            {"enter": self.start_experiment},
            {
                "enter": self.show_start,
                "enter_args": (
                    'Sanding Experiment:\n\nThis is an experiment to determine if an assistive feature of a sanding\nrobot is effective. This experiment should take under 10 minutes to complete.\n\nBy clicking "Start" you certify that you are at least 18 years of age.',
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "In this experiment your job is to remove the blue area\nof the part by controlling a sander.",
                    "start.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "As you sand the color will gradually change.",
                    "colorbar.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "When you are done, it should look like this.",
                    "goal.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "If you sand too much in an area, it will start to change to this color.",
                    "over.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "The sander can be moved to the left and right using the left joystick\non the controller.",
                    "up.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "By default, the sander hovers above the surface.",
                    "up.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "To start sanding, pull on the left trigger on the controller.",
                    "down.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    'Click next to start an example that you can use to get aquainted with the controls.\nPress "Reset" if you would like to start over and try again.',
                    "down.png",
                ),
                "exit": self.hide_slide,
            },
            {"enter": self.start_example},
            {
                "enter": self.show_text_slide,
                "enter_args": (
                    'There are four tests total, with a series of questions after each set of two.\n\nWhen you are ready to begin the recorded portion of the experiment, click "Next".',
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.start_trial,
                "enter_args": (0, 0, "A"),
                "exit": self.end_trial,
            },
            {
                "enter": self.start_trial,
                "enter_args": (0, 1, "B"),
                "exit": self.end_trial,
            },
            {
                "enter": self.show_questionnaire,
                "enter_args": ("A", "B"),
                "exit": self.save_responses,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "The next two tests use a different test article that is curved.",
                    "curved.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_slide,
                "enter_args": (
                    "This test article is less curved on the left and more curved on the right.",
                    "curved.png",
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.show_text_slide,
                "enter_args": (
                    'When you are ready to begin the next recorded portion\nof the experiment, click "Next"',
                ),
                "exit": self.hide_slide,
            },
            {
                "enter": self.start_trial,
                "enter_args": (1, 0, "C"),
                "exit": self.end_trial,
            },
            {
                "enter": self.start_trial,
                "enter_args": (1, 1, "D"),
                "exit": self.end_trial,
            },
            {
                "enter": self.show_questionnaire,
                "enter_args": ("C", "D"),
                "exit": self.save_responses,
            },
            {"enter": self.show_comments, "exit": self.save_comments},
            {
                "enter": self.show_text_slide,
                "enter_args": (
                    'Thank you for completing this experiment.\n\nClick "Next" to submit your responses and\nallow the next participant to complete the experiment.',
                ),
                "exit": self.hide_slide,
            },
            {"enter": self.save},
        ]
        super().__init__()
        self.sure = Sure(self.next)

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
                "Next": self.sure.show,
            }
        )

    def start_trial(self, experiment, test, index):
        self.toolbar.set_buttons(
            {
                "Next": self.sure.show,
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

    def show_slide(self, *args):
        self.slide = Slide(*args)
        self.toolbar.set_buttons(
            {
                "Next": self.next,
            }
        )
        self.toolbar.set_info("")

    def show_text_slide(self, *args):
        self.slide = TextSlide(*args)
        self.toolbar.set_buttons(
            {
                "Next": self.next,
            }
        )
        self.toolbar.set_info("")

    def show_start(self, *args):
        self.slide = TextSlide(*args)
        self.toolbar.set_buttons(
            {
                "Start": self.next,
            }
        )
        self.toolbar.set_info("")

    def hide_slide(self):
        self.slide.destroy()

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

    def show_comments(self):
        self.toolbar.set_buttons({"Next": self.next})
        self.comments = Comments()

    def save_comments(self):
        self.save_answers(self.comments.get_answers())
        self.comments.destroy()

    def save(self):
        self.upload_data()
        self.next()
