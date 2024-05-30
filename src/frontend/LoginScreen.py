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
    'title': '欢迎使用易思', 
    'sign in': '登录',
    'sign up': '注册',
    'user name': '交大邮箱',
    'password': '密码',
    'go': '开始！',
    'error': '出错啦！',
    'success': '好欸！',
    'please enter': '请输入用户名和密码。',
    'language': 'English version',
    'User already exists!': '用户已存在！',
    'User already online!': '用户已在线！',
    'Sign in successfully!': '登录成功！',
    'Sign up successfully!': '注册成功！',
    'No such user!': '此用户不存在！',
    'Wrong password!': '密码错误！',
    'username format error1': '请输入交大邮箱',
    'username format error2': '邮箱地址只能包含数字、大小写字母以及“@_.”！',
    'password format error1': '密码只能包含数字、大小写字母以及“@_.”！',
    'password format error2': '密码长度必须在6-20位之间！',
    'auth_code_error': '验证码发送失败，请重试！',
}

en_texts = {
    'title': 'Welcome to EASEchat', 
    'sign in': 'Sign in',
    'sign up': 'Sign up',
    'user name': 'SJTU Email',
    'password': 'Password',
    'go': 'Go!',
    'error': 'Error',
    'success': 'Success',
    'please enter': 'Please enter your username and password.',
    'language': '中文版',
    'User already exists!': 'User already exists!',
    'User already online!': 'User already online!',
    'Sign in successfully!': 'Sign in successfully!',
    'Sign up successfully!': 'Sign up successfully!',
    'No such user!': 'No such user!',
    'Wrong password!': 'Wrong password!',
    'username format error1': 'Please enter SJTU email address',
    'username format error2': 'Email address can only contain numbers, letters and \"@_.\"!',
    'password format error1': 'Password can only contain numbers, letters and \"@_.\"!',
    'password format error2': 'Password length must be between 6 and 20!',
    'auth_code_error': 'Failed to send auth code, please try again!',
}

class LoginScreen(Screen):

    def __init__(self, my_name, manager, language, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.client_manager = manager
        self.my_name = my_name
        self.language_version = language
        if self.language_version[0] == 'zh':
            self.texts = zh_texts
        else:
            self.texts = en_texts

    def on_enter(self):
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[0, 50, 0, 0])
        # 标题
        self.title_box= BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=-100)
        self.title = BoxLayout(orientation='horizontal', pos_hint={'center_x': 0.5}, spacing=-300)
        self.title.add_widget(Label(text=self.texts['title'], font_size=70, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font))
        # self.title.add_widget(Image(source=r'src\logo.png'))
        self.title_box.add_widget(self.title)
        self.title_box.add_widget(Label(text='Efficient And SEcure chat', font_size=30, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font))
        self.layout.add_widget(self.title_box)

        # 选择登录/注册
        self.is_in = True

        self.choose_sign_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5}, spacing=20)

        self.sign_in = Button(text=self.texts['sign in'], size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=30)
        setattr(self.sign_in, 'state', 'down')
        self.sign_in.bind(on_press=lambda x: self.do_sign_in())
        self.choose_sign_box.add_widget(self.sign_in)

        self.sign_up = Button(text=self.texts['sign up'], size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=30)
        self.sign_up.bind(on_press=lambda x: self.do_sign_up())
        self.choose_sign_box.add_widget(self.sign_up)

        self.layout.add_widget(self.choose_sign_box)

        # 用户名输入
        self.username_box = BoxLayout(orientation='vertical', spacing=-30, size_hint=(1, 0.1))
        self.username_title = Label(text=self.texts['user name'], font_size=30, pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font)
        self.username_box.add_widget(self.username_title)
        self.username = TextInput(multiline=False, size_hint=(0.6, 0.35), pos_hint={'center_x': 0.5}, font_name=word_font, text='@sjtu.edu.cn')
        self.username.background_color = textbox_color
        self.username.foreground_color = input_word_color
        self.username.bind(on_text_validate=self.do_go)
        self.username_box.add_widget(self.username)
        self.layout.add_widget(self.username_box)

        # 密码输入
        self.password_box = BoxLayout(orientation='vertical', spacing=-30, size_hint=(1, 0.1))
        self.password_title = Label(text=self.texts['password'], font_size=30, pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font)
        self.password_box.add_widget(self.password_title)
        self.password = TextInput(password=True, multiline=False, size_hint=(0.6, 0.35), pos_hint={'center_x': 0.5}, font_name=word_font)
        self.password.background_color = textbox_color
        self.password.foreground_color = input_word_color
        self.password.bind(on_text_validate=self.do_go)
        self.password_box.add_widget(self.password)
        self.layout.add_widget(self.password_box)

        # 确认按钮
        self.sign_box = BoxLayout(orientation='horizontal', size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5}, spacing=20)
        self.sign = Button(text=self.texts['go'], size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=30)
        self.sign.bind(on_press=lambda x: self.do_go())
        self.sign_box.add_widget(self.sign)

        self.layout.add_widget(self.sign_box)

        # 添加中英文切换按钮
        self.language_box = BoxLayout(orientation='horizontal', size_hint=(0.2, 0.05), pos_hint={'center_x': 0.1}, spacing=20)
        self.language = Button(text=self.texts['language'], size_hint=(0.3, 1), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=30)
        self.language.bind(on_press=lambda x: self.change_language())
        self.language_box.add_widget(self.language)
        self.layout.add_widget(self.language_box)

        # 添加layout
        self.add_widget(self.layout)

    def do_sign_in(self):
        self.sign_in.bind(on_release=lambda x: setattr(self.sign_in, 'state', 'down'))
        self.sign_in.bind(on_release=lambda x: setattr(self.sign_up, 'state', 'normal'))
        self.is_in = True


    def do_sign_up(self):
        self.sign_up.bind(on_release=lambda x: setattr(self.sign_up, 'state', 'down'))
        self.sign_up.bind(on_release=lambda x: setattr(self.sign_in, 'state', 'normal'))
        self.is_in = False

    def do_go(self, instance=None):
        if self.username.text == '' or self.password.text == '' or self.username.text == '@sjtu.edu.cn':
            popup = Popup(title=self.texts['error'], content=Label(text=self.texts['please enter'], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
            popup.open()
        else:
            # 检查用户名和密码格式
            if not self.username.text.endswith('@sjtu.edu.cn'):
                popup = Popup(title=self.texts['error'], content=Label(text=self.texts['username format error1'], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()
                return

            user_name_is_formatted = login_filter(self.username.text)
            if not user_name_is_formatted:
                popup = Popup(title=self.texts['error'], content=Label(text=self.texts['username format error2'], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()
                return

            password_is_formatted = login_filter(self.password.text)
            if not password_is_formatted:
                popup = Popup(title=self.texts['error'], content=Label(text=self.texts['password format error1'], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()
                return
            
            if len(self.password.text) < 6 or len(self.password.text) > 20:
                popup = Popup(title=self.texts['error'], content=Label(text=self.texts['password format error2'], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()
                return

            # 登录/注册
            if self.is_in:  # 登录
                is_success, word = self.client_manager.sign_in_api(user_name=self.username.text.replace('@sjtu.edu.cn', ''), password=self.password.text)
                # is_success, word = True, 'Sign in successfully!' # 注释这一行
            else:           # 注册
                is_send = self.client_manager.sign_up_api(user_name=self.username.text.replace('@sjtu.edu.cn', ''), password=self.password.text)
                # is_send = True # 注释这一行
                if not is_send:
                    popup = Popup(title=self.texts['error'], content=Label(text=self.texts['auth_code_error'], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                    popup.open()
                    return
                else:
                    self.layout.clear_widgets()
                    self.my_name[0] = self.username.text.replace('@sjtu.edu.cn', '')
                    App.get_running_app().root.current = 'authcode'
                    return
            # is_success, word = True, 'Success' # 注释这一行
            if is_success:
                self.my_name[0] = self.username.text.replace('@sjtu.edu.cn', '')
                popup = Popup(title=self.texts['success'], content=Label(text=self.texts[word], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()
                popup.bind(on_dismiss=lambda x: self.go_to_main())
                self.username.text = ''
                self.password.text = ''
            else:
                popup = Popup(title=self.texts['error'], content=Label(text=self.texts[word], text_size=(300, None), font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                popup.open()

    def change_language(self):
        if self.language_version[0] == 'zh':
            self.language_version[0] = 'en'
            self.texts = en_texts
        else:
            self.language_version[0] = 'zh'
            self.texts = zh_texts
        self.title_box.clear_widgets()
        self.title_box.add_widget(Label(text=self.texts['title'], font_size=70, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font))
        self.title_box.add_widget(Label(text='Efficient And SEcure chat', font_size=30, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font))
        self.sign_in.text = self.texts['sign in']
        self.sign_up.text = self.texts['sign up']
        self.username_title.text = self.texts['user name']
        self.password_title.text = self.texts['password']
        self.sign.text = self.texts['go']
        self.language.text = self.texts['language']

    def go_to_main(self):
        # 跳转到MainScreen
        self.layout.clear_widgets()
        self.main_flag = True
        App.get_running_app().root.current = 'main'


class DebugApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(None, name='login'))
        return sm
    
if __name__ == '__main__':
    DebugApp().run()