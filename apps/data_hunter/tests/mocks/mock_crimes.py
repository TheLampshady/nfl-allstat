from datetime import datetime

two_category_crime = {
    "category":[
        "animal cruelty",
        "drugs"
    ],
    "description": "charged with two felony counts of aggravated animal cruelty after "
                   "one of his dogs died, illegal possession of alligator and marijuana.",
    "date_recorded": "2015-02-02",
    "pos": "dt",
    "case_type": "indicted",
    "team": "bal",
    "outcome": "released by team the same day. resolution undetermined.",
    "name": "first last"
}

one_category_crime = {
    "category": [
        "assault"
    ],
    "description": "accused of hitting a pizza delivery driver in the head in a "
                   "dispute over a parking space in washington, d.c.",
    "date_recorded": "2015-02-03",
    "pos": "lb",
    "case_type": "arrested",
    "team": "ind",
    "outcome": "resolution undetermined.",
    "name": "first last"
}

one_crime_mock = dict(
    player_id=1,
    date_recorded=datetime.strptime("2015-02-03", "%Y-%m-%d").date(),
    case_type="arrested",
    category=["assault"],
    description="accused of hitting a pizza delivery driver in the head in a dispute "
                "over a parking space in washington, d.c.",
    outcome="resolution undetermined."
)
