from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivymd.uix.list import OneLineListItem
from kivymd.app import MDApp

from utils.storage import load_plan_data, get_days, get_plan_exercises, get_sets


class StartWorkoutScreen(Screen):
    plans = ListProperty([])

    def on_enter(self):
        """Triggers list refresh every time the screen is displayed."""
        self.update_list()

    def update_list(self):
        """Populates the UI with actionable, non-empty workout plans."""
        self.ids.plan_list.clear_widgets()
        self.plans = load_plan_data()
        
        for plan in self.plans:
            if self.is_workout_empty(plan):
                continue

            item = OneLineListItem(
                text=plan["plan_name"],
                on_release=lambda x, plan_id=plan["plan_id"]: self.open_plan(plan_id)
            )
            self.ids.plan_list.add_widget(item)

    def is_workout_empty(self, plan):
        """
        Verifies if a workout plan contains executable sets.
        Flattens the nested loop architecture using pythonic generator expressions.
        """
        days = get_days(plan["plan_id"])
        if not days:
            return True

        return not any(
            get_sets(exercise["plan_exercise_id"])
            for day in days
            for exercise in get_plan_exercises(day["day_id"])
        )

    def open_plan(self, plan_id):
        """Injects the chosen plan context into the target execution screen."""
        print(f"Opening plan: {plan_id}")
        
        app = MDApp.get_running_app()
        plan_screen = app.root.get_screen("workout_screen")
        
        # State Mutation & Navigation
        plan_screen.current_plan = plan_id
        app.root.transition.direction = "left"
        app.root.current = "workout_screen"