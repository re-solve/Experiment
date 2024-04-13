import random
from otree.api import *

doc = """
IQ test
"""


class C(BaseConstants):
    NAME_IN_URL = 'IQ_test'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 15

    tasks = ['E', 'M', 'D']
    num_tasks_per_type = 5
    CORRECT_ANSWERS = {
        'E_1': 1, 'E_2': 5, 'E_3': 6, 'E_4': 6, 'E_5': 4,
        'M_1': 6, 'M_2': 2, 'M_3': 4, 'M_4': 3, 'M_5': 1,
        'D_1': 4, 'D_2': 1, 'D_3': 5, 'D_4': 1, 'D_5': 4
    }


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    group_type = models.StringField()
    current_task_id = models.StringField()

    # IQ test and Estimation
    Answer = models.IntegerField(label="Which one do you think is the correct answer?",
                                 choices=[[1, "A"], [2, "B"], [3, "C"], [4, "D"], [5, "E"], [6, "F"]],
                                 widget=widgets.RadioSelectHorizontal)
    Conf_Estimation = models.IntegerField(min=0, max=100, initial=None)
    Conf_Group = models.IntegerField(min=0, max=100, initial=None)

    # Fatigue level
    Fatigue = models.IntegerField(label = "On a scale of 1 to 10, how tired do you feel now?", min=1, max=10)



# FUNCTIONS:
# Helper function to assign task based on round number and group type
def assign_task_id(player: Player, round_number):
    group_type = player.participant.vars.get('group_type', None)
    task_mapping = {
        'DTE': {range(1, 6): 'D', range(6, 11): 'M', range(11, 16): 'E'},
        'ETD': {range(1, 6): 'E', range(6, 11): 'M', range(11, 16): 'D'},
    }

    for range_key, task in task_mapping[group_type].items():
        if round_number in range_key:
            task_index = (round_number - 1) % 5 + 1
            player.current_task_id = f"{task}_{task_index}"
            break

# randomized treatment
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            player.participant.vars['group_type'] = random.choice(['DTE', 'ETD'])
            player.group_type = player.participant.vars['group_type']

        assign_task_id(player, subsession.round_number)



# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Instruction1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Question(Page):
    form_model = 'player'
    timeout_seconds = 120

    @staticmethod
    def is_displayed(player: Player):
        return True

    def get_form_fields(self):
        return ['Answer']

    def vars_for_template(self):
        path = f"IQ_Q/{self.current_task_id}.jpg"
        return {'image_path': path}


class Confidence(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['Conf_Estimation', 'Conf_Group']


class Fatigue(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number % 5 == 0

    def get_form_fields(self):
        return ['Fatigue']


    def before_next_page(self, timeout_happened):
        if self.round_number == C.NUM_ROUNDS:
            chosen_round = random.randint(1, 15)
            chosen_round_payoff = None
            for p in self.in_all_rounds():
                if p.round_number == chosen_round:
                    p.participant.vars['chosen_round'] = chosen_round
                    chosen_task_id = p.current_task_id
                    correct_answer = int(C.CORRECT_ANSWERS.get(chosen_task_id))

                    if p.Answer == correct_answer:
                        p.payoff += cu(10)
                        p.payoff += cu(10) * p.Conf_Estimation / 100
                    else:
                        p.payoff += cu(0)
                        p.payoff += cu(10) * (1 - p.Conf_Estimation / 100)

                    chosen_round_payoff = float(p.payoff)

            if chosen_round_payoff is not None:
                p.participant.vars['app1_payoff'] = chosen_round_payoff


page_sequence = [Introduction, Instruction1, Question, Confidence, Fatigue]
