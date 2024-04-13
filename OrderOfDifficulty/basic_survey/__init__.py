from otree.api import *


doc = """
demographic survey
"""


class C(BaseConstants):
    NAME_IN_URL = 'basic_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label = "1. How old are you?",
                                   min=12, max=120)
    gender = models.IntegerField(label = "2. What gender do you prefer to identify with?",
                                 choices = [[1,"Male"],[2,"Female"],[3,"Non-binary"],[99,"prefer not to say"]],
                                 widget=widgets.RadioSelectHorizontal)
    education = models.IntegerField(label = "3. What is your highest level of education?",
                                    choices = [[1,"No formal education"],[2,"Primary education"],[3,"Secondary education / High school"],
                                               [4,"Associate degree"],[5,"Bachelor's degree"],[6,"Master's degree"],
                                               [7,"Doctoral degree or higher"],[99,"prefer not to say"]],
                                    widget=widgets.RadioSelectHorizontal)
    marriage = models.IntegerField(label="4. What is your current marital status?",
                                 choices=[[1, "Single"], [2, "Married"], [3, "Divorced"], [4,"Widowed"],[5,"Separated"],
                                          [99, "prefer not to say"]], widget=widgets.RadioSelectHorizontal)
    familysize = models.IntegerField(label="5. How many members are there in your household?", min=1, max=20)
    income = models.IntegerField(label = "6. What is your approximate annual household income?",
                                 choices = [[1,"Less than $10K"],[2,"$10K-30K"],[3,"$30K-50K"],[4,"$50K-75K"],
                                            [5, "$75K-100K"],[6, "$100K-150K"],[7, "$150K-200K"],[8, "above 200K"],
                                            [99,"prefer not to say"]],
                                 widget=widgets.RadioSelectHorizontal)
    IQexperience  = models.BooleanField(label="7. Have you ever done IQ questions before?",
                                        choices=[[True, 'Yes'],[False, 'No']], widget=widgets.RadioSelect)
    stress = models.IntegerField(label = "8. On a scale of 1 to 10, how would you describe your stress level over the past two weeks? <br> (10=extremely stressful)", min=1, max=10)
    health = models.IntegerField(label="9. On a scale of 1 to 10, how would you rate your overall health condition during the past two weeks? <br> (10=extremely healthy)", min=1, max=10)

    # for Results
    luck = models.IntegerField()
    earned = models.FloatField()  # Final Total Payment in $




# PAGES
class Survey(Page):
    form_model = "player"
    form_fields = ["age", "gender", "education", "marriage", "familysize", "income", "IQexperience", "stress", "health"]


class Results(Page):
    form_model = 'player'

    def vars_for_template(self):
        chosen_round = self.participant.vars.get('chosen_round', None)
        app1_payoff = self.participant.vars.get('app1_payoff', 0)
        random_choice = self.participant.vars.get('random_choice',None)
        app2_payoff = self.participant.vars.get('app2_payoff', 0)

        import numpy as np
        luck = self.field_maybe_none('luck')
        if luck is None:
            self.luck = np.random.choice([1, 0], p=[0.2, 0.8])

        self.payoff= (app1_payoff + app2_payoff) * self.session.config['real_world_currency_per_point'] * self.luck + self.session.config['participation_fee']
        self.earned = float((app1_payoff + app2_payoff) * self.session.config['real_world_currency_per_point'] * self.luck + self.session.config['participation_fee'])
        # 30 points = $15

        return {
            'luck': self.luck,
            'chosen_round': chosen_round,
            'app1_payoff': app1_payoff,
            'random_choice': random_choice,
            'app2_payoff': app2_payoff,
            'total_payoff': app1_payoff + app2_payoff
        }



page_sequence = [Survey,Results]
