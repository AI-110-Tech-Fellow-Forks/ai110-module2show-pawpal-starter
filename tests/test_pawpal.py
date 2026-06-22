import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Scheduler, DailySchedule, ScheduledTask


def test_mark_complete_changes_status():
    task = Task("Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feeding", duration_minutes=10, priority="high"))
    pet.add_task(Task("Grooming", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 2


def test_daily_task_creates_next_occurrence_on_complete():
    task = Task("Feeding", duration_minutes=10, priority="high", pet_name="Biscuit", recurrence="daily")
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.title == "Feeding"
    assert next_task.recurrence == "daily"
    assert next_task.due_date == task.due_date + timedelta(days=1)


def test_weekly_task_creates_next_occurrence_on_complete():
    task = Task("Grooming", duration_minutes=20, priority="medium", pet_name="Biscuit", recurrence="weekly")
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is not None
    assert next_task.recurrence == "weekly"
    assert next_task.due_date == task.due_date + timedelta(days=7)


def test_non_recurring_task_returns_none_on_complete():
    task = Task("Vet visit", duration_minutes=60, priority="high")
    result = task.mark_complete()
    assert task.completed is True
    assert result is None


def test_complete_task_appends_next_occurrence_to_list():
    task = Task("Feeding", duration_minutes=10, priority="high", recurrence="daily")
    task_list = [task]
    scheduler = Scheduler()
    scheduler.complete_task(task, task_list)
    assert len(task_list) == 2
    assert task_list[0].completed is True
    assert task_list[1].completed is False


def test_check_for_conflicts_detects_overlap_within_schedule():
    schedule = DailySchedule(date="today", total_time_available=60)
    walk = Task("Morning walk", duration_minutes=30, priority="high", pet_name="Biscuit")
    feed = Task("Feeding",      duration_minutes=20, priority="high", pet_name="Biscuit")
    # Both start at 08:00 — guaranteed overlap
    schedule.add_task(ScheduledTask(walk, "08:00", "08:30"))
    schedule.add_task(ScheduledTask(feed, "08:00", "08:20"))
    warnings = schedule.check_for_conflicts()
    assert len(warnings) == 1
    assert "WARNING" in warnings[0]


def test_check_for_conflicts_returns_empty_when_no_overlap():
    schedule = DailySchedule(date="today", total_time_available=60)
    walk = Task("Morning walk", duration_minutes=30, priority="high", pet_name="Biscuit")
    feed = Task("Feeding",      duration_minutes=10, priority="high", pet_name="Biscuit")
    schedule.add_task(ScheduledTask(walk, "08:00", "08:30"))
    schedule.add_task(ScheduledTask(feed, "08:30", "08:40"))
    assert schedule.check_for_conflicts() == []


def test_detect_conflicts_catches_cross_pet_overlap():
    scheduler = Scheduler()
    dog_schedule = DailySchedule(date="Biscuit (dog)", total_time_available=60)
    cat_schedule = DailySchedule(date="Mochi (cat)",   total_time_available=60)
    walk = Task("Morning walk", duration_minutes=30, priority="high", pet_name="Biscuit")
    meds = Task("Medication",   duration_minutes=10, priority="high", pet_name="Mochi")
    # Both scheduled at 08:00 — owner can't do both at once
    dog_schedule.add_task(ScheduledTask(walk, "08:00", "08:30"))
    cat_schedule.add_task(ScheduledTask(meds, "08:00", "08:10"))
    warnings = scheduler.detect_conflicts([dog_schedule, cat_schedule])
    assert any("Biscuit" in w and "Mochi" in w for w in warnings)


def test_detect_conflicts_no_warnings_when_schedules_dont_overlap():
    scheduler = Scheduler()
    dog_schedule = DailySchedule(date="Biscuit (dog)", total_time_available=60)
    cat_schedule = DailySchedule(date="Mochi (cat)",   total_time_available=60)
    walk = Task("Morning walk", duration_minutes=30, priority="high", pet_name="Biscuit")
    meds = Task("Medication",   duration_minutes=10, priority="high", pet_name="Mochi")
    dog_schedule.add_task(ScheduledTask(walk, "08:00", "08:30"))
    cat_schedule.add_task(ScheduledTask(meds, "08:30", "08:40"))
    assert scheduler.detect_conflicts([dog_schedule, cat_schedule]) == []


def test_filter_tasks_by_completion_status():
    done = Task("Feeding", duration_minutes=10, priority="high")
    done.mark_complete()
    pending = Task("Morning walk", duration_minutes=30, priority="high")

    scheduler = Scheduler()
    assert scheduler.filter_tasks([done, pending], completed=True) == [done]
    assert scheduler.filter_tasks([done, pending], completed=False) == [pending]


def test_filter_tasks_by_pet_name():
    biscuit_task = Task("Walk", duration_minutes=30, priority="high", pet_name="Biscuit")
    mochi_task = Task("Playtime", duration_minutes=20, priority="medium", pet_name="Mochi")

    scheduler = Scheduler()
    assert scheduler.filter_tasks([biscuit_task, mochi_task], pet_name="Biscuit") == [biscuit_task]
    assert scheduler.filter_tasks([biscuit_task, mochi_task], pet_name="Mochi") == [mochi_task]


def test_sort_by_time_orders_tasks_by_time_window():
    walk = Task("Morning walk", duration_minutes=30, priority="high")
    walk.required_time_window = "08:00"
    meds = Task("Medication", duration_minutes=5, priority="high")
    meds.required_time_window = "07:00"
    groom = Task("Grooming", duration_minutes=20, priority="medium")
    groom.required_time_window = "14:00"

    scheduler = Scheduler()
    sorted_tasks = scheduler.sort_by_time([walk, meds, groom])

    assert [t.title for t in sorted_tasks] == ["Medication", "Morning walk", "Grooming"]
