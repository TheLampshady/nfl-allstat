import string
import random
from apps.data_hunter.configs.player_choices import \
    fantasy_position_list as fpl, team_code_list as tcl

TEST_AMOUNT = 100


def get_name(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def get_random_roster(player_amount):
    result = list()
    for _ in range(player_amount):
        first = get_name(random.randint(5, 7))
        last = get_name(random.randint(5, 7))

        result.append(
            dict(
                first_name=first,
                last_name=last,
                name=first+" "+last,
                position=fpl[random.randint(0, len(fpl)-1)],
                team=tcl[random.randint(0, len(tcl)-1)],
                jersey=random.randint(1, 99),
                bye_week=random.randint(1, 10),
            )
        )
    return result


player_one = dict(
    first_name="first",
    last_name="last",
    name="first last",
    position="wr",
    team="nyj",
    jersey=42,
    bye_week=9,
    image="https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Reddit_logo.svg/440px-Reddit_logo.svg.png"
)

player_one_double = dict(
    first_name="first",
    last_name="last",
    name="first last",
    position="wr",
    team="sea",
    jersey=42,
    bye_week=9,
)

player_two = dict(
    first_name="11111111",
    last_name="222222222",
    name="11111111 222222222",
    position="wr",
    team="nyj",
    jersey=42,
    bye_week=9,
    image="https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Reddit_logo.svg/440px-Reddit_logo.svg.png"
)

sport_roster = get_random_roster(TEST_AMOUNT)