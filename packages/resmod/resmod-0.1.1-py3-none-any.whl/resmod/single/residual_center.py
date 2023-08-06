#!/usr/bin/python3


def residual_center(v1, v2):
    """ Extracts centered residuals for specified interaction term
    to be used in any regression frame work (e.g., ols, rlm, etc.).


    Author
    ------
    Drew E. Winters <drewEwinters@gmail.com>


    Parameters
    ----------
    v1: array_like
        A specified variable for interaction
    v2: array_like
        A second specified variable for interaction


    Returns
    -------
    ndarray
        An array of centered residuals with the same length as v1 and v2.
        If v1 and v2 are different lengths then an error is returned.


    Notes
    -----
    Centering residuals for interaction terms prevents violating assumptions
        of non correlated residuals in regression based methods.
    This allows the direct coefficiencts to be interpreted as though
        the interaction was not included in the model (little et al, 2006).


    Refereces
    --------
    Little, T. D., Bovaird, J. A., & Widaman, K. F. (2006).
    On the Merits of Orthogonalizing Powered and Product Terms:
    Implications for Modeling Interactions Among Latent Variables.
    Structural Equation Modeling, 13(4), 497-519.


    Examples
    --------
    Packages
        from resmod.single import residual_center         #for orthogonalizing
        import statsmodels.formula.api as smf             #for estimation
        import statsmodels as sms
        from statsmodels import datasets                  #for importing data
        import numpy as np                                #for data structring
        import pandas as pd                               #for dataframe

    Getting data
        duncan_prestige = sms.datasets.get_rdataset("Duncan", "carData")
        income = duncan_prestige.data.income
        education = duncan_prestige.data.education

    Creating dataframe
        v1 = np.array(income)                             #v1 as an array
        v2 = np.array(education)                          #v2 as an array
        dat = pd.DataFrame({"income": v1, "education" : v2})

    Estimation
        residual_center(dat.income, dat.education)

    Returns
        array([  63.11264837,    229.8491846,    741.28285426,  -191.61545996,
                 143.13497759,  -1522.02012271,  250.49755451,   1222.03876523,
                 281.50598242,   463.22429449,  -657.16077574,   951.3190848 ,
                 923.98157381,  -761.79683046,  -500.35610126,  -798.28161848,
                -474.82578368,  -357.03501052,  -457.2861054 ,   585.94123821,
                -981.98093767,  -476.50649685,  -312.02816875,  -549.40617942,
                 165.39170698,  -458.91783728,  -1052.25086135, -293.40322494,
                 169.06536061,  -372.67648496,   101.34978524,   1153.8352266,
                -337.3613032,    599.90768769,   386.69161908,   248.37917402,
                 182.34841689,   117.02343887,   679.23266571,   360.97604371,
                 115.6538024,    194.02207051,   612.22286945,  -485.36288933,
                 98.28416593]
                 )
    """
    import statsmodels.formula.api as smf
    import numpy as np
    import pandas as pd
    mod = np.array(v1 * v2)
    v11 = np.array(v1)
    v22 = np.array(v2)
    data = pd.DataFrame({"mod": mod, "v1": v11, "v2": v22})
    res_cent = np.array(smf.ols(formula="mod ~ v1 + v2",
                                data=data).fit().resid)
    return(res_cent)
