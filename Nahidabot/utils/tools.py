def rarity_rating(score: float, flag: str = "single") -> tuple[str, str]:
    """评分"""
    if flag == "total":
        score /= 5

    if score >= 55:
        return "PER", "Crimson"
    elif 50 <= score < 55:
        return "ACE", "DeepPink"
    elif 45 <= score < 50:
        return "UR", "OrangeRed"
    elif 40 <= score < 45:
        return "SSR", "Gold"
    elif 35 <= score < 40:
        return "SR", "Violet"
    elif 30 <= score < 35:
        return "R", "DeepSkyBlue"
    elif 25 <= score < 30:
        return "N", "LimeGreen"
    elif 0 <= score < 25:
        return "G", "white"
    else:
        return "UN", "#afafaf"
