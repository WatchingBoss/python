from random import randint
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.multiplications = []

    def generate_random(self, amount: int):
        self.multiplications = [[randint(20, 90), randint(20, 90)] for _ in range(amount)]
        self.answers = [i[0] * i[1] for i in self.multiplications]
         

    def update_multiplications(self, instance):
        self.generate_random(amount=5)
        mult_strings = [' * '.join(map(str, i)) for i in self.multiplications]
        mult_string = '\n'.join(map(str, mult_strings))
        self.list_multiplications_label.text = "Multiplications: \n{0}".format(mult_string)
        self.input_box.text = ''

    def check_answers(self, instance):
        input_answers_list = [int(i) for i in self.input_box.text.split('\n')]
        result = list(map(lambda v_1, v_2: v_1 == v_2, self.answers, input_answers_list))
        self.input_box.text = '\n'.join(['{0} - {1}'.format(input_answers_list[i], result[i]) for i in range(len(input_answers_list))])

    def build(self):
        layout_app = BoxLayout(orientation='vertical')
        layout_boxes = BoxLayout(orientation='horizontal')
        layout_buttons = BoxLayout(orientation='horizontal')

        self.list_multiplications_label = Label(text='Multiplication: ')
        layout_boxes.add_widget(self.list_multiplications_label)

        self.input_box = TextInput(multiline=True)
        layout_boxes.add_widget(self.input_box)

        update_button = Button(text='Update')
        update_button.bind(on_press=self.update_multiplications)
        layout_buttons.add_widget(update_button)

        check_answers_button = Button(text='Check')
        check_answers_button.bind(on_press=self.check_answers)
        layout_buttons.add_widget(check_answers_button)

        layout_app.add_widget(layout_boxes)
        layout_app.add_widget(layout_buttons)
        return layout_app


if __name__ == "__main__":
    root = MyApp()
    root.run()