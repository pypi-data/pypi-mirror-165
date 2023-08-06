#!/usr/bin/python3


import pytest
from resmod.single.residual_center import residual_center


def test_residual_center():
    # packages
    import statsmodels.formula.api as smf
    import statsmodels as sms
    from statsmodels import datasets
    import numpy as np
    import pandas as pd
    # downloading data
    duncan_prestige = sms.datasets.get_rdataset("Duncan", "carData")
    income = duncan_prestige.data.income
    education = duncan_prestige.data.education
    # dataframe
    v1 = np.array(income)
    v2 = np.array(education)
    dat = pd.DataFrame({"income": v1, "education": v2})
    # testing
    assert residual_center(dat.income, dat.education).all() == np.array([
        63.11264837,   229.8491846 ,   741.28285426,  -191.61545996,
        143.13497759, -1522.02012271,   250.49755451,  1222.03876523,
        281.50598242,   463.22429449,  -657.16077574,   951.3190848 ,
        923.98157381,  -761.79683046,  -500.35610126,  -798.28161848,
        -474.82578368,  -357.03501052,  -457.2861054 ,   585.94123821,
        -981.98093767,  -476.50649685,  -312.02816875,  -549.40617942,
        165.39170698,  -458.91783728, -1052.25086135,  -293.40322494,
        169.06536061,  -372.67648496,   101.34978524,  1153.8352266 ,
        -337.3613032 ,   599.90768769,   386.69161908,   248.37917402,
        182.34841689,   117.02343887,   679.23266571,   360.97604371,
        115.6538024 ,   194.02207051,   612.22286945,  -485.36288933,
        98.28416593]).all()
