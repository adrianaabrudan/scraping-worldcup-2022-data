import pandas as pd
import re

file_name = "fbref.csv"


def clean_data(file_name):
    df = pd.read_csv(file_name)
    df['Squad'] = [i.split(' ', 1)[1] for i in df['Squad']]
    df['Age'] = [i.split('-')[0] for i in df['Age']]
    df['Club'] = [str(i).split(' ', 1)[1] if len(str(i).split(' ', 1)) == 2 else i for i in df['Club']]

    return df


if __name__ == "__main__":
    print(clean_data(file_name))
