from Services.state_manager import StateManager

state_manager = StateManager()

pet = state_manager.load_pet_state()

print("Pet State:")
print(pet)

pet["hunger"] += 10

state_manager.save_pet_state(pet)

print("\nUpdated Hunger:")
print(pet["hunger"])