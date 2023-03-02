from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.logger import Logger
from database_handler import DatabaseHandler
from kivymd.uix.datatables import MDDataTable
from kivy.uix.button import Button



class Main_screen(MDScreen):
    def open_config(self):
        self.manager.current = 'login_screen'
    def dish_vote(self, Dish_name, vote):
        db = DatabaseHandler()
        dish_id = db.get_dish_id(Dish_name)
        if dish_id is None: Logger.warning(f'Wrong dish name: {Dish_name}'); return

        STATS_LOOKUP = {
            -1: (0, 1, 0),
            0: (0, 0, 1),
            1: (1, 0, 0)
        }

        if vote in STATS_LOOKUP:
            db.change_dish_stats(dish_id, *STATS_LOOKUP[vote])
        else:
            Logger.warning(f'Wrong vote value: {vote}')
        db.close()



class Login_screen(MDScreen):
    def enter(self, code):
        # check if the code entered is correct
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


class Statistics_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checked_rows = None
        self.data_table = None

    def on_pre_enter(self, *args):

        self.data_table = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            background_color=(1, 1, 1, 0.3),
            background_color_cell=(1, 1, 1, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data=[
                ("Dish", .2),
                ("Likes", 40),
                ("Dislikes", 30),
                ("Neutrals", 30),
            ],
            row_data=[]
        )
        self.data_table.bind(on_row_press=self.on_row_press)
        self.data_table.bind(on_check_press=self.on_check_press)
        self.add_widget(self.data_table)
        self.load()

    @staticmethod
    def on_row_press(table, row):
        print(f"Row was pressed. Data is: {row.text}")

    @staticmethod
    def on_check_press(table, current_row):
        print(f"Row {current_row} was checked")

    def load(self):
        Logger.info('Loading Statistics')
        db = DatabaseHandler()
        dishes = db.get_all_dish_stats()
        if dishes == "": Logger.warning('No dishes found'); return
        for dish in dishes:
            self.data_table.row_data.append(
                (dish.dish.name, str(dish.likes), str(dish.dislikes), str(dish.neutrals)))
        db.close()
        Logger.info('Statistics loaded')

class Feedback_view_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checked_rows = None
        self.data_table = None

    def on_pre_enter(self, *args):

        self.data_table = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            background_color=(1, 1, 1, 0.3),
            background_color_cell=(1, 1, 1, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data=[
                ("Dish", 30),
                ("Likes", 30),
                ("Dislikes", 30),
                ("Neutrals", 30),
            ],
            row_data=[]
        )
        self.data_table.bind(on_row_press=self.on_row_press)
        self.data_table.bind(on_check_press=self.on_check_press)
        self.add_widget(self.data_table)
        self.load()

    @staticmethod
    def on_row_press(table, row):
        print(f"Row was pressed. Data is: {row.text}")

    @staticmethod
    def on_check_press(table, current_row):
        print(f"Row {current_row} was checked")

    def load(self):
        pass



class Feedback_screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #define the parent id: dish_suggestion
        #self.ids.dish_suggestion.clear_widgets()

    # there is a text field called dishes, when something is typed we will used the database handler to search for dishes that match the input and display them in a list
    def search_dish(self, dishes):
        self.ids.dish_suggestion.clear_widgets()
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
                #there is a BDBoxLayout called dish_suggestion, we will add the dishes to it in form of buttons
                self.ids.dish_suggestion.add_widget(
                    Button(text=dish.name, on_release=self.set_dish))
            db.close()

    def set_dish(self, instance):
        self.ids.dish_name.text = instance.text
        self.ids.dish_suggestion.clear_widgets()

    def submit_feedback(self):
        try:
            title = self.ids.feedback_title.text
        except:
            Logger.warning('No title')
            return
        dish = self.ids.dish.text
        description = self.ids.description.text

        Logger.info('submit_feedback: ' + title +
                    ' ' + dish + ' ' + description)
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
