# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python3 -m pytest:

```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run `python3 main.py` to see the scheduler in action from the terminal:

```
=============================================
All tasks split by pet:
  Biscuit: ['Afternoon walk', 'Morning walk', 'Feeding', 'Grooming', 'Fetch in yard']
  Mochi:   ['Medication', 'Playtime', 'Feeding']

Completion status:
  Pending (7):   ['Afternoon walk (Biscuit)', 'Medication (Mochi)', 'Morning walk (Biscuit)',
                  'Playtime (Mochi)', 'Feeding (Biscuit)', 'Grooming (Biscuit)', 'Fetch in yard (Biscuit)']
  Completed (1): ['Feeding (Mochi)']

Biscuit's tasks sorted by time window:
  [08:00]  Morning walk
  [09:00]  Feeding
  [14:00]  Afternoon walk
  [no window]  Grooming
  [no window]  Fetch in yard

Today's Schedule — Biscuit (dog)
========================================
  08:00–08:30  Morning walk (30 min) [high]
             Included: priority=high, duration=30 min
  08:30–08:40  Feeding (10 min) [high]
             Included: priority=high, duration=10 min
  08:40–09:00  Afternoon walk (20 min) [medium]
             Included: priority=medium, duration=20 min
========================================
  Total time: 60 / 60 min used

Today's Schedule — Mochi (cat)
========================================
  08:00–08:05  Medication (5 min) [high]
             Included: priority=high, duration=5 min
  08:05–08:15  Feeding (10 min) [high]
             Included: priority=high, duration=10 min
========================================
  Total time: 15 / 30 min used
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python3 -m pytest tests/test_pawpal.py -v
```

Sample test output:

```
collected 13 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED
tests/test_pawpal.py::test_daily_task_creates_next_occurrence_on_complete PASSED
tests/test_pawpal.py::test_weekly_task_creates_next_occurrence_on_complete PASSED
tests/test_pawpal.py::test_non_recurring_task_returns_none_on_complete PASSED
tests/test_pawpal.py::test_complete_task_appends_next_occurrence_to_list PASSED
tests/test_pawpal.py::test_check_for_conflicts_detects_overlap_within_schedule PASSED
tests/test_pawpal.py::test_check_for_conflicts_returns_empty_when_no_overlap PASSED
tests/test_pawpal.py::test_detect_conflicts_catches_cross_pet_overlap PASSED
tests/test_pawpal.py::test_detect_conflicts_no_warnings_when_schedules_dont_overlap PASSED
tests/test_pawpal.py::test_filter_tasks_by_completion_status PASSED
tests/test_pawpal.py::test_filter_tasks_by_pet_name PASSED
tests/test_pawpal.py::test_sort_by_time_orders_tasks_by_time_window PASSED

============================== 13 passed in 0.01s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by `required_time_window` (HH:MM); tasks with no window sort last via `"99:99"` sentinel |
| Priority filtering | `Scheduler.prioritize_tasks()` + `fit_tasks()` | Greedy selection — high-priority tasks fill the budget first; lower-priority tasks are dropped if time runs out |
| Task filtering | `Scheduler.filter_tasks()` | Filter by completion status (`completed=True/False`), pet name, or both combined |
| Conflict handling | `DailySchedule.check_for_conflicts()`, `Scheduler.detect_conflicts()` | Returns warning strings for overlapping slots within a pet's schedule and across different pets |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.complete_task()` | Marks done and returns a fresh copy with `due_date + 1` or `+ 7` days; non-recurring tasks return `None` |

## 📸 Demo Walkthrough

The Streamlit app (`streamlit run app.py`) lets a user plan a full day of pet care in five steps:

1. **Enter owner info** — type the owner's name and set the total minutes available for pet care that day (e.g., 90 minutes).

2. **Enter pet info** — type the pet's name and select a species from the dropdown (dog, cat, or other).

3. **Add tasks** — for each care activity, fill in the title, duration, priority, and an optional time window (`HH:MM`). Click "Add task" to append it to the session list. Tasks appear in a live table below the form.

4. **Generate the schedule** — click the "Generate schedule" button. The Scheduler runs the full pipeline: sorts tasks by time window, prioritizes by importance, fits as many as possible into the available time, and assigns sequential start/end times starting at 08:00. The page then shows:
   - A **sorted task table** in chronological order by time window
   - A **schedule table** with start time, end time, task name, duration, and priority for every task that fit
   - A green **success banner** showing total minutes used out of the available budget
   - A **conflict check** — green banner if no overlaps, amber warning banners (one per conflict) naming both tasks and their times
   - A **"Tasks that didn't fit"** table listing anything the time budget couldn't accommodate

5. **Start over** — click "Clear all tasks" to reset and plan a new day.
