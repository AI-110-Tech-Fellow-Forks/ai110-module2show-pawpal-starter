import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Pet care planning assistant — powered by your Scheduler backend")

# ── Owner & Pet Setup ──────────────────────────────────────────────────────────
st.subheader("Owner & Pet")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_time = st.number_input("Available time (minutes)", min_value=10, max_value=480, value=90)
with col2:
    pet_name = st.text_input("Pet name", value="Biscuit")
    species = st.selectbox("Species", ["dog", "cat", "other"])

st.divider()

# ── Task Entry ─────────────────────────────────────────────────────────────────
st.subheader("Add Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    time_window = st.text_input("Time window (HH:MM)", value="", placeholder="e.g. 08:00")

if st.button("Add task"):
    st.session_state.tasks.append({
        "title": task_title,
        "duration_minutes": int(duration),
        "priority": priority,
        "required_time_window": time_window.strip(),
    })

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
    if st.button("Clear all tasks"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Schedule Generation ────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule", type="primary"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name, available_time_minutes=int(available_time))
        pet = Pet(name=pet_name, species=species)

        tasks = []
        for t in st.session_state.tasks:
            task = Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                pet_name=pet_name,
            )
            task.required_time_window = t.get("required_time_window", "")
            tasks.append(task)

        scheduler = Scheduler()

        # ── Sorted view ───────────────────────────────────────────────────────
        st.markdown("### Tasks sorted by time window")
        sorted_tasks = scheduler.sort_by_time(tasks)
        sorted_rows = [
            {
                "Title": t.title,
                "Time window": t.required_time_window if t.required_time_window else "—",
                "Priority": t.priority,
                "Duration (min)": t.duration_minutes,
            }
            for t in sorted_tasks
        ]
        st.table(sorted_rows)

        # ── Build the schedule ────────────────────────────────────────────────
        schedule = scheduler.build_schedule(owner, pet, tasks, time_available=int(available_time))

        st.markdown("### Today's Schedule")
        if not schedule.scheduled_tasks:
            st.warning("No tasks fit within the available time budget.")
        else:
            schedule_rows = [
                {
                    "Start": item.start_time,
                    "End": item.end_time,
                    "Task": item.task.title,
                    "Duration (min)": item.task.duration_minutes,
                    "Priority": item.task.priority,
                }
                for item in schedule.scheduled_tasks
            ]
            st.table(schedule_rows)

            time_used = sum(item.get_duration() for item in schedule.scheduled_tasks)
            st.success(f"Schedule built — {time_used} / {int(available_time)} minutes used")

        # ── Conflict detection ────────────────────────────────────────────────
        st.markdown("### Conflict Check")
        conflicts = scheduler.detect_conflicts([schedule])
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts detected.")

        # ── Tasks that didn't fit ─────────────────────────────────────────────
        scheduled_titles = {st.task.title for st in schedule.scheduled_tasks}
        dropped = [t for t in tasks if t.title not in scheduled_titles]
        if dropped:
            st.markdown("### Tasks that didn't fit")
            st.table([
                {"Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
                for t in dropped
            ])
