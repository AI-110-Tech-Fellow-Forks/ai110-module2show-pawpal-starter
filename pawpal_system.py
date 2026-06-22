class Owner:
    def __init__(self, name: str, email: str = "", available_time_minutes: int = 120):
        self.name = name
        self.email = email
        self.available_time_minutes = available_time_minutes
        self.preferences: list = []

    def get_available_time(self) -> int:
        pass

    def get_preferences(self) -> list:
        pass


class Pet:
    def __init__(self, name: str, species: str, breed: str = "", age: int = 0):
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.special_needs: list = []
        self.routines: dict = {}

    def get_needs(self) -> list:
        pass

    def validate_task(self, task: "Task") -> bool:
        pass


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str = "medium", category: str = "general"):
        self.title = title
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.required_time_window: str = ""
        self.is_recurring: bool = False

    def is_required(self) -> bool:
        pass

    def get_priority_score(self) -> int:
        pass

    def fits_in_slot(self, start_time: str, duration: int) -> bool:
        pass


class ScheduledTask:
    def __init__(self, task: Task, start_time: str, end_time: str, reason: str = ""):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason

    def get_duration(self) -> int:
        pass


class DailySchedule:
    def __init__(self, date: str, total_time_available: int):
        self.date = date
        self.scheduled_tasks: list[ScheduledTask] = []
        self.total_time_available = total_time_available
        self.explanations: list = []

    def add_task(self, task: Task, start_time: str) -> None:
        pass

    def check_for_conflicts(self) -> bool:
        pass

    def get_explanation(self) -> str:
        pass


class Scheduler:
    def build_schedule(self, owner: Owner, pet: Pet, tasks: list[Task], time_available: int) -> DailySchedule:
        pass

    def prioritize_tasks(self, tasks: list[Task]) -> list[Task]:
        pass

    def fit_tasks(self, prioritized_tasks: list[Task], time_available: int) -> list[Task]:
        pass

    def assign_times(self, tasks: list[Task]) -> DailySchedule:
        pass

    def explain_choices(self) -> str:
        pass
