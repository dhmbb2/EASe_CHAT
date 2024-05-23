from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, StencilPush, StencilUse, StencilUnUse
from kivy.uix.button import Button


def hex_to_rgb(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    return rgb_color + (alpha,)

def get_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
    return formatted_time
class ColoredRoundedLabel(BoxLayout):
    def __init__(self, text, back_color, word_color, halign, font_size, font_name, **kwargs):
        super(ColoredRoundedLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(*back_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[30])
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(Label(text=text, color=word_color, halign=halign, font_size=font_size, font_name=font_name))

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class MyApp(App):
    def build(self):
        layout = BoxLayout()
        colored_label = ColoredRoundedLabel(text='Hello, world!', size_hint=(1, 0.5), back_color=hex_to_rgb('#FF0000'), word_color=hex_to_rgb("#000000"))  # 创建一个带有红色背景的标签
        layout.add_widget(colored_label)
        return layout

if __name__ == '__main__':
    MyApp().run()