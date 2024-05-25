from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime

class MyScreen(Screen):
    def __init__(self, **kwargs):
        super(MyScreen, self).__init__(**kwargs)
        self.layout = BoxLayout()
        self.add_widget(self.layout)

    def on_enter(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Button(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.screen1 = MyScreen(name='screen1')
        self.screen2 = MyScreen(name='screen2')
        self.add_widget(self.screen1)
        self.add_widget(self.screen2)

    def switch_screen(self):
        if self.current == 'screen1':
            self.current = 'screen2'
        else:
            self.current = 'screen1'

class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        switch_button = Button(text='Switch screen')
        switch_button.bind(on_release=lambda x: sm.switch_screen())
        root = BoxLayout(orientation='vertical')
        root.add_widget(sm)
        root.add_widget(switch_button)
        return root

if __name__ == '__main__':
    MyApp().run()