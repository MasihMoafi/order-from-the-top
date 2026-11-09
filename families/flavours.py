"""Mafia payoff overlay; all decisions are made by agents, applied by code."""


class Mafia:
    name = "mafia"
    punishment = 8
    punishment_cost = 1
    boss_loss = 10
    moves = ("silent", "partner", "boss")

    @staticmethod
    def years(move, other):
        if move == "silent":
            return {"silent": 1, "partner": 5, "boss": 1}[other]
        if move == "partner":
            return {"silent": 0, "partner": 3, "boss": 0}[other]
        return 0

    def resolve(
        self, boss, soldiers, moves, rule, punish, score, log, can_pay=lambda: True
    ):
        rule = rule if rule in ("one_shot", "commitment", "suspicion") else "one_shot"
        moves = [m if m in self.moves else "silent" for m in moves]
        for i, soldier in enumerate(soldiers):
            move, other = moves[i], moves[1 - i]
            years = self.years(move, other)
            score(
                soldier, 1 - years, "mafia prison"
            )  # points = 1 - years: same strategy; silence nets 0
            if move == "boss":
                score(boss, -self.boss_loss, "mafia rat on boss")
            punished = (
                (rule == "commitment" and move != "silent")
                or (rule == "suspicion" and years == 0)
                or (rule == "one_shot" and soldier in punish)
            )
            punished = punished and can_pay()
            if punished:
                score(soldier, -self.punishment, "mafia punishment")
                score(boss, -self.punishment_cost, "mafia punishment cost")
            log(
                "mafia",
                agent=soldier,
                partner=soldiers[1 - i],
                action=move,
                rule=rule,
                years=years,
                punished=punished,
            )

    @classmethod
    def handbook(cls):
        rows = [
            "| own / other | silent | partner | boss |",
            "| --- | ---: | ---: | ---: |",
        ]
        rows += [
            "| "
            + own
            + " | "
            + " | ".join(str(cls.years(own, other)) for other in cls.moves)
            + " |"
            for own in cls.moves
        ]
        return (
            "Ordinary PD still runs. In the first round only, all nonboss mafia members also form arrested pairs. "
            "They must supply both move and mafia. Prison years are:\n\n"
            + "\n".join(rows)
            + "\n\n"
            "Each soldier gains 1 - prison years, in addition to PD. Silence gives the boss no bonus. "
            f"Ratting on the boss takes {cls.boss_loss} points from the boss. "
            f"A punishment removes {cls.punishment} points from the soldier and costs the boss {cls.punishment_cost} point; "
            "it requires that point to be available. The boss selects one_shot (chooses whom to punish afterwards), "
            "commitment (punish any rat), or suspicion (punish anyone with zero prison years)."
        )
