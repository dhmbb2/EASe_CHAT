import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from backend.apis import ClientManager

manager = ClientManager(HOST = "127.0.0.1", PORT = 11451)

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [0, 100, 0, 200] # padding: [left, top, right, bottom]
        layout = BoxLayout(orientation='vertical', spacing=20)

        self.title_box= BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.title_box.add_widget(Label(text='Welcome to the Login Screen', font_size=50, pos_hint={'center_x': 0.5}))
        layout.add_widget(self.title_box)

        # 选择登录/注册
        self.is_in = True

        self.choose_sign_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5}, spacing=20)

        self.sign_in = Button(text="Sign in", size_hint=(0.3, 1), pos_hint={'center_x': 0.5})
        setattr(self.sign_in, 'state', 'down')
        self.sign_in.bind(on_press=lambda x: self.do_sign_in())
        self.choose_sign_box.add_widget(self.sign_in)

        self.sign_up = Button(text="Sign up", size_hint=(0.3, 1), pos_hint={'center_x': 0.5})
        self.sign_up.bind(on_press=lambda x: self.do_sign_up())
        self.choose_sign_box.add_widget(self.sign_up)

        layout.add_widget(self.choose_sign_box)

        # 用户名输入
        self.username_box = BoxLayout(orientation='vertical', spacing=-30, size_hint=(1, 0.1))
        self.username_box.add_widget(Label(text='User Name', font_size=30, pos_hint={'center_x': 0.5}))
        self.username = TextInput(multiline=False, size_hint=(0.6, 0.4), pos_hint={'center_x': 0.5})
        self.username_box.add_widget(self.username)
        layout.add_widget(self.username_box)

        # 密码输入
        self.password_box = BoxLayout(orientation='vertical', spacing=-30, size_hint=(1, 0.1))
        self.password_box.add_widget(Label(text='Password', font_size=30, pos_hint={'center_x': 0.5}))
        self.password = TextInput(password=True, multiline=False, size_hint=(0.6, 0.4), pos_hint={'center_x': 0.5})
        self.password_box.add_widget(self.password)
        layout.add_widget(self.password_box)

        # 确认按钮
        self.sign_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.03), pos_hint={'center_x': 0.5}, spacing=20)
        self.sign = Button(text="Go!", size_hint=(0.3, 1), pos_hint={'center_x': 0.5})
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

    def do_go(self):
        global manager

        if self.username.text == '' or self.password.text == '':
            popup = Popup(title='Error', content=Label(text='Please enter your username and password', text_size=(300, None)), size=(400, 200), size_hint=(None, None))
            popup.open()
        else:
            is_success, word = manager.sign_api(is_in=self.is_in, user_name=self.username.text, password=self.password.text)

            popup = Popup(title='Sign in', content=Label(text=word, text_size=(300, None)), size=(400, 200), size_hint=(None, None))

        # 到时候下面删掉
        # elif self.is_in:
        #     # 登录

        #     popup = Popup(title='Sign in', content=Label(text=f'Sign in successfully, your username is {self.username.text}, your password is {self.password.text}', text_size=(300, None)), size=(400, 200), size_hint=(None, None))
        #     popup.open()
        # else:
        #     # 注册
        #     popup = Popup(title='Sign up', content=Label(text=f'Sign up successfully, your username is {self.username.text}, your password is {self.password.text}', text_size=(300, None)), size=(400, 200), size_hint=(None, None))
            popup.open()
        # 到时候上面删掉



class CHAT(App):
    def build(self):
        self.title = 'Login Screen'
        Window.size = (800, 600)
        Window.bind(on_resize=self.on_window_resize)
        return LoginScreen()
    
    def on_window_resize(self, window, width, height):
        if width > 800 or height > 600:
            window.size = (800, 600)




if __name__ == '__main__':
    CHAT().run()