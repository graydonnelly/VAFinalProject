import pandas as pd

cc_data = pd.read_csv(r'~/Desktop/MC2/cc_data.csv')

locations = cc_data.location.unique()

print(locations)
print(len(locations))

