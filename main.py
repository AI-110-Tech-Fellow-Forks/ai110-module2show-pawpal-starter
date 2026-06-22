from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", email="jordan@email.com", available_time_minutes=90)

dog = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
cat = Pet(name="Mochi", species="cat", breed="Tabby", age=5)

owner.pets = [dog, cat]

# --- Tasks added out of order on purpose ---
all_tasks = [
    Task("Afternoon walk",  duration_minutes=20, priority="medium", category="exercise",    pet_name="Biscuit"),
    Task("Medication",      duration_minutes=5,  priority="high",   category="medical",     pet_name="Mochi"),
    Task("Morning walk",    duration_minutes=30, priority="high",   category="exercise",    pet_name="Biscuit"),
    Task("Playtime",        duration_minutes=20, priority="medium", category="enrichment",  pet_name="Mochi"),
    Task("Feeding",         duration_minutes=10, priority="high",   category="feeding",     pet_name="Biscuit"),
    Task("Grooming",        duration_minutes=20, priority="medium", category="grooming",    pet_name="Biscuit"),
    Task("Feeding",         duration_minutes=10, priority="high",   category="feeding",     pet_name="Mochi"),
    Task("Fetch in yard",   duration_minutes=15, priority="low",    category="enrichment",  pet_name="Biscuit"),
]

# Set required_time_window on a few tasks to demo sort_by_time
all_tasks[2].required_time_window = "08:00"  # Morning walk
all_tasks[0].required_time_window = "14:00"  # Afternoon walk
all_tasks[4].required_time_window = "09:00"  # Feeding (Biscuit)

# Mark one task complete to demo filtering
all_tasks[6].mark_complete()  # Mochi's Feeding already done

owner.tasks = all_tasks

scheduler = Scheduler()

# --- Filter by pet ---
print("=" * 45)
print("All tasks split by pet:")
biscuit_tasks = scheduler.filter_tasks(all_tasks, pet_name="Biscuit")
mochi_tasks   = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
print(f"  Biscuit: {[t.title for t in biscuit_tasks]}")
print(f"  Mochi:   {[t.title for t in mochi_tasks]}")

# --- Filter by completion ---
print("\nCompletion status:")
pending   = scheduler.filter_tasks(all_tasks, completed=False)
completed = scheduler.filter_tasks(all_tasks, completed=True)
print(f"  Pending ({len(pending)}):   {[t.title + ' (' + t.pet_name + ')' for t in pending]}")
print(f"  Completed ({len(completed)}): {[t.title + ' (' + t.pet_name + ')' for t in completed]}")

# --- Sort Biscuit's tasks by time window ---
print("\nBiscuit's tasks sorted by time window:")
sorted_biscuit = scheduler.sort_by_time(biscuit_tasks)
for t in sorted_biscuit:
    window = t.required_time_window if t.required_time_window else "no window"
    print(f"  [{window}]  {t.title}")

# --- Build and print schedules ---
print()
dog_schedule = scheduler.build_schedule(owner, dog, biscuit_tasks, time_available=60)
cat_schedule = scheduler.build_schedule(owner, cat, mochi_tasks,   time_available=30)

print(dog_schedule.get_explanation())
print()
print(cat_schedule.get_explanation())
