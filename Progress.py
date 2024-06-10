from PyQt5 import QtCore, QtWidgets, QtGui, uic
import sys
import random

import Neyroset


class Progress_Neyro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("int_prog.ui")
        self.ui.show()
        self.set3()

    def set3(self):
        #Экземпляр потока и его обработчик
        # - виндовс рамки и обработчик кнопки
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def stop_training(self):
        self.brain_instance.stop_training_flag = True
        self.ui.progressBar.reset()
        self.ui.label_2.setText("Обучение остановлено")
        self.ui.close()

    def signal_zombie(self, value):
        fake_data = [
            "Обучение может занимать до нескольких минут,\r\n в зависимости от данных",
            "Чем больше данных MNIST используется,\r\n тем выше вероятность,\r\n  что ИНС распазнает ваше изображение",
            "Результаты обучения можно сохранить в любой txt файл",
            "Если эпох нет - нет и обучения, только рандомайзер",
            "Опрос сети значит, что обученную сеть тестируют на \r\n обучающей выборки, данных MNIST",
            "Переобучение происходит,\r\n когда примеры из обучающей выборки \r\nочень хорошо распознаются, а остальные нет",
            "Помните, выбор конкретной функции активации\r\n может зависеть от конкретной архитектуры сети или\r\n характеристик входных данных"

        ]

        if value[1] > 100:
            current_value = self.ui.progressBar.value()
            self.ui.progressBar.setValue(current_value + 1)
            self.ui.label_2.setText("Нейросеть обученка")
            return

        if value[1] == 100:
            #current_value = self.ui.progressBar.value()
            #self.ui.progressBar.setValue(current_value + 1)
            self.ui.label_2.setText("Выполняется опрос сети")
            return

        if value[0] == "progress_increment":
            current_value = self.ui.progressBar.value()
            self.ui.progressBar.setValue(current_value + 1)

        if value[1] % 20 == 0:
            random_data = random.choice(fake_data)
            self.ui.label_2.setText(random_data)


if __name__ =="__main__":
    app = QtWidgets.QApplication(sys.argv)
    brain_instance = Neyroset.brain()
    win = Progress_Neyro()
    sys.exit(app.exec_())