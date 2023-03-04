from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.logger import Logger
from database_handler import DatabaseHandler
from kivymd.uix.datatables import MDDataTable
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivymd.icon_definitions import md_icons
import time

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
        else: self.ids.error_label_feedback.text = "Feedback"; self.ids.error_label_feedback.color = (1, 1, 1, 1); self.manager.current = 'feedback_consultation_screen'; 
        #send the feedback title to the feedback_consultation_screen
        print(self.checked_rows)
        self.manager.get_screen('feedback_consultation_screen').ids.feedback_consultation_title.text = self.checked_rows[0][0]
        self.checked_rows = None
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
    def on_enter(self, *args):
        feedback_title = self.ids.feedback_consultation_title.text
        Logger.info(f'Feedback: Opening feedback: {feedback_title}')
        db = DatabaseHandler()
        feedback = db.get_feedback_id(feedback_title)
        feedback = db.get_feedback_by_id(feedback)
        Logger.info(f'Feedback: {feedback}, {feedback.feedback_title}, {feedback.feedback}, {feedback.date}, {feedback.dish.name}')
        if feedback == []: Logger.warning('Feedback: No feedback found'); return
        dish = feedback.dish.name
        print(dish)
        self.ids.feedback_consultation_title.text = feedback.feedback_title
        self.ids.feedback_consultation_date.text = feedback.date
        self.ids.feedback_consultation_selected_dishes = str(dish)
        self.ids.feedback_consultation_description.text = feedback.feedback
        db.close()

    def delete_feedback(self):
        Logger.info('Feedback: Deleting feedback')
        feedback_title = self.ids.feedback_consultation_title.text
        db = DatabaseHandler()
        feedback_id = db.get_feedback_id(feedback_title)
        if feedback_id is None: Logger.warning(f'Feedback: Wrong feedback title: {feedback_title}'); return
        db.delete_feedback(feedback_id)
        db.close()
        self.manager.current = 'feedback_view_screen'
        self.manager.get_screen('feedback_view_screen').load()

    def mark_as_read(self):
        Logger.info('Feedback: Marking feedback as read')
        feedback_title = self.ids.feedback_consultation_title.text
        db = DatabaseHandler()
        feedback_id = db.get_feedback_id(feedback_title)
        if feedback_id is None: Logger.warning(f'Feedback: Wrong feedback title: {feedback_title}'); return
        db.mark_feedback_as_read(feedback_id)
        db.close()
        self.manager.current = 'feedback_view_screen'
        self.manager.get_screen('feedback_view_screen').load()

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
        message = f'{title} added successfully'
        if dish == '': Logger.warning('No dish selected'); dish = 'None';

        Logger.info('submit_feedback: ' + title +' | ' + dish + ' | ' + description)

        try:
            db = DatabaseHandler()
            db.add_feedback(str(title), db.get_dish_id(dish), str(description))
            db.close()
        except Exception as e:
            Logger.error(f'Error: {e}')
            message = f'Error: {e}'

        self.ids.feedback_title.text = ''
        self.ids.dish_name.text = ''
        self.ids.description.text = ''

        #content = Label + Button
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        button = Button(text="Back to main screen")
        button.bind(on_release=lambda *args: self.close_popup(popup))
        content.add_widget(button)
        popup = Popup(title='Feedback', content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

    def close_popup(self, popup):
        popup.dismiss()
        self.manager.current = 'main_screen'





class layout(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
        return


if __name__ == '__main__':
    db = DatabaseHandler()
    layout().run()
