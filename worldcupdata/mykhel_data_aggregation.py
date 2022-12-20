import pandas as pd
import glob

files = glob.glob("mykhel_files/*")
# print(files)
pd.set_option('display.max_columns', None)

df_overview = pd.DataFrame(pd.read_csv("mykhel_files\mykhel_overview.csv"))
df_goals = pd.DataFrame(pd.read_csv("mykhel_files\mykhel_goals.csv"))
df1 = pd.merge(df_overview, df_goals, on=['PLAYER NAME', 'TEAM', 'MATCHES'], how='outer')

df_types_of_goals = pd.DataFrame(pd.read_csv("mykhel_files\mykhel_types_of_goals.csv"))
df2 = pd.merge(df1, df_types_of_goals, on=['PLAYER NAME', 'MATCHES', 'GOALS'], how='outer')

df_attempts = pd.DataFrame(pd.read_csv("mykhel_files\mykhel_attempts.csv"))
df3 = pd.merge(df2, df_attempts, on=['PLAYER NAME', 'MATCHES'], how='outer')

df_passes = pd.DataFrame(pd.read_csv("mykhel_files\mykhel_passes.csv"))
df4 = pd.merge(df3, df_passes, on=['PLAYER NAME', 'MATCHES'], how='outer')

df_defence = pd.DataFrame(pd.read_csv("mykhel_files\mykhel_defence.csv"))
df5 = pd.merge(df4, df_defence, on=['PLAYER NAME', 'TEAM'], how='outer')

df_disciplinary = pd.DataFrame(pd.read_csv("mykhel_files\mykhel_disciplinary.csv"))
df6 = pd.merge(df5, df_disciplinary, on=['PLAYER NAME', 'TEAM', 'MATCHES'], how='outer')

print(df6)
df6.to_csv("mykhel_files/mykhel.csv", index=False, header=True)
