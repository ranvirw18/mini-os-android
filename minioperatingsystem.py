import os
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform

# File path fix for Android
if platform == 'android':
    from android.storage import app_storage_path
    base_path = app_storage_path()
else:
    base_path = "."

USERNAME = "admin"
PASSWORD = "1234"

class LoginScreen(BoxLayout):
    def _init_(self, app, **kwargs):
        super()._init_(orientation='vertical', **kwargs)
        self.app = app

        self.add_widget(Label(text="Mini OS Login"))

        self.user = TextInput(hint_text="Username")
        self.add_widget(self.user)

        self.passw = TextInput(hint_text="Password", password=True)
        self.add_widget(self.passw)

        btn = Button(text="Login")
        btn.bind(on_press=self.check_login)
        self.add_widget(btn)

        self.msg = Label(text="")
        self.add_widget(self.msg)

    def check_login(self, instance):
        if self.user.text.strip() == USERNAME and self.passw.text.strip() == PASSWORD:
            self.app.root.clear_widgets()
            self.app.root.add_widget(MainScreen())
        else:
            self.msg.text = "Invalid Login"


class MainScreen(BoxLayout):
    def _init_(self, **kwargs):
        super()._init_(orientation='vertical', **kwargs)

        self.output = Label(
            text="Welcome to Mini OS\nType help",
            size_hint_y=0.6
        )
        self.add_widget(self.output)

        self.input = TextInput(
            hint_text="Enter command",
            size_hint_y=0.2
        )
        self.add_widget(self.input)

        btn = Button(text="Run Command", size_hint_y=0.2)
        btn.bind(on_press=self.execute)
        self.add_widget(btn)

    def execute(self, instance):
        cmd = self.input.text.strip()
        self.input.text = ""

        response = ""

        try:
            parts = cmd.split()

            if cmd == "help":
                response = (
                    "Commands:\n"
                    "help\n"
                    "time\n"
                    "create <file>\n"
                    "read <file>\n"
                    "delete <file>"
                )

            elif cmd == "time":
                response = time.ctime()

            elif parts and parts[0] == "create":
                file_path = os.path.join(base_path, parts[1])
                with open(file_path, "w") as f:
                    f.write("Mini OS File")
                response = "File created"

            elif parts and parts[0] == "read":
                file_path = os.path.join(base_path, parts[1])
                with open(file_path, "r") as f:
                    response = f.read()

            elif parts and parts[0] == "delete":
                file_path = os.path.join(base_path, parts[1])
                os.remove(file_path)
                response = "File deleted"

            else:
                response = "Unknown command"

        except Exception as e:
            response = "Error: " + str(e)

        self.output.text = self.output.text + "\n> " + cmd + "\n" + response


class MiniOSApp(App):
    def build(self):
        return LoginScreen(self)


if _name_ == "_main_":
    MiniOSApp().run()
