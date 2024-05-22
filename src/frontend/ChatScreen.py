import textwrap
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import StringProperty
from frontend.utils import *


word_color = hex_to_rgb('#CCCCCC')
textbox_color = hex_to_rgb('#CACACA')
input_word_color = hex_to_rgb('#282828')

title_font = 'src/fonts/AcademyEngravedStd.otf'
word_font = 'src/fonts/Consolas.ttf'

class MyTextInput(TextInput):
    MAX_LINE_LENGTH = 90  # 每行最多的字符数

    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.plain_text = ''

    def insert_text(self, substring, from_undo=False):
        lines = self.text.split('\n')
        if len(lines[-1]) + len(substring) > self.MAX_LINE_LENGTH:
            substring = '\n' + substring
        self.plain_text += substring.replace('\n', '')
        return super(MyTextInput, self).insert_text(substring, from_undo=from_undo)

class ChatScreen(Screen):
    chat_with = StringProperty()
    user_chat_with = None

    def __init__(self, manager, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.client_manager = manager

    def on_enter(self):
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[0, 50, 0, 0])

        # 显示聊天对象名称
        self.title_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.exit_button = Button(font_size=70, text='X', size_hint=(0.2, 1), background_normal='', background_color=[0,0,0,0], font_name=title_font, color=word_color)
        self.exit_button.bind(on_press=lambda x: self.do_exit())

        self.title_box.add_widget(self.title_label)
        self.title_box.add_widget(self.exit_button)
        self.layout.add_widget(self.title_box)

        # 显示历史信息
        self.history_scroll = ScrollView(size_hint=(1, 0.6), pos_hint={'center_x': 0.5}, scroll_type=['bars', 'content'])
        self.history_scroll.add_widget(self.history_label)
        self.layout.add_widget(self.history_scroll)

        # 显示输入框
        self.input_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.175), spacing=0)
        self.input = MyTextInput(multiline=False, size_hint=(0.8, 1), pos_hint={'center_x': 0.5}, font_name=word_font)
        self.input.background_color = textbox_color
        self.input.foreground_color = input_word_color
        self.input.bind(on_text_validate=self.do_send_message)
        self.input_box.add_widget(self.input)
        # 按钮
        self.button = BoxLayout(orientation='vertical', size_hint=(0.2, 1), spacing=0)
        # 发送消息按钮
        self.send_message_button = Button(text='Send a message', size_hint=(1, 0.5), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
        self.send_message_button.bind(on_press=self.do_send_message)
        self.button.add_widget(self.send_message_button)
        # 发送文件按钮
        self.send_message_button = Button(text='Send a file', size_hint=(1, 0.5), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
        self.send_message_button.bind(on_press=self.do_send_file)
        self.button.add_widget(self.send_message_button)

        self.input_box.add_widget(self.button)

        self.layout.add_widget(self.input_box)

        # 加载历史信息
        # 注释掉下一段
        # self.history = [' '*90, 'You: Hello', f'{self.user_chat_with}: Hi', 'You: How are you?', f'{self.user_chat_with}: Fine, thank you. And you?', 'You: I am fine too. Thank you.', f'{self.user_chat_with}: Bye', 'You: Bye']
        # self.load_history()

        # # 读取服务器信息
        Clock.schedule_interval(self.do_get_messgae, 0.01)

        self.add_widget(self.layout)

    def on_chat_with(self, instance, value):
        # 初始化
        self.title_label = Label(font_size=70, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font)
        self.history_label = Label(size_hint_y=None, font_name=word_font, halign='left')
        self.user_chat_with = value
        self.title_label.text = f'Chat with {value}'

    def load_history(self):
        self.history_label.text = '\n'.join(self.history) + '\n '
        self.history_label.height = self.history_label.texture_size[1]

    def do_get_messgae(self, dt):
        packages = self.client_manager.get_message_api(self.user_chat_with)
        self.history = [' '*90]
        for package in packages:
            user, time, item = package
            if item[0] == 'message':
                self.history.append(f'({time}) {user}: {item[1]}')
            elif item[0] == 'file':
                self.history.append(f'({time}) {user}: [file] {item[1]}')

        self.load_history()

    def do_send_message(self, instance):
        # 注释掉下一段
        # new_message = f'({get_time()}) You: {self.input.plain_text}'
        # new_message = textwrap.fill(new_message, 90)
        # self.history.append(new_message)
        # self.load_history()

        item = ('message', self.input.plain_text)
        package = (self.user_chat_with, get_time(), item)
        self.client_manager.send_message_api(package)

        # 清空输入框
        self.input.text = ''
        self.input.plain_text = ''

    def do_send_file(self, instance):
        # 创建一个 FileChooser 控件
        filechooser = FileChooserIconView()
        # 创建一个 Popup 控件
        self.files_popup = Popup(title='Choose a file', content=filechooser, size_hint=(0.9, 0.9))
        # 绑定 on_selection 事件
        filechooser.bind(on_submit=self.on_file_selection)
        # 打开 Popup 控件
        self.files_popup.open()

    def on_file_selection(self, instance, value, _):

        # 注释掉下一段
        # self.history.append(f'({get_time()}) You: [file] {value[0]}')
        # self.load_history()

        item = ('file', value[0])
        package = (self.user_chat_with, get_time(), item)
        self.client_manager.send_message_api(package)

        self.files_popup.dismiss()

    def do_exit(self):
        self.clear_widgets()
        App.get_running_app().root.current = 'main'