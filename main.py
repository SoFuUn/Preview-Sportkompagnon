from kivy.config import Config

# Graphics configuration must happen before compiling other Kivy modules
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', True)

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar

# Local screen imports
from screens.menu import MainMenu
from screens.one_rm import OneRepMaxScreen
from screens.history import HistoryScreen
from screens.trainings_plan import TrainingPlanScreen
from screens.edit_plan import EditPlanScreen
from screens.start_workout import StartWorkoutScreen
from screens.workout import WorkoutScreen
from utils.theme_manager import ThemeManager

# UI Layer Compilation
Builder.load_file('screens/menu.kv')
Builder.load_file('screens/trainings_plan.kv')
Builder.load_file('screens/one_rm.kv')
Builder.load_file('screens/start_workout.kv')
Builder.load_file('screens/history.kv')
Builder.load_file('screens/edit_plan.kv')
Builder.load_file('screens/workout.kv')

class PreviewSportkompagnon(MDApp):
    def build(self):
        ThemeManager.apply(self, "default")
        
        sm = ScreenManager()
        self.main_menu = MainMenu(name="menu")
        sm.add_widget(self.main_menu)
        sm.add_widget(EditPlanScreen(name='edit_plan'))
        sm.add_widget(WorkoutScreen(name='workout_screen'))

        menu_ids = self.main_menu.ids

        self.trainings_plan_screen = TrainingPlanScreen()
        menu_ids.tab_trainings_plan.add_widget(self.trainings_plan_screen)

        self.orm_screen = OneRepMaxScreen()
        menu_ids.tab_orm_screen.add_widget(self.orm_screen)

        self.start_workout_screen = StartWorkoutScreen()
        menu_ids.tab_start_workout.add_widget(self.start_workout_screen)

        self.history_screen = HistoryScreen()
        menu_ids.tab_history_screen.add_widget(self.history_screen)
        
        return sm
    
    # --- Preview Helper Added to App Class Context ---
    def show_preview_warning(self):
        MDSnackbar(
            MDLabel(
                text="Not available in preview.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            ),
            bg_color=(0.2, 0.2, 0.2, 1),
            duration=1.5
        ).open()

if __name__ == '__main__':
    PreviewSportkompagnon().run()