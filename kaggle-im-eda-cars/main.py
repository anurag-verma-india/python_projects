import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(color_codes=True)

df = pd.read_csv("./data.csv")

print(df.head(10))
