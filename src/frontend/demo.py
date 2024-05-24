from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.app import App
from kivy.properties import StringProperty

class MyTextInput(TextInput):
    text_for_label = StringProperty('')

    def insert_text(self, substring, from_undo=False):
        self.text_for_label += substring
        return super(MyTextInput, self).insert_text(substring, from_undo=from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        # 获取删除前的文本长度
        old_length = len(self.text_for_label)
        # 调用父类的 do_backspace 方法
        super(MyTextInput, self).do_backspace(from_undo=from_undo, mode=mode)
        # 计算删除的字符数
        num_deleted = old_length - len(self.text)
        # 更新 self.text_for_label
        self.text_for_label = self.text_for_label[:-num_deleted]

class WrapTextInput(RelativeLayout):
    def __init__(self, background_color, word_color, font_size, font_name, **kwargs):
        super(WrapTextInput, self).__init__(**kwargs)
        self.text_input = TextInput(multiline=True, size_hint=(1, 1), background_color=background_color, cursor_color=word_color, font_size=font_size, font_name=font_name)
        self.label = Label(size_hint=(1, 1), text=self.text_input.text, color=word_color, valign='bottom', halign='left', font_size=font_size, font_name=font_name)
        self.label.bind(size=self.label.setter('text_size'))
        self.text_input.bind(text=self.label.setter('text'))
        self.text = self.text_input.text
        self.add_widget(self.label)
        self.add_widget(self.text_input)



class MyApp(App):
    def build(self):
        return WrapTextInput(background_color=(1, 1, 1, 1), word_color=(0, 0, 0, 1), font_size=30, font_name='src/fonts/FZFWZhuZGDSMCJW.TTF')

if __name__ == '__main__':
    MyApp().run()