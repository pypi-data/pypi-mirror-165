"""Utilities to transform data from one format/ontology/unit to another."""

import pandas as pd


def get_bmi(wt, ht):
    """Convert weight (kg) and height (cm) into BMI"""
    wt = wt[['Weight']].dropna().reset_index().groupby(wt.index.name
                                                      )['Weight'].median()
    ht = ht[['Height']].dropna().reset_index().groupby(ht.index.name
                                                      )['Height'].median()

    ht = ht / 100

    bmi = wt / (ht * ht)
    bmi = pd.DataFrame(bmi, columns=['bmi'])
    return bmi


def convert_icd_to_ccs(icd_code, version=10):
    pass
