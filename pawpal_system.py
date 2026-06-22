class Owner:
    def __init__(self, name: str, email: str = "", available_time_minutes: int = 120):
        self.name = name
        self.email = email
        self.available_time_minutes = available_time_minutes
        self.preferences: list = []
        self.pets: list["Pet"] = []
        self.tasks: list["Task"] = []

    def get_available_time(self) -> int:
        return self.available_time_minutes

    def get_preferences(self) -> list:
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
        self.tasks.append(task)

    def get_needs(self) -> list:
        return self.special_needs

    def validate_task(self, task: "Task") -> bool:
        return True


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str = "medium", category: str = "general"):
        self.title = title
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.required_time_window: str = ""
        self.is_recurring: bool = False
        self.completed: bool = False

    def is_required(self) -> bool:
        return self.priority == "high"

    def get_priority_score(self) -> int:
        return {"high": 3, "medium": 2, "low": 1}.get(self.priority, 1)

    def mark_complete(self) -> None:
        self.completed = True


class ScheduledTask:
    def __init__(self, task: Task, start_time: str, end_time: str, reason: str = ""):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason

    def get_duration(self) -> int:
        return self.task.duration_minutes


class DailySchedule:
    def __init__(self, date: str, total_time_available: int, start_time: str = "08:00"):
        self.date = date
        self.start_time = start_time
        self.scheduled_tasks: list[ScheduledTask] = []
        self.total_time_available = total_time_available
        self.explanations: list = []

    def add_task(self, scheduled_task: ScheduledTask) -> None:
        self.scheduled_tasks.append(scheduled_task)

    def has_room_for(self, task: Task, start_time: str) -> bool:
        used = sum(st.get_duration() for st in self.scheduled_tasks)
        return used + task.duration_minutes <= self.total_time_available

    def check_for_conflicts(self) -> bool:
        for i, a in enumerate(self.scheduled_tasks):
            for b in self.scheduled_tasks[i + 1:]:
                if a.start_time < b.end_time and b.start_time < a.end_time:
                    return True
        return False

    def get_explanation(self) -> str:
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
        prioritized = self.prioritize_tasks(tasks)
        chosen = self.fit_tasks(prioritized, time_available)
        schedule = self.assign_times(chosen, time_available=time_available)
        schedule.date = f"{pet.name} ({pet.species})"
        self.last_schedule = schedule
        return schedule

    def prioritize_tasks(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: t.get_priority_score(), reverse=True)

    def fit_tasks(self, prioritized_tasks: list[Task], time_available: int) -> list[Task]:
        chosen, remaining = [], time_available
        for task in prioritized_tasks:
            if task.duration_minutes <= remaining:
                chosen.append(task)
                remaining -= task.duration_minutes
        return chosen

    def assign_times(self, tasks: list[Task], start_time: str = "08:00", time_available: int = 0) -> DailySchedule:
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
