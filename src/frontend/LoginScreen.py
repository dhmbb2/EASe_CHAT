import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import kivy.graphics
from frontend.utils import *

word_color = hex_to_rgb('#CCCCCC')
textbox_color = hex_to_rgb('#CACACA')
input_word_color = hex_to_rgb('#282828')

title_font = 'src/fonts/AcademyEngravedStd.otf'
word_font = 'src/fonts/Consolas.ttf'

class LoginScreen(Screen):
    def __init__(self, manager, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.client_manager = manager

    def on_enter(self):
        layout = BoxLayout(orientation='vertical', spacing=20, padding=[0, 100, 0, 150])
        # 标题
        self.title_box= BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=-100)
        self.title_box.add_widget(Label(text='Welcome to EASEchat', font_size=70, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font))
        layout.add_widget(self.title_box)
        self.title_box.add_widget(Label(text='Efficient And SEcure chat', font_size=30, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font))

        # 选择登录/注册
        self.is_in = True

        self.choose_sign_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5}, spacing=20)

        self.sign_in = Button(text="Sign in", size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
        setattr(self.sign_in, 'state', 'down')
        self.sign_in.bind(on_press=lambda x: self.do_sign_in())
        self.choose_sign_box.add_widget(self.sign_in)

        self.sign_up = Button(text="Sign up", size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
        self.sign_up.bind(on_press=lambda x: self.do_sign_up())
        self.choose_sign_box.add_widget(self.sign_up)

        layout.add_widget(self.choose_sign_box)

        # 用户名输入
        self.username_box = BoxLayout(orientation='vertical', spacing=-30, size_hint=(1, 0.1))
        self.username_box.add_widget(Label(text='User Name', font_size=30, pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font))
        self.username = TextInput(multiline=False, size_hint=(0.6, 0.35), pos_hint={'center_x': 0.5}, font_name=word_font)
        self.username.background_color = textbox_color
        self.username.foreground_color = input_word_color
        self.username.bind(on_text_validate=self.do_go)
        self.username_box.add_widget(self.username)
        layout.add_widget(self.username_box)

        # 密码输入
        self.password_box = BoxLayout(orientation='vertical', spacing=-30, size_hint=(1, 0.1))
        self.password_box.add_widget(Label(text='Password', font_size=30, pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font))
        self.password = TextInput(password=True, multiline=False, size_hint=(0.6, 0.35), pos_hint={'center_x': 0.5}, font_name=word_font)
        self.password.background_color = textbox_color
        self.password.foreground_color = input_word_color
        self.password.bind(on_text_validate=self.do_go)
        self.password_box.add_widget(self.password)
        layout.add_widget(self.password_box)

        # 确认按钮
        self.sign_box = BoxLayout(orientation='horizontal', size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5}, spacing=20)
        self.sign = Button(text="Go!", size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=30)
        self.sign.bind(on_press=lambda x: self.do_go())
        self.sign_box.add_widget(self.sign)

        layout.add_widget(self.sign_box)

        # 添加layout
        self.add_widget(layout)

    def do_sign_in(self):
        self.sign_in.bind(on_release=lambda x: setattr(self.sign_in, 'state', 'down'))
        self.sign_in.bind(on_release=lambda x: setattr(self.sign_up, 'state', 'normal'))
        self.is_in = True


    def do_sign_up(self):
        self.sign_up.bind(on_release=lambda x: setattr(self.sign_up, 'state', 'down'))
        self.sign_up.bind(on_release=lambda x: setattr(self.sign_in, 'state', 'normal'))
        self.is_in = False

    def do_go(self, instance=None):
        if self.username.text == '' or self.password.text == '':
            popup = Popup(title='Error', content=Label(text='Please enter your username and password.', text_size=(300, None), font_name=word_font), size=(400, 200), size_hint=(None, None), title_font=word_font)
            popup.open()
        else:
            is_success, word = self.client_manager.sign_api(is_in=self.is_in, user_name=self.username.text, password=self.password.text)
            print(is_success)
            # is_success, word = True, 'Success' # 注释这一行
            if is_success:
                popup = Popup(title='Success', content=Label(text=word, text_size=(300, None), font_name=word_font), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()
                popup.bind(on_dismiss=lambda x: self.go_to_main())
                self.username.text = ''
                self.password.text = ''
            else:
                popup = Popup(title='Error', content=Label(text=word, text_size=(300, None), font_name=word_font), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()

    def go_to_main(self):
        # 跳转到MainScreen
        self.main_flag = True
        App.get_running_app().root.current = 'main'

class DebugApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(None, name='login'))
        return sm
    
if __name__ == '__main__':
    DebugApp().run()