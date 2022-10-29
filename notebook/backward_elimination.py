import pandas as pd
import statsmodels.api as sm

def backwardEliminationMLR(x, y, verbose=False):
    accept_coeff = 0.05

    flag = True
    model = sm.OLS(y, x).fit()
    
    if verbose:
        print('Variable p-value')
        print(model.pvalues)
        print(' ')
        
    while flag:
        max = -1

        for k in range(len(x.columns)):
            if k != 0:
                if model.pvalues[k] > accept_coeff:
                    if max != -1:
                        if model.pvalues[k] > model.pvalues[max]:
                            max = k
                    else:
                        max = k

        if max != -1:
            x = x.drop(x.columns[max], axis=1)
            model = sm.OLS(y, x).fit()
            
            if verbose:
                print(model.pvalues)
                print(' ')
        else:
            flag = False
            
    return model