from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.logger import Logger
from database_handler import DatabaseHandler
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dropdownitem import MDDropDownItem




class Main_screen(MDScreen):
    def open_config(self):
        self.manager.current = 'login_screen'
    pass

class Login_screen(MDScreen):
    pass

class Config_screen(MDScreen):
    pass

class Feedback_screen(MDScreen):
    #there is a text field called dishes, when something is typed we will used the database handler to search for dishes that match the input and display them in a list
    def search_dish(self, dishes):
        if dishes == '':
            return
        else:
            Logger.info('search_dish: ' + dishes)
            db = DatabaseHandler()
            # used MDDroDownItem to display the dishes
            query = db.query_dishes(dishes)
            if query == "":
                Logger.warning('No dishes found')
                return
            for dish in query:
                Logger.info('Dish: ' + dish.name)
                self.ids.drop_down.add_widget(MDDropDownItem(text=dish.name))
                
                


    pass

class layout(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        return

if __name__ == '__main__':
    db = DatabaseHandler()
    layout().run()
