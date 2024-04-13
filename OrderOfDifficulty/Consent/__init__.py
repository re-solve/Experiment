from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(1000)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    prolific_id = models.StringField(label="Please provide your PROLIFIC ID")

    consent = models.BooleanField(default=0)


# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

class Consent_Form(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def before_next_page(player, timeout_happened):

        player.participant.label = player.prolific_id

class No_Consent(Page):
    @staticmethod
    def is_displayed(player):
        return player.consent == 0



page_sequence = [Welcome, Consent_Form, No_Consent]
