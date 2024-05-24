import os
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
# 将中文字体存放在某一个目录下，建议使用相对路径
resource_add_path(os.path.abspath(r".\src\fonts"))
# 替换掉默认字体
LabelBase.register("Roboto", "FZYanZQKSJF.TTF")

from kivy.app import App
from kivy.uix.label import Label
class SimpleApp(App):
   def build(self):
       return Label(text='迷明小栈：www.mtools.club')
if __name__ == '__main__':

   SimpleApp().run()
