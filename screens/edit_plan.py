from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivymd.app import MDApp

from utils.storage import ( 
    get_days,
    get_exercises_with_sets,
    save_plan_set_entry, 
    delete_set, 
    update_set
)


class EditPlanScreen(Screen):
    # Class attributes for structural tracking
    current_plan = None
    current_day = None
    dialog = None

    def on_enter(self):
        self.update_day_list()
        self.update_exercise_list()

    def update_day_list(self):
        self.ids.day_list.clear_widgets()
        self.days = get_days(self.current_plan)
        for day in self.days:
            item = DayItem(
                id=day["day_id"],
                text=day["day"],
                callback_change_scene=self.change_scene,
                callback_remove_day=self.remove_day
            )
            self.ids.day_list.add_widget(item)

    # DISABLED FOR PREVIEW: Intercept Day Creation Dialog
    def show_add_dialog(self):
        MDApp.get_running_app().show_preview_warning()

    def add_day(self, *args):
        pass

    # DISABLED FOR PREVIEW: Intercept Exercise Selection Screen
    def open_exercise_selector(self):
        MDApp.get_running_app().show_preview_warning()

    def receive_exercise(self, id, exercise):
        pass

    def update_exercise_list(self):
        self.ids.exercise_list.clear_widgets()
        self.exercises = get_exercises_with_sets(self.current_day)
        for exercise in self.exercises:
            item = ExpandableExerciseItem(
                id=exercise["plan_exercise_id"],
                text=exercise["exercise_name"],
                callback_add_set=self.add_set_item
            )
            self.ids.exercise_list.add_widget(item)
            
            item.ids.container.clear_widgets()
            item.sets = exercise["sets"]
            for set_data in item.sets:
                setrow = SetInputRow(
                    id=set_data["set_id"],
                    plan_exercise_id=item.id,
                    reps=set_data["reps"],
                    weight=set_data["weight"]
                )
                item.ids.container.add_widget(setrow)

    def switch_screen(self):
        main_menu = self.manager.get_screen("menu")
        main_menu.ids.bot_nav.switch_tab("trainings_plan")
        self.manager.transition.direction = "right"
        self.manager.current = "menu"

    # DISABLED FOR PREVIEW: Intercept Day Deletion
    def remove_day(self, widget):
        MDApp.get_running_app().show_preview_warning()
    
    def change_scene(self, day_id=None):
        if self.ids.sm_content.current == "calender":
            self.current_day = day_id
            self.update_exercise_list()
            self.ids.sm_content.transition.direction = 'left'
            self.ids.sm_content.current = 'exercises'
        else:
            self.ids.sm_content.transition.direction = "right"
            self.ids.sm_content.current = "calender"  
    
    # ACTIVE FOR PREVIEW: Allows testing set addition
    def add_set_item(self, id, container):
        new_set = {"plan_exercise_id": id}
        set_id = save_plan_set_entry(new_set)
        item = SetInputRow(
            id=set_id,
            plan_exercise_id=id,
            reps="",
            weight=""
        )
        container.add_widget(item)


class DayItem(MDBoxLayout):
    id = NumericProperty()
    text = StringProperty()
    callback_change_scene = ObjectProperty(None)
    callback_remove_day = ObjectProperty(None)


class ExpandableExerciseItem(MDBoxLayout):
    id = NumericProperty()
    text = StringProperty()
    callback_add_set = ObjectProperty(None)
    container = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = self.ids.container
        self.toggle()

    def toggle(self):
        is_open = self.container.disabled
        self.container.disabled = not is_open
        self.container.opacity = 1 if is_open else 0
    
    # DISABLED FOR PREVIEW: Intercept Exercise Deletion
    def del_entry(self):
        MDApp.get_running_app().show_preview_warning()

    
class SetInputRow(MDBoxLayout):
    id = NumericProperty()
    plan_exercise_id = NumericProperty()

    def __init__(self, reps="", weight="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.reps_field.text = str(reps)
        self.ids.weight_field.text = str(weight)

    def on_touch_down(self, touch):
        if self.disabled and self.collide_point(*touch.pos):
            return False
        return super().on_touch_down(touch)
    
    # ACTIVE FOR PREVIEW: Allows testing database saves for text changes
    def save_to_db(self):
        # Fallback values to prevent SQLite type mismatch crashes on empty inputs
        reps = self.ids.reps_field.text.strip() or "0"
        weight = self.ids.weight_field.text.strip() or "0.0"
        
        set_payload = {
            "set_id": self.id,
            "reps": int(reps) if reps.isdigit() else 0,
            "weight": float(weight) if weight.replace('.', '', 1).isdigit() else 0.0
        }
        update_set(set_payload)

    # ACTIVE FOR PREVIEW: Allows testing set removal
    def del_row(self):
        set_id = self.id
        self.parent.remove_widget(self)
        delete_set(set_id)