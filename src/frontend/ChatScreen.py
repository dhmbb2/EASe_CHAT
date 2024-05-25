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
from datetime import datetime


word_color = hex_to_rgb('#CCCCCC')
my_word_color = hex_to_rgb('#4EC9B0')
word_background_color = my_word_color
my_word_background_color = word_color
textbox_color = hex_to_rgb('#CACACA')
input_word_color = hex_to_rgb('#282828')

title_font = 'src/fonts/FZFWZhuZGDSMCJW.TTF'
word_font = 'src/fonts/FZFWZhuZGDSMCJW.TTF'

zh_texts = {
    'message': '发送消息', 
    'file': '发送文件',
    'download': '下载',
    'downloaded': '已下载',
    'file_tag': '文件',
    'download_warning': '下载出错',
    'choose_file': '选择文件',
}

en_texts = {
    'message': 'Send a message', 
    'file': 'Send a file',
    'download': 'Download',
    'downloaded': 'Downloaded',
    'file_tag': 'File',
    'download_warning': 'Download warning',
    'choose_file': 'Choose a file',
}

class ChatScreen(Screen):
    chat_with = StringProperty()
    user_chat_with = None

    def __init__(self, my_name, manager, language, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.client_manager = manager
        self.my_name = my_name
        self.language_version = language
        self.old_packages = []
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


        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[0, 50, 0, 0])

        # 显示聊天对象名称
        self.title_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.exit_button = Button(font_size=70, text='X', size_hint=(0.2, 1), background_normal='', background_color=[0,0,0,0], font_name=title_font, color=word_color)
        self.exit_button.bind(on_press=lambda x: self.do_exit())

        if self.title_label.parent:
            self.title_label.parent.remove_widget(self.title_label)
        self.title_box.add_widget(self.title_label)
        self.title_box.add_widget(self.exit_button)
        self.layout.add_widget(self.title_box)

        # 显示历史信息
        self.history_scroll = ScrollView(size_hint=(1, 0.725))
        if self.history_box.parent:
            self.history_box.parent.remove_widget(self.history_box)
        self.history_scroll.add_widget(self.history_box)
        self.layout.add_widget(self.history_scroll)

        # 显示输入框
        self.input_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.175), spacing=0)
        self.layout.add_widget(self.input_box)

        # 输入框
        self.input = WrapTextInput(self, background_color=textbox_color, word_color=input_word_color, font_size=25, font_name=word_font)
        self.input.on_text_validate = self.do_send_message  # 当 WrapTextInput 的 on_text_validate 事件被触发时，调用 do_send_mess
        self.input.bind(on_text_validate=self.do_send_message)
        self.input_box.add_widget(self.input)
        # 按钮
        self.button = BoxLayout(orientation='vertical', size_hint=(0.2, 1), spacing=0)
        # 发送消息按钮
        self.send_message_button = Button(text=self.texts['message'], size_hint=(1, 0.5), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
        self.send_message_button.bind(on_press=self.do_send_message)
        self.button.add_widget(self.send_message_button)
        # 发送文件按钮
        self.send_message_button = Button(text=self.texts['file'], size_hint=(1, 0.5), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
        self.send_message_button.bind(on_press=self.do_send_file)
        self.button.add_widget(self.send_message_button)
        self.input_box.add_widget(self.button)

        # 加载历史信息
        # 注释掉下一段
        # self.history = [' '*90, 'You: Hello', f'{self.user_chat_with}: Hi', 'You: How are you?', f'{self.user_chat_with}: Fine, thank you. And you?', 'You: I am fine too. Thank you.', f'{self.user_chat_with}: Bye', 'You: Bye']
        # self.load_history()

        # # 读取服务器信息
        self.clock_event = Clock.schedule_interval(self.do_get_message, 0.01)

        self.add_widget(self.layout)

    def on_chat_with(self, instance, value):
        # 初始化
        self.title_label = Label(font_size=70, pos_hint={'center_x': 0.5}, color=word_color, font_name=title_font)
        self.history_box = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=0)
        self.user_chat_with = value

    # def load_history(self):
    #     self.history_label.text = '\n'.join(self.history) + '\n '
    #     self.history_label.height = self.history_label.texture_size[1]

    def do_get_message(self, dt):
        if self.language_version[0] == 'zh':
            self.title_label.text = f'在和{self.user_chat_with}聊天'
        else:
            self.title_label.text = f'Chating with {self.user_chat_with}'
        packages = self.client_manager.get_message_api(self.user_chat_with)


        # self.history = [' '*90]
        if packages != self.old_packages or self.language_is_changed:
            self.language_is_changed = False
            self.old_packages = packages.copy()
            self.history_box.clear_widgets()
            self.input_box.clear_widgets()

            # 输入框
            self.input = WrapTextInput(self, background_color=textbox_color, word_color=input_word_color, font_size=25, font_name=word_font)
            self.input.on_text_validate = self.do_send_message  # 当 WrapTextInput 的 on_text_validate 事件被触发时，调用 do_send_mess
            self.input.bind(on_text_validate=self.do_send_message)
            self.input_box.add_widget(self.input)
            # 按钮
            self.button = BoxLayout(orientation='vertical', size_hint=(0.2, 1), spacing=0)
            # 发送消息按钮
            self.send_message_button = Button(text=self.texts['message'], size_hint=(1, 0.5), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
            self.send_message_button.bind(on_press=self.do_send_message)
            self.button.add_widget(self.send_message_button)
            # 发送文件按钮
            self.send_message_button = Button(text=self.texts['file'], size_hint=(1, 0.5), pos_hint={'center_x': 0.5}, color=word_color, font_name=word_font, font_size=25)
            self.send_message_button.bind(on_press=self.do_send_file)
            self.button.add_widget(self.send_message_button)
            self.input_box.add_widget(self.button)

            # self.history_box.add_widget(Label(text=(' '+'1\n')*10, font_size=25, color=word_color, font_name=word_font, size_hint=(1, None), height=50))
            for package in packages:
                user, time, item = package
                # item = ('file', 'test.txt', True)
                if item[0] == 'message':
                    if user == self.user_chat_with:
                        text = f'({time}) {user}:\n{item[1]}'
                        message = Label(text=text, halign='left', font_size=25, color=word_color, font_name=word_font, size_hint=(1, None))
                        message.bind(texture_size=message.setter('size'), width=lambda s, w: s.setter('text_size')(s, (w, None)))
                        self.history_box.add_widget(message)
                        # self.history.append(f'({time}) {user}: {item[1]}')
                    else:
                        text = f'({time}) {self.my_name[0]}:\n{item[1]}'
                        message = Label(text=text, halign='left', font_size=25, color=my_word_color, font_name=word_font, size_hint=(1, None))
                        message.bind(texture_size=message.setter('size'), width=lambda s, w: s.setter('text_size')(s, (w, None)))
                        self.history_box.add_widget(message)
                        # self.history.append(f'({time}) {user}: {item[1]}')
                elif item[0] == 'file':
                    # self.history.append(f'({time}) {user}: [file] {item[1]}')
                    file_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
                    if user == self.user_chat_with:
                        text = f"({time}) {user}:\n[{self.texts['file_tag']}] {item[1]}"
                        message = Label(text=text, halign='left', font_size=25, color=word_color, font_name=word_font, size_hint=(0.85, None))
                        message.bind(texture_size=message.setter('size'), width=lambda s, w: s.setter('text_size')(s, (w, None)))
                        file_box.add_widget(message)
                        if type(item[2]) == str:
                            # download_button = Button(text='Download', size_hint=(0.15, 1), color=word_color, font_name=word_font, font_size=25)
                            # download_button.bind(on_press=lambda x: self.do_get_file(item[1]))
                            # file_box.add_widget(download_button)
                            popup = Popup(title=self.texts['download_warning'], content=Label(text=item[2], color=word_color, font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                            popup.open()
                        elif item[2]:
                            download_button = Button(text=self.texts['download'], size_hint=(0.15, 1), color=word_color, font_name=word_font, font_size=25)
                            download_button.bind(on_press=lambda x: self.do_download_file(item[1]))
                            file_box.add_widget(download_button)
                        elif not item[2]:
                            file_box.add_widget(Label(text=self.texts['downloaded'], halign='left', font_size=25, color=word_color, size_hint=(0.15, 1), font_name=word_font,height=50))
                        self.history_box.add_widget(file_box)
                    else:
                        text = f"({time}) {self.my_name[0]}:\n[{self.texts['file_tag']}] {item[1]}"
                        message = Label(text=text, halign='left', font_size=25, color=my_word_color, font_name=word_font, size_hint=(0.85, None))
                        message.bind(texture_size=message.setter('size'), width=lambda s, w: s.setter('text_size')(s, (w, None)))
                        # file_box.bind(minimum_height=message.setter('height'))
                        file_box.add_widget(message)
                        if type(item[2]) == str:
                            # download_button = Button(text='Download', size_hint=(0.15, 1), color=word_color, font_name=word_font, font_size=25)
                            # download_button.bind(on_press=lambda x: self.do_get_file(item[1]))
                            # file_box.add_widget(download_button)
                            popup = Popup(title=self.texts['download_warning'], content=Label(text=item[2], color=word_color, font_name=word_font, font_size=25), size=(400, 200), size_hint=(None, None), title_font=word_font)
                            popup.open()
                        elif item[2]:
                            download_button = Button(text=self.texts['download'], size_hint=(0.15, 1), color=word_color, font_name=word_font, font_size=25)
                            download_button.bind(on_press=lambda x: self.do_download_file(item[1]))
                            file_box.add_widget(download_button)
                        elif not item[2]:
                            file_box.add_widget(Label(text=self.texts['downloaded'], halign='left', font_size=25, color=my_word_color, size_hint=(0.15, 1), font_name=word_font,height=50))
                        self.history_box.add_widget(file_box)
            self.history_box.bind(minimum_height=self.history_box.setter('height'))

        # self.load_history()

    def do_send_message(self, instance=None):
        # 注释掉下一段
        # new_message = f'({get_time()}) You: {self.input.text}'
        # new_message = textwrap.fill(new_message, 90)
        # self.history.append(new_message)
        # self.load_history()

        item = ('message', self.input.text_input.text, False)
        package = (self.user_chat_with, get_time(), item)
        self.client_manager.send_message_api(package)

        # 清空输入框
        self.input.text = ''
        self.input.text_input.text = ''

    def do_send_file(self, instance):
        # 创建一个 FileChooser 控件
        filechooser = FileChooserIconView(font_name=word_font)
        # 创建一个 Popup 控件
        self.files_popup = Popup(title=self.texts['choose_file'], content=filechooser, size_hint=(0.9, 0.9), title_font=word_font)
        # 绑定 on_selection 事件
        filechooser.bind(on_submit=self.on_file_selection)
        # 打开 Popup 控件
        self.files_popup.open()

    def on_file_selection(self, instance, value, _):

        # 注释掉下一段
        # self.history.append(f'({get_time()}) You: [file] {value[0]}')
        # self.load_history()

        item = ('file', value[0], False)
        package = (self.user_chat_with, get_time(), item)
        self.client_manager.send_message_api(package)

        self.files_popup.dismiss()

    def do_download_file(self, file_name):
        self.client_manager.download_file_api(self.user_chat_with, file_name)

    def on_leave(self):
        Clock.unschedule(self.clock_event)
        self.clock_event = None

    def do_exit(self):
        Clock.unschedule(self.clock_event)
        self.clock_event = None
        self.clear_widgets()
        App.get_running_app().root.current = 'main'