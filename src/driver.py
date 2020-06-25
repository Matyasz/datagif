import seaborn as sns
import numpy as np
import pandas as pd
import imageio
import matplotlib.pyplot as plt

sns.set_style(style="darkgrid")

def fancy_plot(x: str, y: str, t: str, data, fix_y: bool=False, fix_x: bool=False):

  """
    ooh if x is the same as t. then make sure to fill full plot and only 
    add new data as you go, so they don't need to super duplicate their data
  """
  time_values = np.sort(data[t].unique())

  for time in time_values:
    time_df = data.loc[data[t] == time]

    plot_args = {
      'x': x,
      'y': y,
      'data': time_df
    }
    
    # sns.lmplot(**plot_args)
    sns.relplot(**plot_args)

    if fix_x:
      plt.xlim(data[x].min(), data[x].max())
    if fix_y:
      plt.ylim(data[y].min(), data[y].max())

  plt.show()


dfs = []
n = 20
t = 3

for times in range(1, t + 1):
  data = [5 + (times * i) + (2 * np.random.normal()) for i in range(n)]
  xval = [i for i in range(n)]
  time = [times for _ in range(n)]

  dfs.append(
      pd.DataFrame({
      'time': time,
      'xval': xval,
      'yval': data
    })
  )

df = pd.concat(dfs, ignore_index=True)
# print(df)
fancy_plot(
  x='xval', y='yval', t='time',
  data=df,
  fix_x=True, fix_y=True
)
