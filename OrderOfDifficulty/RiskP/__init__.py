from otree.api import *
import random

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'RiskP'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    left_side_amount = models.IntegerField(initial=10)
    switching_point_risk = models.IntegerField()



# PAGES
class Instruction2(Page):
    pass

class Risk(Page):
    form_model = 'player'
    form_fields = ['switching_point_risk']

    def vars_for_template(player: Player):
        return dict(right_side_amounts=range(0, 11, 1))

    def before_next_page(self, timeout_happened):
        if 'random_choice' not in self.participant.vars:
            self.participant.vars['random_choice'] = random.randint(1, 11)

        random_choice = self.participant.vars['random_choice']

        if self.switching_point_risk <= random_choice - 1:  # 0 ~ 10
                self.payoff += random_choice - 1
        else:
            blue = random.choice([0, 1])
            if blue == 1:
                self.payoff += cu(10)

        self.participant.vars['app2_payoff'] = float(self.payoff)



page_sequence = [Instruction2, Risk]
