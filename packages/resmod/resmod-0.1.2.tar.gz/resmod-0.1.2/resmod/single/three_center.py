#!/usr/bin/python3

def three_center(v1, v2, v3):
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
    v3: array_like
        A third specified variable for interaction 


    Returns
    -------
    ndarray
        An array of centered residuals with the same length as v1, v2, and v3. 
        If different lengths then an error is returned

 
    Notes
    -----
    Centering residuals for interaction terms prevents violating assumptions of
    non correlated residuals in regression based methods.
    This allows the direct coefficiencts to be interpreted as though the
    interaction was not included in the model (little et al, 2006).


    Refereces
    --------
    Little, T. D., Bovaird, J. A., & Widaman, K. F. (2006).
    On the Merits of Orthogonalizing Powered and Product Terms:
    Implications for Modeling Interactions Among Latent Variables.
    Structural Equation Modeling, 13(4), 497-519.

 
 
    Examples
    --------
    Packages
        import statsmodels.formula.api as smf
        import statsmodels as smf
        from statsmodels import datasets
        import numpy as np
        import pandas as pd

    Getting data
        duncan_prestige = sms.datasets.get_rdataset("Duncan", "carData")
        income = duncan_prestige.data.income
        education = duncan_prestige.data.education
        prestige = duncan_prestige.data.prestige

    Creating dataframe
        v1 = np.array(income)
        v2 = np.array(education)
        v3 = np.array(prestige)
        dat = pd.DataFrame({"income": v1, "education" : v2, "prestige" : v3})

    Estimation 
        three_center(dat.income, dat.education, dat.prestige)

    Returns
        array([   4772.05291535,   26459.32115153,  118656.61598441,
                 -37602.92746188,   39198.74800491, -183237.27900063,
                  68109.7086619 ,  179924.56306499,  -74441.83220678,
                  73695.6901204 , -109189.83095442,  141359.82297104,
                  177970.64563484, -117125.8142879 ,  -73806.33993883,
                 -100431.84803594,  -84740.9280171 ,  -57765.85374726,
                 -79775.95213371,  105743.31343772, -124251.78934514,
                 -97082.16831786, -111230.4071848 ,  -58655.74398585,
                 -361.51790791,  -81021.85369737, -108014.98878415,
                 -72537.8799828 ,   13420.74269443,  -38094.78910029,
                 37781.22771986,  112011.20726695,  -24018.33539905,
                 81689.6355129 ,   60133.46303806,   24427.10708318,
                 25339.12889224,   44316.46929194,  103217.39026453,
                 48967.85766974,   49204.28630066,   43525.39900971,
                 87552.05115362,  -77821.44787679,   43733.07952156])
    """
    import statsmodels.formula.api as smf
    import numpy as np
    import pandas as pd
    mod = np.array(v1 * v2 * v3)
    v11 = np.array(v1)
    v22 = np.array(v2)
    v33 = np.array(v3)
    data = pd.DataFrame({"mod": mod, "v1": v11, "v2" : v22, "v3" : v33})
    three_cent = np.array(smf.ols(formula = "mod ~ v1 + v2 + v3", data=data).fit().resid)
    return(three_cent)
