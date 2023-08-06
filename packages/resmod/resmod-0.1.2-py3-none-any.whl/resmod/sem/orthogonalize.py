#!/usr/bin/python3

def orthogonalize(list1, list2, data):
    """ Extracts centered residuals for lists of interaction terms
        to be used in specifying a latent varaible interaction term.

    Author
    ------
    Drew E. Winters <drewEwinters@gmail.com>


    Parameters
    ----------
    list1: list or array of strings
           A list of column names of variables for interaction
    list2: list or array of strings
           A second list of column names of variables for interaction
    data: pandas dataframe
          A pandas dataframe


    Returns
    -------
    pandas dataframe
      A dataframe of centered residuals with names specified by names in
      list 1 and list 2 specifiying the interaction terms list1.list2


    Notes
    -----
    Centering residuals for interaction terms prevents violating assumptions
    of non correlated residuals in regression based methods.
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
      from resmod.sem import orthogonalize
      import statsmodels.formula.api as smf
      import statsmodels as sms
      from statsmodels import datasets
      import numpy as np
      import pandas as pd

    Getting data
      duncan_prestige = sms.datasets.get_rdataset("Duncan", "carData")
      income = duncan_prestige.data.income
      education = duncan_prestige.data.education

    Creating dataframe
      income = np.array(duncan_prestige.data.income)
      education = np.array(duncan_prestige.data.education)
      prestige = np.array(duncan_prestige.data.prestige)
      dat = pd.DataFrame({"income": income, "education": education, "prestige": prestige})

    Creating lists of column names for interactions
      l1 = ["income"]
      l2 = ["education", "prestige"]


    Estimation
      r = orthogonalize(l1, l2, dat)
      r.head()

    Returns
         income.education  income.prestige
      0         63.112648        34.246807
      1        229.849185       399.315757
      2        741.282854       732.789351
      3       -191.615460      -277.473163
      4        143.134978       276.041595
    """
    from resmod.single import residual_center
    val=[]
    name=[]
    for i in list1:
      for j in list2:
        name.append(i+"."+j)
        val.append(residual_center(np.array(data[i]), np.array(data[j])))
    df = pd.DataFrame(val).T
    df.columns = name
    return(df)
