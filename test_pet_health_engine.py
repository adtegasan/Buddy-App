from Services.data_loader import DataLoader
from Engines.context_engine import ContextEngine
from Engines.pet_health_engine import PetHealthEngine

loader = DataLoader()
context_engine = ContextEngine()
health_engine = PetHealthEngine()

data = loader.load_all()

context = context_engine.build_context(data)

health = health_engine.calculate_pet_health(context)

print("\n=== WORK CONTEXT ===\n")

for key, value in context.items():
    print(f"{key}: {value}")

print("\n=== PET HEALTH ===\n")

for key, value in health.items():
    print(f"{key}: {value}")