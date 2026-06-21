from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem


class OneRepMaxScreen(Screen):
    # Core mathematical scale for submaximal repetition estimation
    rm_percentages = [
        1.00, 0.95, 0.93, 0.90, 0.87,
        0.85, 0.83, 0.80, 0.77, 0.75,
        0.72, 0.70, 0.67, 0.65, 0.62,
        0.60, 0.58, 0.56, 0.54, 0.52,
        0.50, 0.48, 0.46, 0.44, 0.42
    ]
    
    # Safe fallback initialization
    orm = 0.0

    def orm_calculate(self):
        """Calculates estimated 1RM using the Epley formula with strict type validation."""
        try:
            weight = float(self.ids.weight_input.text.strip())
            reps = int(self.ids.reps_input.text.strip())
            
            # Formelberechnung (Epley-Gleichung)
            self.orm = round(weight * (1 + (reps / 30)), 2)
            
            # UI State Mutation
            self.ids.result_label.text = f"Dein 1RM: {self.orm} kg"
            self.ids.orm_save_btn.disabled = False
            self.ids.orm_input.text = str(self.orm)
            
            self.rep_max_calculate()
            
        except ValueError:
            # Catching alphabetic or empty inputs safely without crashing the main thread
            self.ids.result_label.text = "Ungültige Eingabe!"

    def rep_max_calculate(self):
        """Generates the breakdown matrix utilizing a pythonic enumeration model."""
        self.ids.rm_values.clear_widgets()
        
        # Enumerate with start=1 yields structural clean layout mapping (Repetition: Calculated Weight)
        for target_rep, percentage in enumerate(self.rm_percentages, start=1):
            calculated_rm = round(self.orm * percentage, 2)
            self.ids.rm_values.add_widget(
                OneLineListItem(text=f"{target_rep} Wdh:  {calculated_rm} kg")
            )


class OneRepMaxCalc(MDBoxLayout):
    pass


class RepMaxTable(MDBoxLayout):
    pass