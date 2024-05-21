from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

class MainWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text='Go to Second Window', on_press=self.change_window))

    def change_window(self, instance):
        self.manager.current = 'second'

class SecondWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text='Go to Main Window', on_press=self.change_window))

    def change_window(self, instance):
        self.manager.current = 'main'

class WindowManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        self.title = 'Window Manager'
        wm = WindowManager()
        wm.add_widget(MainWindow(name='main'))
        wm.add_widget(SecondWindow(name='second'))
        return wm

if __name__ == '__main__':
    MyApp().run()