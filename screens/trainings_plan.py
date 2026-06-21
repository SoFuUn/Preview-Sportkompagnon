from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivymd.uix.list import OneLineListItem
from kivy.app import App
from kivymd.app import MDApp
from utils.storage import load_plan_data

class TrainingPlanScreen(Screen):
    plans = ListProperty([])
    dialog = None

    def on_kv_post(self, basewidget):
        self.update_list()

    def update_list(self):
        self.ids.plan_list.clear_widgets()
        self.data = load_plan_data()
        for plan in self.data:
            item = OneLineListItem(
                text=plan["plan_name"],
                on_release=lambda x, id=plan["plan_id"]: self.open_plan(id)
            )
            self.ids.plan_list.add_widget(item)

    # DISABLED FOR PREVIEW: Fallback block
    def add_plan(self, *args):
        pass

    # ACTIVE FOR PREVIEW: Allows the user to look inside existing plans
    def open_plan(self, id):
        print(f"Opening plan: {id}")
        app = App.get_running_app()
        plan_screen = app.root.get_screen("edit_plan")
        plan_screen.current_plan = id

        app.root.transition.direction = "left"
        app.root.current = "edit_plan"

    # DISABLED FOR PREVIEW: Intercept Plan Creation Dialog
    def show_add_dialog(self):
        MDApp.get_running_app().show_preview_warning()