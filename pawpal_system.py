from datetime import date, timedelta


class Owner:
    def __init__(self, name: str, email: str = "", available_time_minutes: int = 120):
        self.name = name
        self.email = email
        self.available_time_minutes = available_time_minutes
        self.preferences: list = []
        self.pets: list["Pet"] = []
        self.tasks: list["Task"] = []

    def get_available_time(self) -> int:
        """Return the total minutes the owner has available for pet care today."""
        return self.available_time_minutes

    def get_preferences(self) -> list:
        """Return the owner's scheduling preferences (e.g. preferred task order)."""
        return self.preferences


class Pet:
    def __init__(self, name: str, species: str, breed: str = "", age: int = 0):
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.special_needs: list = []
        self.routines: dict = {}
        self.tasks: list["Task"] = []

    def add_task(self, task: "Task") -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def get_needs(self) -> list:
        """Return the pet's list of special needs or conditions."""
        return self.special_needs

    def validate_task(self, task: "Task") -> bool:
        """Return True if the task is appropriate for this pet."""
        return True


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str = "medium", category: str = "general", pet_name: str = "", recurrence: str = ""):
        self.title = title
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.pet_name = pet_name
        self.required_time_window: str = ""
        self.recurrence: str = recurrence  # "daily", "weekly", or ""
        self.due_date: date = date.today()
        self.completed: bool = False

    def is_required(self) -> bool:
        """Return True if this task must be included in the schedule (high priority)."""
        return self.priority == "high"

    def get_priority_score(self) -> int:
        """Return a numeric score (1–3) used to sort tasks by importance."""
        return {"high": 3, "medium": 2, "low": 1}.get(self.priority, 1)

    def mark_complete(self) -> "Task | None":
        """Mark this task done; return a fresh copy with the next due date if recurring, else None."""
        self.completed = True
        if self.recurrence == "daily":
            days_ahead = 1
        elif self.recurrence == "weekly":
            days_ahead = 7
        else:
            return None
        next_task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            pet_name=self.pet_name,
            recurrence=self.recurrence,
        )
        next_task.required_time_window = self.required_time_window
        next_task.due_date = self.due_date + timedelta(days=days_ahead)
        return next_task


class ScheduledTask:
    def __init__(self, task: Task, start_time: str, end_time: str, reason: str = ""):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason

    def get_duration(self) -> int:
        """Return the duration of the underlying task in minutes."""
        return self.task.duration_minutes


class DailySchedule:
    def __init__(self, date: str, total_time_available: int, start_time: str = "08:00"):
        self.date = date
        self.start_time = start_time
        self.scheduled_tasks: list[ScheduledTask] = []
        self.total_time_available = total_time_available
        self.explanations: list = []

    def add_task(self, scheduled_task: ScheduledTask) -> None:
        """Append a ScheduledTask to the day's plan."""
        self.scheduled_tasks.append(scheduled_task)

    def has_room_for(self, task: Task, start_time: str) -> bool:
        """Return True if the task fits within the remaining available time."""
        used = sum(st.get_duration() for st in self.scheduled_tasks)
        return used + task.duration_minutes <= self.total_time_available

    def check_for_conflicts(self) -> list[str]:
        """Return a list of warning strings for every overlapping task pair; empty list means no conflicts."""
        warnings = []
        for i, a in enumerate(self.scheduled_tasks):
            for b in self.scheduled_tasks[i + 1:]:
                if a.start_time < b.end_time and b.start_time < a.end_time:
                    warnings.append(
                        f"WARNING: '{a.task.title}' ({a.start_time}–{a.end_time}) "
                        f"overlaps with '{b.task.title}' ({b.start_time}–{b.end_time})"
                    )
        return warnings

    def get_explanation(self) -> str:
        """Return a formatted string summarising the day's schedule and time used."""
        lines = [f"Today's Schedule — {self.date}", "=" * 40]
        for st in self.scheduled_tasks:
            lines.append(
                f"  {st.start_time}–{st.end_time}  {st.task.title} "
                f"({st.task.duration_minutes} min) [{st.task.priority}]"
            )
            if st.reason:
                lines.append(f"             {st.reason}")
        time_used = sum(st.get_duration() for st in self.scheduled_tasks)
        lines += ["=" * 40, f"  Total time: {time_used} / {self.total_time_available} min used"]
        return "\n".join(lines)


class Scheduler:
    def __init__(self):
        self.last_schedule: DailySchedule = None

    def build_schedule(self, owner: Owner, pet: Pet, tasks: list[Task], time_available: int) -> DailySchedule:
        """Orchestrate prioritisation, fitting, and time assignment to produce a DailySchedule."""
        prioritized = self.prioritize_tasks(tasks)
        chosen = self.fit_tasks(prioritized, time_available)
        schedule = self.assign_times(chosen, time_available=time_available)
        schedule.date = f"{pet.name} ({pet.species})"
        self.last_schedule = schedule
        return schedule

    def prioritize_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted from highest to lowest priority score."""
        return sorted(tasks, key=lambda t: t.get_priority_score(), reverse=True)

    def fit_tasks(self, prioritized_tasks: list[Task], time_available: int) -> list[Task]:
        """Greedily select tasks in priority order until the time budget is exhausted."""
        chosen, remaining = [], time_available
        for task in prioritized_tasks:
            if task.duration_minutes <= remaining:
                chosen.append(task)
                remaining -= task.duration_minutes
        return chosen

    def detect_conflicts(self, schedules: list[DailySchedule]) -> list[str]:
        """Return warnings for overlapping tasks within each schedule and across different pet schedules."""
        warnings = []
        # Within each schedule
        for schedule in schedules:
            warnings.extend(schedule.check_for_conflicts())
        # Across different pet schedules (owner can only do one thing at a time)
        all_tasks = [st for s in schedules for st in s.scheduled_tasks]
        for i, a in enumerate(all_tasks):
            for b in all_tasks[i + 1:]:
                if a.task.pet_name != b.task.pet_name and a.start_time < b.end_time and b.start_time < a.end_time:
                    warnings.append(
                        f"WARNING: '{a.task.title}' for {a.task.pet_name} ({a.start_time}–{a.end_time}) "
                        f"conflicts with '{b.task.title}' for {b.task.pet_name} ({b.start_time}–{b.end_time})"
                    )
        return warnings

    def complete_task(self, task: Task, task_list: list[Task]) -> None:
        """Mark a task complete and append the next occurrence to task_list if it recurs."""
        next_occurrence = task.mark_complete()
        if next_occurrence:
            task_list.append(next_occurrence)

    def filter_tasks(self, tasks: list[Task], completed: bool = None, pet_name: str = None) -> list[Task]:
        """Return tasks matching the given completion status and/or pet name; None means no filter applied."""
        result = tasks
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        return result

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by required_time_window ascending; tasks with no window sort last."""
        return sorted(tasks, key=lambda t: t.required_time_window if t.required_time_window else "99:99")

    def assign_times(self, tasks: list[Task], start_time: str = "08:00", time_available: int = 0) -> DailySchedule:
        """Assign sequential start/end times to each task and return a DailySchedule."""
        h, m = map(int, start_time.split(":"))
        current = h * 60 + m
        schedule = DailySchedule(date="", total_time_available=time_available, start_time=start_time)
        for task in tasks:
            start_str = f"{current // 60:02d}:{current % 60:02d}"
            current += task.duration_minutes
            end_str = f"{current // 60:02d}:{current % 60:02d}"
            reason = f"Included: priority={task.priority}, duration={task.duration_minutes} min"
            schedule.add_task(ScheduledTask(task, start_str, end_str, reason))
        self.last_schedule = schedule
        return schedule
