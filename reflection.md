# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- 3 Actions:
    - We need to allow users to enter information about their pet and upload it
    - Take that information and let them add tasks they want need to accomplish
    - Create a schedule based on these tasks

- Briefly describe your initial UML design.
    - The intial UML design created a simple layout with classes for Owner, Pet, Task, Schedule, and the relationships. For example owner owns pet, pet has tasks, daily schedule relies on scheduler.

- What classes did you include, and what responsibilities did you assign to each?
    - Owner — holds the pet owner's name, availability, and preferences; provides the scheduler with time constraints and ordering preferences.

    - Pet — stores the pet's profile (species, breed, age, special needs), validates whether a given task is appropriate for this pet.

    - Task — represents a single care activity with a title, duration, priority, and category; knows how to score itself for prioritization and check if it fits a time slot.

    - ScheduledTask — wraps a Task with a concrete start/end time and a reason explaining why it was chosen; used to build the final plan.

    - DailySchedule — the output of the planning process; holds the ordered list of ScheduledTasks, checks for time conflicts, and produces a human-readable explanation of the plan.

    - Scheduler — the core logic layer; takes an Owner, Pet, and list of Tasks, prioritizes them by importance, fits as many as possible into the available time, and returns a DailySchedule.  

**b. Design changes**

- Did your design change during implementation?
    - Yes the design did change.
- If yes, describe at least one change and why you made it.
    - One thing that changed are adding ownerships for task list that is made, that way a list of tasks can be associated with a specific owner.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - It considers time, so the time the owner has availible, then it considers the priority level of the task, and lastly the required time window, to make sure everything fits.
- How did you decide which constraints mattered most?
    - Time availability was the primary constraint because no matter how important a task is, it cannot be completed if the owner has no time. Priority was made secondary because when multiple tasks compete for limited time, importance should determine which ones make the cut — a high-priority medication should never be dropped in favor of a low-priority fetch session.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - The scheduler uses a greedy algorithm, it picks tasks in priority order and locks in each one the moment it fits, without looking ahead. This means it can miss combinations that would actually fit more total tasks into the available time. For example, if a 30-minute high-priority task is chosen first and only 25 minutes remain, two 20-minute medium-priority tasks will both be dropped even though one of them could have fit if the high-priority task had been skipped.

- Why is that tradeoff reasonable for this scenario?
    - For a daily pet care app, the greedy approach is a good fit because the task lists are small so the suboptimal scheduling cases are rare. More importantly, the behavior is predictable and transparent to the owner they can always trust that the most important tasks were considered first.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI for a lot of the brainstorming and desgin. I think it is very effective at getting the general case right but for opitmizing or making sure the code is actually what you want, its easier to manually make those specific changes. 

- What kinds of prompts or questions were most helpful?
    - The most helpful prompts were the specific ones. The longer and more specific the prompt the more accurate the solution was. Also asking it to explain certain topics or sections worked really well. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - One moment was when it was clearly asking me to change one of my classes to refer to a class that just did not exist. Im assmuning it got confused and probably would have fixed it later on in the chat.

- How did you evaluate or verify what the AI suggested?
    - I made sure to look over any implementations to some extent and also test things myself to make sure it works as intended.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - We tests: 
        - Task completion status — that calling mark_complete() flips task.completed from False to True

        - Pet task count — that calling pet.add_task() increases the length of pet.tasks
        - Daily recurrence — that marking a daily task complete returns a new Task with due_date = today + 1 day and completed = False
        - Weekly recurrence — same as above but due_date = today + 7 days
        - Non-recurring tasks — that mark_complete() returns None instead of a new task when recurrence is empty
         - Recurrence via Scheduler — that scheduler.complete_task() appends the next occurrence to the task list, growing it from 1 to 2
        - No cross-pet conflict — that non-overlapping multi-pet schedules return an empty list
        - Filter by completion status — that filter_tasks(completed=True/False) correctly separates done vs. pending tasks

        - Sort by time window — that tasks with HH:MM time windows come back in chronological order
- Why were these tests important?
    - These test are important cause it helps cover some of the potential actions the live site will run into. We want to make sure that these actions work as intended so we can cover a large userbase. 

```
=================================== test session starts ===================================
platform darwin -- Python 3.13.12, pytest-9.1.0, pluggy-1.6.0
rootdir: /Users/rshankar/Desktop/AI110-TF/ai110-module2show-pawpal-starter
collected 13 items

tests/test_pawpal.py .............                                                  [100%]

=================================== 13 passed in 0.01s ===================================
```

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - 4, because covered most cases and realistic user cases and they all passed, but there is always some case that can break it.
- What edge cases would you test next if you had more time?
    - I would probably test the empty task list, or the identical pet name conflict.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I am most satisfied with how in depth the classes are and how they all came together after all the planning to accomplish different tasks.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - I would try to improve some of the logic to be more user friendly. We can build upon some of the collision and algorithm sections to be more optimal for users. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - I learned that AI is very helpful for planning and desiging but it needs a guide, or else it will go way off track and you will waste a lot of token trying to get it back on track. 


## Sample Output:

Owner: Jordan  |  Available time: 90 min

Today's Schedule — Biscuit (dog)
========================================
  08:00–08:30  Morning walk (30 min) [high]
             Included: priority=high, duration=30 min
  08:30–08:40  Feeding (10 min) [high]
             Included: priority=high, duration=10 min
  08:40–09:00  Grooming (20 min) [medium]
             Included: priority=medium, duration=20 min
========================================
  Total time: 60 / 60 min used

Today's Schedule — Mochi (cat)
========================================
  08:00–08:10  Feeding (10 min) [high]
             Included: priority=high, duration=10 min
  08:10–08:15  Medication (5 min) [high]
             Included: priority=high, duration=5 min
========================================
  Total time: 15 / 30 min used
rshankar@Ryans-MacBook-Air-2 ai110-module2show-pawpal-starter %
