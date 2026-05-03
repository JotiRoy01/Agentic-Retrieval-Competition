from agentic.data_loader import DataLoader
from agentic.data_loader import load, load_from_config

#loader = DataLoader()
law_df = load(filename="val.csv", nrows=1000)

#print(law_df.head())