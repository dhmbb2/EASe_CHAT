from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from frontend.LoginScreen import LoginScreen
from frontend.MainScreen import MainScreen
from backend.apis import ClientManager


class WindowManager(ScreenManager):
    pass

class CHAT(App):
    def build(self):
        self.title = 'CHAT'
        Window.size = (800, 600)
        self.manager = ClientManager(HOST = "127.0.0.1",PORT = 11451)
        Window.bind(on_resize=self.on_window_resize)
        wm = WindowManager()
        wm.add_widget(LoginScreen(self.manager, name='login'))
        wm.add_widget(MainScreen(name='main'))
        return wm
    
    def on_window_resize(self, window, width, height):
        if width > 800 or height > 600:
            window.size = (800, 600)

if __name__ == '__main__':
    CHAT().run()