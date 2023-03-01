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
    def enter(self, code):
        #check if the code entered is correct
        if code == '1234':
            self.manager.current = 'config_screen'
            self.ids.error_label.text = ''
        else:
            Logger.warning(f'Authentication: Wrong code entered: {code}')
            self.ids.error_label.text = 'Wrong code'
            self.ids.code.helper_text_mode = "on_error"
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
            db.close()
        
    def submit_feedback(self):
        try:
            title = self.ids.feedback_title.text
        except:
            Logger.warning('No title')
            return
        dish = self.ids.dish.text
        description = self.ids.description.text

        Logger.info('submit_feedback: ' + title + ' ' + dish + ' ' + description)
        pass
                
                


    pass

class layout(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        return

if __name__ == '__main__':
    db = DatabaseHandler()
    layout().run()
