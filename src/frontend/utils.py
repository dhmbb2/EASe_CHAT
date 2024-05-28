from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, StencilPush, StencilUse, StencilUnUse
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.text import Label as CoreLabel
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
import re


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

class WrapTextInput(RelativeLayout):
    plain_text = StringProperty('')

    def __init__(self, screen, background_color, word_color, font_size, font_name, **kwargs):
        super(WrapTextInput, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_key_down)
        self.screen = screen
        self.text_input = TextInput(multiline=True, size_hint=(1, 1), background_color=background_color, cursor_color=word_color, font_size=font_size, font_name=font_name)
        # self.text_input.bind(on_text_validate=self._on_text_validate)
        self.label = Label(size_hint=(1, 1), text=self.text_input.text, color=word_color, valign='bottom', halign='left', font_size=font_size, font_name=font_name)
        self.label.bind(size=self.label.setter('text_size'))
        self.text_input.bind(text=self.label.setter('text'))
        self.text = self.text_input.text
        self.add_widget(self.label)
        self.add_widget(self.text_input)

    def on_text(self, instance, value):
        self.plain_text = value
        self.label.text = value
        self.text_input.text = value

    def _on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keyboard == 13 and 'ctrl' in modifiers:
            self.screen.do_send_message()
            return True

def login_filter(text):
    filtered_text = re.sub(r'[^a-zA-Z0-9_@.]', '', text)
    if filtered_text != text:
        return False
    else:
        return True

class MyApp(App):
    def build(self):
        layout = BoxLayout()
        colored_label = ColoredRoundedLabel(text='Hello, world!', size_hint=(1, 0.5), back_color=hex_to_rgb('#FF0000'), word_color=hex_to_rgb("#000000"))  # 创建一个带有红色背景的标签
        layout.add_widget(colored_label)
        return layout

if __name__ == '__main__':

    print(login_filter('huanyuqingming@sjtu.edu.cn'))

    # MyApp().run()