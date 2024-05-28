import re
import sys

from typing import Union
from main import predict_blood_sugar

# noinspection PyUnresolvedReferences
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox


class Validator:
    re_float = '^-?[0-9]+(\\.[0-9]+)?$'

    @staticmethod
    def validate_value_in_range(data: Union[int, float], low: Union[int, float],
                                high: Union[int, float]) -> tuple[bool, str]:
        msg = ""
        if not (low or high) and low != 0 and high != 0:
            return True, msg  # Return always True if borders not specified

        low, high = (low, high) if low and high else (0, low if low else high)
        if low > high:
            msg = f"Lower boundaries grated than higher boundaries (LOW={low} > HIGH={high})"
            return False, msg

        result = low <= data <= high
        if not result:
            msg = f"Value should be in range:  {low} - {high}"
        return result, msg

    @staticmethod
    def validate_float(data: str) -> tuple[bool, str]:
        msg = ""
        result = bool(re.match(Validator.re_float, data))
        if not result:
            msg = f"Wrong data type. Should be float. Try again!"
        return result, msg


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('design.ui', self)  # Load the .ui file
        self.signal_logic()

    @staticmethod
    def show_validation_error(error_text: str = "Error text"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText("Validation error!")
        msg.setInformativeText(error_text)
        msg.exec_()

    # noinspection PyUnresolvedReferences
    def get_age_value(self) -> Union[float, None]:
        org_style = ""
        err_style = "border: 1px solid red;"

        raw_data = self.age_input.text()
        valid_flag, message = Validator.validate_float(raw_data)
        if not valid_flag:
            self.age_input.setStyleSheet(err_style)
            self.show_validation_error(error_text=message)
            return None

        data = float(raw_data)
        valid_flag, message = Validator.validate_value_in_range(data=data, low=0, high=100)
        if not valid_flag:
            self.age_input.setStyleSheet(err_style)
            self.show_validation_error(error_text=message)
            return None

        self.age_input.setStyleSheet(org_style)
        return data

    # noinspection PyUnresolvedReferences
    def get_bmi_value(self) -> Union[float, None]:
        org_style = ""
        err_style = "border: 1px solid red;"

        raw_data = self.bmi_input.text()
        valid_flag, message = Validator.validate_float(raw_data)
        if not valid_flag:
            self.bmi_input.setStyleSheet(err_style)
            self.show_validation_error(error_text=message)
            return None

        data = float(raw_data)
        valid_flag, message = Validator.validate_value_in_range(data=data, low=10, high=45)
        if not valid_flag:
            self.bmi_input.setStyleSheet(err_style)
            self.show_validation_error(error_text=message)
            return None

        self.bmi_input.setStyleSheet(org_style)
        return data

    # noinspection PyUnresolvedReferences
    def get_activity_value(self) -> Union[float, None]:
        org_style = ""
        err_style = "border: 1px solid red;"

        raw_data = self.activity_input.text()
        valid_flag, message = Validator.validate_float(raw_data)
        if not valid_flag:
            self.activity_input.setStyleSheet(err_style)
            self.show_validation_error(error_text=message)
            return None

        data = float(raw_data)
        valid_flag, message = Validator.validate_value_in_range(data=data, low=0, high=10)
        if not valid_flag:
            self.activity_input.setStyleSheet(err_style)
            self.show_validation_error(error_text=message)
            return None

        self.activity_input.setStyleSheet(org_style)
        return data

    # noinspection PyUnresolvedReferences
    def calculate_blood_sugar(self):
        age = self.get_age_value()
        if age is None:
            return None

        bmi = self.get_bmi_value()
        if bmi is None:
            return None

        activity = self.get_activity_value()
        if activity is None:
            return None

        blood_sugar = predict_blood_sugar(
            age_input=age,
            bmi_input=bmi,
            activity_input=activity
        )
        self.blood_sugar_output.setText(f"{round(blood_sugar, 3)}")

    # noinspection PyUnresolvedReferences
    def signal_logic(self):
        self.calculate_button.released.connect(self.calculate_blood_sugar)


class Interface:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = Window()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())


def main():
    ui = Interface()
    ui.run()


if __name__ == '__main__':
    main()
