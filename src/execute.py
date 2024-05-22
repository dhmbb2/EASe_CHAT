from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from frontend.LoginScreen import LoginScreen
from frontend.MainScreen import MainScreen
from frontend.ChatScreen import ChatScreen
from backend.apis import ClientManager
from frontend.utils import hex_to_rgb


class WindowManager(ScreenManager):
    pass

class CHAT(App):
    def build(self):
        self.title = 'EASE'
        Window.size = (800, 600)
        Window.clearcolor = hex_to_rgb('#282828')
        self.manager = ClientManager(HOST = "127.0.0.1",PORT = 11451)
        # self.manager = None
        Window.bind(on_resize=self.on_window_resize)
        wm = WindowManager()
        wm.add_widget(LoginScreen(self.manager, name='login'))
        wm.add_widget(MainScreen(self.manager, name='main'))
        wm.add_widget(ChatScreen(self.manager, name='chat'))
        return wm
    
    def on_window_resize(self, window, width, height):
        if width > 800 or height > 600:
            window.size = (800, 600)

    def on_stop(self):
        self.manager.xx_api()

if __name__ == '__main__':
    CHAT().run()