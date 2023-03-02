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
            check=True,
            column_data=[
                ("Dish", 50),
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
        Logger.info('Loading Statistics')
        db = DatabaseHandler()
        dishes = db.get_all_dish_stats()
        if dishes == "": Logger.warning('No dishes found'); return
        for dish in dishes:
            self.data_table.row_data.append(
                (dish.dish.name, str(dish.likes), str(dish.dislikes), str(dish.neutrals)))
        db.close()
        Logger.info('Statistics loaded')
    
    def reset_selected_statistics(self):
        Logger.info('Resetting selected statistics') 
        self.checked_rows = self.data_table.get_row_checks()
        if self.checked_rows is None: Logger.warn("Statistics: No Selected Entry"); return
        db = DatabaseHandler()
        for row in self.checked_rows:
            dish_id = db.get_dish_id(row[0])
            if dish_id is None: Logger.warning(f'Wrong dish name: {row.text}'); return
            db.reset_dish_stats(dish_id)
        db.close()
        self.load()
        self.checked_rows = None


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
            check=True,
            column_data=[
                ("Title", 60),
                ("Feedback", 200),
                ("Date", 39),
                ("Status", 35),
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
        Logger.info('Loading Feedback')
        self.data_table.row_data = []
        db = DatabaseHandler()
        feedbacks = db.get_all_feedback()
        if feedbacks == "": Logger.warning('No feedbacks found'); return
        for feedback in feedbacks:
            self.data_table.row_data.append( #only show the first 20 characters of the feedback
                (feedback.feedback_title, feedback.feedback, feedback.date, feedback.read_status))
        Logger.info('Feedback: Feedback loaded')

    def open_selected_feedback(self):
        Logger.info('Feedback: Opening selected feedback')
        self.checked_rows = self.data_table.get_row_checks()
        if self.checked_rows == []: Logger.warning("Feedback: No Selected Entry"); self.ids.error_label_feedback.text = "Select at least one feedback"; self.ids.error_label_feedback.color = (1, 0, 0, 1); return
        elif len(self.checked_rows) > 1: Logger.warning("Feedback: Multiple Selected Entries"); self.ids.error_label_feedback.text = "Select only one feedback"; self.ids.error_label_feedback.color = (1, 0, 0, 1); return
        else: self.ids.error_label_feedback.text = "Feedback"; self.ids.error_label_feedback.color = (1, 1, 1, 1)

    def make_selected_feedback_read(self):
        Logger.info('Feedback: Marking selected feedback as read')
        self.checked_rows = self.data_table.get_row_checks()
        if self.checked_rows == []: Logger.warning("Feedback: No Selected Entry"); return
        db = DatabaseHandler()
        for row in self.checked_rows:
            feedback_id = db.get_feedback_id(row[0])
            if feedback_id is None: Logger.warning(f'Wrong feedback title: {row.text}'); return
            db.mark_feedback_as_read(feedback_id)
        db.close()
        self.load()
        self.checked_rows = None

    def delete_selected_feedback(self):
        Logger.info('Deleting selected feedback')
        self.checked_rows = self.data_table.get_row_checks()
        if self.checked_rows == []: Logger.warning("Feedback: No Selected Entry"); return
        db = DatabaseHandler()
        for row in self.checked_rows:
            feedback_id = db.get_feedback_id(row[0])
            if feedback_id is None: Logger.warning(f'Feedback: Wrong feedback title: {row.text}'); return
            db.delete_feedback(feedback_id)
        db.close()
        self.load()
        self.checked_rows = None

class Feedback_consultation_screen(MDScreen):
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

    def submit_feedback(self, title, dish, description):
        if dish == '': Logger.warning('No dish selected'); dish = 'None';

        Logger.info('submit_feedback: ' + title +' | ' + dish + ' | ' + description)

        db = DatabaseHandler()
        db.add_feedback(str(title), db.get_dish_id(dish), str(description))
        db.close()

        self.ids.feedback_title.text = ''
        self.ids.dish_name.text = ''
        self.ids.description.text = ''

class layout(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        return


if __name__ == '__main__':
    db = DatabaseHandler()
    layout().run()
