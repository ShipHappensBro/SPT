import os
import subprocess
from kivy.app import App #, Builder
from kivy.core.window import Window
from kivy.config import Config

# Builder.load_file("main1.kv")
# Config.set('graphics','resizable','0');
Config.set('graphics','width','640');
Config.set('graphics','height','480');

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput

class Container(BoxLayout):
    pass

class MainApp(App):
    def build(self):
        self.title="Spetstorg STP  CurrentUser: " + subprocess.run(["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"], stdout=subprocess.PIPE, text=True).stdout.strip() +"\\"+ os.getlogin()
        Window.clearcolor = (1,1,1,1)
        al = AnchorLayout()
        bl = BoxLayout(orientation='vertical', size_hint=[.5,.5])

        self.text_input=TextInput(text=os.getlogin(),multiline=False)

        bl.add_widget(self.text_input) #LOGIN
        bl.add_widget(TextInput())

        bl.add_widget(Button(
            text='Войти',
            on_press=self.btn_press
        ))

        al.add_widget(bl)
        return al
        
    def on_text(self,instance,value):
        self.on_text.text=print(self.on_text)
    
    def btn_press(self, instance):
        print(self.text_input.text)

        
if __name__ =="__main__":
    MainApp().run()
