import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('./dataset/link_info.csv')
    print(df.loc[df['lecture'] == 'Lesson 1.1 Natural Language Content Analysis'].at[0, 'id'])
