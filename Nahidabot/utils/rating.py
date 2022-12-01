from typing import Optional


def rarity_rating(score:Optional[float])->str:
    if score is None:
        return "未评级"
    elif score == 60:
        return "P"
    elif score >= 55:
        return "ACE"
    elif 50<=score<55:
        return "UR"
    elif 45<=score<50:
        return "SSR"
    elif 40<=score<45:
        return "SR"
    elif 35<=score<40:
        return "R"
    elif 30<=score<35:
        return "N"
    else :
        return "G"
