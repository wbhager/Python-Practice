# Python Practice 2: Strengthening core Python

# Background: My data skills are a bit ahead, so I want to catch up a bit with the other parts of python. For example, I am still a beginner with making things like classes
#             and methods, so I want that to be my focus for this file.

# Goal: I can fully understand the basics of classes and methods, and I can determine what method I need to use given a situation that calls for one.

# Project: Build a simple console-based task-manager app that lets a user:
#     - Create tasks
#     - Complete tasks
#     - View all tasks
#     - Filter by status (complete/incomplete)

# Day 1: Planned out the project, learned the basics about classes, custom methods, and dunder methods, constructed the dunder and basic custom methods
# Day 2: Learned the differences between constructor, dunder, instance, static, and class methods. Learned how to determine what kind of method I would need for different
#        use cases. Finished constructing the main loop that prompts the user for actions and utilizes the appropriate methods in the class to get the user the correct info

# Day 3 (Very short): Finished the view function, tested most of the edgecases, and debugged areas such as the completion instance method and the input string lines

# COMPLETED on Day 3

from datetime import datetime

class Task:

    # Defining methods in the class Task

    # Constructor method that defines all the attributes that a task must have
    def __init__(self, title: str, datetime_issued: datetime, importance: int, urgency: int, priority: int, completion_flag: bool = False, datetime_completed: datetime = None) -> None:
        self.title = title
        self.datetime_issued = datetime_issued
        self.importance = importance
        self.urgency = urgency
        self.priority = priority
        self.completion_flag = completion_flag
        self.datetime_completed = datetime_completed
    
    # String dunder method so that anyone can see the details of task
    def __str__(self) -> str:
        return f"Task name: {self.title}, Task Issue Date: {self.datetime_issued}, Importance Level (1-5): {self.importance}, Urgency Level (1-5): {self.urgency}, Priority Level (2-10): {self.priority}, Completion Checker: {self.completion_flag}, Date Completed if Completed: {self.datetime_completed}"
    
    # Representation dunder method so that I can see any task object if I want to while debugging
    def __repr__(self) -> str:
        return f"Task(title = '{self.title}', datetime_issued = {self.datetime_issued}, importance = {self.importance}, urgency = {self.urgency}, priority = {self.priority}, completion_flag = {self.completion_flag}, datetime_completed = {self.datetime_completed})"

    # Completion instance method
    def mark_complete(self) -> None:
        self.completion_flag = True
        self.datetime_completed = datetime.now()

# Task title/priority modification
def task_modification(task_list, old_title, new_title, new_importance_level, new_urgency_level):
    for task in task_list:
        if task.title.lower() == old_title.lower():
            task.title = new_title
            task.importance_level = new_importance_level
            task.urgency_level = new_urgency_level
    



# Main loop where the user interacts with the app
def main():

    task_list = []

    while True:
        action = input("Welcome to Will's task manager app, where you can add tasks, modify existing tasks, view one or all tasks, complete tasks, or exit the program. What would you like to do? ")
            # Include where if the words add, modify, complete, exit, or quit in any way are specified, then the program will do the specified action
        if "add" in action:
            task_title = input("What is the name of the task you would like to add? ")
            datetime_issued = datetime.now()
            importance_level = input("On a scale of 1-5, with 5 being the most important, how important is this task? ")
            urgency_level = input("On a scale of 1-5, with a 5 being the most urgent, how urgently does this task need to be done? ")
            priority_level = int(importance_level) + int(urgency_level)
            task = Task(task_title, datetime_issued, importance_level, urgency_level, priority_level)
            task_list.append(task)

        elif "modify" in action:
            print("Ok! We can modify the title, the importance level, and/or the urgency level of the task. ")
            old_title = input("What is the name of the task that you wish to modify? ")
            new_title = input("What is the name of the title that you want your task to be? If you want it to stay the same, please type in the old task title. ")
            new_importance_level = input("What is the new importance level that you want your task to be? If you want it to stay the same, please type in the old importance level. ")
            new_urgency_level = input("What is the new urgency level that you want your task to be? If you want it to stay the same, please type in the old urgency level. ")
            task_modification(task_list, old_title, new_title, new_importance_level, new_urgency_level)
            print("Task modified!")
        
        elif "complete" in action:
            completed_task = input("Which task would you like to set to complete? ")
            found = False
            for task in task_list:
                if task.title.lower() == completed_task.lower():
                    task.mark_complete()
                    found = True
                    print("Task completed! Great job!")
                    break
            if not found:
                print("Task not found. You will need to try again later.")

        elif "view" in action:
            how_many_tasks = input("Would you like to view one specified task, or the whole list? Please input the title of the task if you want the one task, or input task list if you want the task list: ")
            if how_many_tasks == "task list":
                for task in task_list:
                    print()
                    print(task)
            for task in task_list:
                if how_many_tasks.lower() == task.title.lower():
                    print()
                    print(task)
            print()

        elif action in ("quit", "exit"):
            print("You have selected to quit the program. Everything will now reset.")
            quit()

        else:
            print("You did not specify to add, modify, complete, or exit the program. This program will now shut down and everything will reset.")
            quit()



if __name__ == "__main__":
    main()