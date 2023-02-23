from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class Main_screen(MDScreen):
    def open_config(self):
        self.manager.current = 'login_screen'
    pass

class Login_screen(MDScreen):
    pass

class Config_screen(MDScreen):
    pass

class layout(MDApp):
    def build(self):
        return

if __name__ == '__main__':
    layout().run()
