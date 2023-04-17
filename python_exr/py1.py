import pandas as pd

# Creating an empty dataframe
df = pd.DataFrame(columns=['a', 'b'])

# Appending a row
df = df.append({ 'a': 1, 'b': 2 }, ignore_index=True)

