from .Shougun import *


def dmg_info(prop: Role) -> list[DmgInfo]:
    if prop.talent:
        return eval(f"{prop.talent.abbr}(prop)")

    return []


def buff_info(prop: Role):
    if prop.talent:
        print(f"{prop.talent.abbr}_buff(prop)")
        return eval(f"{prop.talent.abbr}_buff(prop)")

    return []
