import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import kivy.graphics
from frontend.utils import *

word_color = hex_to_rgb('#CCCCCC')
textbox_color = hex_to_rgb('#CACACA')
input_word_color = hex_to_rgb('#282828')

title_font = 'src/fonts/FZFWZhuZGDSMCJW.TTF'
word_font = 'src/fonts/FZFWZhuZGDSMCJW.TTF'

zh_texts = {
    'title1': '请输入从',
    'title2': '@sjtu.edu.cn',
    'title3': '收到的的验证码',
    'submit': '开始！',
    'error': '出错啦！',
    'authcode error': '验证码错误！',
}

en_texts = {
    'title1': 'Please enter the verification code you received from',
    'title2': '@sjtu.edu.cn',
    'title3': '',
    'submit': 'Go!',
    'error': 'Error',
    'authcode error': 'Invalid authcode!',
}

class AuthcodeScreen(Screen):
    def __init__(self, my_name, manager, language, **kwargs):
        super(AuthcodeScreen, self).__init__(**kwargs)
        self.client_manager = manager
        self.my_name = my_name
        self.language_version = language
        self.old_language = []
        self.language_is_changed = True

    def on_enter(self):
        if self.language_version[0] == 'zh':
            self.texts = zh_texts
        else:
            self.texts = en_texts
        if self.old_language != self.language_version:
            self.old_language = self.language_version.copy()
            self.language_is_changed = True
        else:
            self.language_is_changed = False

        self.layout = BoxLayout(orientation='vertical', spacing=-500, padding=[50, 50, 50, 50])
        self.add_widget(self.layout)
        self.exit_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.layout.add_widget(self.exit_box)
        self.exit_box.add_widget(Label(text=' ', size_hint=(0.9, 1)))
        self.exit_box.add_widget(Button(text='X', size_hint=(0.1, 1), on_press=self.go_to_login, color=word_color, font_name=word_font, font_size=100, background_normal='', background_color=[0,0,0,0]))
        self.title_box = BoxLayout(orientation='vertical', size_hint=(1, 0.6), spacing=-900)
        self.layout.add_widget(self.title_box)
        self.title_box.add_widget(Label(text=self.texts['title1'], size_hint=(1, 0.2), color=word_color, font_name=word_font, font_size=50))
        self.title_box.add_widget(Label(text=self.my_name[0]+self.texts['title2'], size_hint=(1, 0.2), color=word_color, font_name=word_font, font_size=50))
        self.title_box.add_widget(Label(text=self.texts['title3'], size_hint=(1, 0.2), color=word_color, font_name=word_font, font_size=50))

        self.input_box = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=30, padding=[0, 100, 0, 220])
        self.layout.add_widget(self.input_box)
        self.authcode_input = LimitedTextInput(multiline=False, size_hint=(0.3, 0.7), pos_hint={'center_x': 0.5}, cursor_color=word_color, font_name=word_font, font_size=100)
        self.authcode_input.background_color = textbox_color
        self.authcode_input.foreground_color = input_word_color
        self.authcode_input.halign = 'center'
        self.authcode_input.valign = 'center'
        self.input_box.add_widget(self.authcode_input)
        self.input_box.add_widget(Button(text=self.texts['submit'], size_hint=(0.2, 0.3), pos_hint={'center_x': 0.5}, on_press=self.do_submit_authcode, color=word_color, font_name=word_font, font_size=30))
    

    def go_to_login(self, instance):
        self.layout.clear_widgets()
        App.get_running_app().root.current = 'login'

    def do_submit_authcode(self, instance): 
        is_success = self.client_manager.auth_code_api(self.my_name[0], self.authcode_input.text)
        # is_success = False
        if is_success:
            self.layout.clear_widgets()
            App.get_running_app().root.current = 'main'
        else:

            popup = Popup(title=self.texts['error'], content=Label(text=self.texts['authcode error'], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
            popup.open()
            self.authcode_input.text = ''
