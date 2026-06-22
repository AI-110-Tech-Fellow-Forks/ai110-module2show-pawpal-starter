from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", email="jordan@email.com", available_time_minutes=90)

dog = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
cat = Pet(name="Mochi", species="cat", breed="Tabby", age=5)

owner.pets = [dog, cat]

# --- Tasks for Biscuit (dog) ---
dog_tasks = [
    Task("Morning walk",  duration_minutes=30, priority="high",   category="exercise"),
    Task("Feeding",       duration_minutes=10, priority="high",   category="feeding"),
    Task("Grooming",      duration_minutes=20, priority="medium", category="grooming"),
    Task("Fetch in yard", duration_minutes=15, priority="low",    category="enrichment"),
]

# --- Tasks for Mochi (cat) ---
cat_tasks = [
    Task("Feeding",    duration_minutes=10, priority="high",   category="feeding"),
    Task("Medication", duration_minutes=5,  priority="high",   category="medical"),
    Task("Playtime",   duration_minutes=20, priority="medium", category="enrichment"),
]

owner.tasks = dog_tasks + cat_tasks

# --- Build schedules ---
scheduler = Scheduler()

dog_schedule = scheduler.build_schedule(owner, dog, dog_tasks, time_available=60)
cat_schedule = scheduler.build_schedule(owner, cat, cat_tasks, time_available=30)

# --- Print ---
print(f"\nOwner: {owner.name}  |  Available time: {owner.get_available_time()} min\n")
print(dog_schedule.get_explanation())
print()
print(cat_schedule.get_explanation())
