import json
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import App
from utils.storage import get_days, get_plan_exercises, get_sets, save_history_entry


class WorkoutScreen(Screen):
    current_plan = None

    def on_enter(self):
        self.exercise_index = 0
        self.set_index = 0
        
        self.update_day_container()

    def update_day_container(self):
        self.ids.day_container.clear_widgets()
        self.days = get_days(self.current_plan)
        for day in self.days:
            item = DayContItem(
                id=day["day_id"],
                text=day["day"],
                callback_change_scene=self.change_scene
                )
            self.ids.day_container.add_widget(item)

    def setup_exercises(self):
        self.ids.exercise_container.clear_widgets()
        self.exercises = get_plan_exercises(self.current_day)
        self.exercise_data = []
        for exercise in self.exercises:
            sets_data = []

            sets = get_sets(exercise["plan_exercise_id"])
            for s in sets:
                sets_data.append({
                    "reps": s["reps"],
                    "weight": s["weight"]
                })

            self.exercise_data.append({
                "exercise_id": exercise["exercise_id"],
                "exercise_name": exercise["exercise_name"],
                "sets": sets_data
            })
        self.setup_current_set()

    def setup_current_set(self):
        self.ids.exercise_container.clear_widgets()
        exercise_data = self.exercise_data[self.exercise_index]

        exercise_id = exercise_data["exercise_id"]
        exercise_name = exercise_data["exercise_name"]
        sets = exercise_data["sets"]

        current_set = sets[self.set_index]

        item = ExerciseItem(
            id=exercise_id,
            text=exercise_name,
            reps=current_set["reps"],
            weight=current_set["weight"]
            )
        self.ids.exercise_container.add_widget(item)

    def get_next_set(self):
        self.set_index += 1
        exercise_data = self.exercise_data[self.exercise_index]
        sets = exercise_data["sets"]
        if self.set_index >= len(sets):
            self.exercise_index += 1
            self.set_index = 0

            if self.exercise_index >= len(self.exercise_data):
                self.ids.sm_content.current = 'day_cont'
                self.manager.current = "menu"
                return
        self.setup_current_set()

    def change_scene(self, day_id):
        self.ids.sm_content.transition.direction = 'left'
        self.ids.sm_content.current = 'exercise_cont'
        self.current_day = day_id
        self.history_id = save_history_entry(self.current_plan, day_id)
        self.setup_exercises()

    def switch_screen(self):
        main_menu = self.manager.get_screen("menu")
        main_menu.ids.bot_nav.switch_tab("start_workout")
        self.manager.transition.direction = "right"
        self.manager.current = "menu"

class DayContItem(MDBoxLayout):
    id = NumericProperty()
    text = StringProperty()
    callback_change_scene = ObjectProperty(None)

class ExerciseItem(MDBoxLayout):
    id = NumericProperty()
    text = StringProperty()

    def __init__(self, reps="0", weight="0", *args, **kwargs):
        super().__init__(*args, **kwargs)
        formatted_name = str(self.text).strip().upper().replace(" ", "_")
        self.ids.exercise_name.text = formatted_name
        self.ids.reps_field.text = str(reps)
        self.ids.weight_field.text = str(weight)


