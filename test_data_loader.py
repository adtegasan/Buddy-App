from Services.data_loader import DataLoader

loader = DataLoader()

data = loader.load_all()

print("\n=== DATASETS LOADED ===\n")

for name, dataframe in data.items():
    print(f"{name}:")
    print(dataframe)
    print("\n")