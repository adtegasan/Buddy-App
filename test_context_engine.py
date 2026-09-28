from Services.data_loader import DataLoader
from Engines.context_engine import ContextEngine

loader = DataLoader()
engine = ContextEngine()

data = loader.load_all()

context = engine.build_context(data)

print("\n=== WORK CONTEXT ===\n")

for key, value in context.items():
    print(f"{key}: {value}")