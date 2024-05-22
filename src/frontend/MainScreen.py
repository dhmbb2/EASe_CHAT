from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from frontend.utils import *

word_color = hex_to_rgb('#CCCCCC')

title_font = 'src/fonts/AcademyEngravedStd.otf'
word_font = 'src/fonts/Consolas.ttf'

class MainScreen(Screen):
    def __init__(self, manager, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.client_manager = manager
        self.user_list = []
        self.list_is_changed = True
        self.layout = BoxLayout(orientation='vertical', spacing=-100, padding=[0, -70, 0, 70])
        # 查询在线名单
        Clock.schedule_interval(self.get_user_list, 1)

        # 显示在线名单
        if self.list_is_changed:
            for user in self.user_list:
                user_box = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.03), pos_hint={'center_x': 0.5}, spacing=20)
                user_botton = Button(text=user, size_hint=(0.3, 1), pos_hint={'center_x': 0.5})
                # user_botton.bind(on_press=lambda x: self.do_go())
                user_box.add_widget(user_botton)

                self.layout.add_widget(user_box)

        self.add_widget(self.layout)

    def get_user_list(self, dt):
        # user_list = self.client_manager.get_user_list_api()
        user_list = []
        # for i in range(50):
        #     user_list.append('user' + str(i+1))
        # user_list = [user_list[i:i+4] for i in range(0, len(user_list), 4)]

        if user_list != self.user_list:
            self.user_list = user_list
            self.list_is_changed = True
        else:
            self.list_is_changed = False

        self.show_user_list()

    def show_user_list(self):
        # 显示在线名单
        if self.list_is_changed:
            self.layout.clear_widgets()
            # 显示标题
            title_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
            title_box.add_widget(Label(text='Start CHAT to your friends!', font_size=50, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font, size_hint=(0.8, 1)))
            exit_button = Button(font_size=50, text='X', size_hint=(0.2, 1), background_normal='', background_color=[0,0,0,0], font_name=title_font, color=word_color)
            exit_button.bind(on_press=lambda x: self.do_exit())
            title_box.add_widget(exit_button)
            self.layout.add_widget(title_box)
            
            # 创建一个ScrollView
            scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
            # 创建一个BoxLayout，将其添加到ScrollView中
            user_box = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=100, padding=[0, 100, 0, 20])
            user_box.bind(minimum_height=user_box.setter('height'))
            
            for users in self.user_list:
                user_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=40)
                block_num = 4 - len(users)
                user_buttons.add_widget(Widget())
                for user in users:
                    user_button = Button(text=user, size_hint_y=None, height=Window.height*0.1, color=word_color, font_name=word_font, font_size=25)
                    user_button.bind(on_press=lambda x, user=user: self.do_chat(user))
                    user_buttons.add_widget(user_button)
                for i in range(block_num+1):
                    user_buttons.add_widget(Widget())
                user_box.add_widget(user_buttons)

            scroll_view.add_widget(user_box)
            self.layout.add_widget(scroll_view)

            if self.layout.parent:
                self.layout.parent.remove_widget(self.layout)
            self.add_widget(self.layout)

    def do_chat(self, user):
        # 获取 ChatScreen 实例并设置 chat_with 属性
        chat_screen = App.get_running_app().root.get_screen('chat')
        chat_screen.chat_with = user
        # 跳转到 ChatScreen
        App.get_running_app().root.current = 'chat'

    def do_exit(self):
        App.get_running_app().root.current = 'login'



class DebugApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(None, name='main'))
        return sm
    
if __name__ == '__main__':
    DebugApp().run()