from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(50):
            lbl = Label(text='Label ' + str(i), size_hint_y=None, height=40, halign='left')
            lbl.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))
            layout.add_widget(lbl)

        root = ScrollView()
        root.add_widget(layout)
        return root

if __name__ == '__main__':
    MyApp().run()