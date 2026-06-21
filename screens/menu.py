from kivy.uix.screenmanager import Screen
from kivy.metrics import dp


class MainMenu(Screen):
    def on_kv_post(self, base_widget):
        """
        Wird einmalig aufgerufen, nachdem das KV-File vollständig geladen wurde.
        Optimiert die Höhen der Navigations- und Top-Bars plattformübergreifend.
        """
        super().on_kv_post(base_widget)
        
        # Sicheres Überschreiben der Bottom-Navigation-Höhe
        if 'bot_nav' in self.ids:
            nav_bar = self.ids.bot_nav
            nav_bar.height = dp(50)
            # Falls Kind-Container angepasst werden müssen, prüfen wir auf das Attribut 'height'
            for child in nav_bar.children:
                if hasattr(child, 'height'):
                    child.height = dp(50)

        # Sicheres Überschreiben der Top-Bar-Höhe
        if 'top_bar' in self.ids:
            top_bar = self.ids.top_bar
            top_bar.size_hint_y = None
            top_bar.height = dp(50)
            for child in top_bar.children:
                if hasattr(child, 'height'):
                    child.height = dp(50)