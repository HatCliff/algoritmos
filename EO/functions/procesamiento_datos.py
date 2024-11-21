import pandas as pd
def leer_data(entrada):
    data = pd.read_csv(entrada, header=None)
    return data 