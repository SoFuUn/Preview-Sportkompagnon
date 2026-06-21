from kivy.core.window import Window

class ThemeManager:
    current_theme = "Default"

    themes = {
        "default": {
            "palette": "Indigo",
            "hue": "500",
            "style": "Dark",
            "primary": (63/255, 81/255, 181/255, 1),
            "background": (0.08, 0.08, 0.08, 1),
            "text": (1, 1, 1, 1),
            "accent": (0.3, 0.5, 1, 0.5),
        }
    }

    @classmethod
    def apply(cls, app, name):
        theme = cls.themes[name]
        app.theme_cls.primary_palette = theme["palette"]
        app.theme_cls.primary_hue = theme["hue"]
        app.theme_cls.theme_style = theme["style"]
        app.primary_color = theme["primary"]
        app.background_color = theme["background"]
        app.text_color = theme["text"]
        app.accent_color = theme["accent"]
        Window.clearcolor = theme["background"]
        
        