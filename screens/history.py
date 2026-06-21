from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineIconListItem, OneLineAvatarListItem, IconLeftWidget
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

from utils.storage import load_history_data


class HistoryScreen(Screen):
    def on_enter(self):
        # Der Dateiname wird hier nicht mehr übergeben – die Storage-Logik nutzt ihren internen Default-Wert.
        self.data = load_history_data()

        # Bereite Daten für die RecycleView-Struktur vor
        self.ids.history_list.data = [
            {
                "name": workout_data["name"],
                "workout_data": workout_data,
                "callback": self.show_detail
            } 
            for _, workout_data in self.data.items()
        ]

    def show_detail(self, chosen_history):
        container = self.ids.history_overview_container
        container.clear_widgets()
        
        # Instanziierung der Detail-Komponente
        item = HistoryOverviewItem(
            name=chosen_history.name,
            workout_data=chosen_history.workout_data
        )
        container.add_widget(item)
        
        # Navigation in den Detail-Screen
        self.ids.sm_content.transition.direction = "left"
        self.ids.sm_content.current = "history_item_overview"

    def switch_screen(self):
        self.ids.sm_content.transition.direction = "right"
        self.ids.sm_content.current = "history_library_overview"


class HistoryEntry(MDCard):
    name = StringProperty()
    workout_data = ObjectProperty()
    callback = ObjectProperty()


class HistoryOverviewItem(MDBoxLayout):
    name = StringProperty()
    workout_data = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Verzögert den UI-Bau um einen Frame, um sichere ID-Bindung zu garantieren
        Clock.schedule_once(self.build_ui)

    def build_ui(self, dt):
        """Generiert dynamisch die Liste der Übungen und Sätze aus den Verlaufsdaten."""
        if not self.workout_data or not self.ids.get('info_container'):
            return

        container = self.ids.info_container
        container.clear_widgets()

        for exercise_name, sets in self.workout_data.items():
            if exercise_name == "name":
                continue

            # Header für die jeweilige Übung erstellen
            exercise_header = OneLineAvatarListItem(
                text=f"[b]{exercise_name}[/b]",
                divider=None
            )
            icon = IconLeftWidget(icon="dumbbell")
            exercise_header.add_widget(icon)
            container.add_widget(exercise_header)
            
            # Einzelne Sätze der Übung unter dem Header einfügen
            for set_index, set_data in enumerate(sets, 1):
                set_item = TwoLineIconListItem(
                    text=f"Satz {set_index}",
                    secondary_text=f"{set_data['reps']} Wdh.  @  {set_data['weight']} kg",
                    divider="Inset"
                )
                sub_icon = IconLeftWidget(icon="circle-small")
                set_item.add_widget(sub_icon)
                container.add_widget(set_item)


class HistoryLibraryScreen(MDBoxLayout):
    pass


class UniqueHistoryScreen(MDBoxLayout):
    pass