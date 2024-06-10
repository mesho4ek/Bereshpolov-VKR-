# Модули
import numpy
# scipy.для сигмоидальной функции expit()
import scipy.special
# помощник для загрузки данных из файлов изображений в формате PNG
from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui, uic
import scipy.misc
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import glob
import sys
import numpy
import time
import random
import os
import csv

# Реализация Leaky ReLU
def leaky_relu(x, alpha=0.01):
    return numpy.where(x > 0, x, alpha*x)

class intell:
    # методы
    # Инициализация
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate, fun_activ):
        # Задаем кол-во узлов:
        self.inodes = inputnodes  # во входном
        self.hnodes = hiddennodes  # в скрытом
        self.onodes = outputnodes  # в выходном слое
        self.fun_activation = fun_activ
        print("Обучение началось")

        # Матрицы весовых коэф. связей, где wih - матрица весов между входным и скрытым слоями,
        # матрица весов между скрытым и выходными слоями
        self.wih = numpy.random.rand(self.hnodes, self.inodes) - 0.5
        self.who = numpy.random.rand(self.onodes, self.hnodes) - 0.5

        # коэффициент обучения
        self.lr = learningrate
        # Быстрое создание функции лямбда-выражение.

        if self.fun_activation == 0:
            # Использование сигмоиды в качестве функции активации
            self.activation_function = lambda x: scipy.special.expit(x)
            #logistic activation function - один из видов сигмоиды
            #self.activation_function = lambda x: 1 / (1 + numpy.exp(-x))

        elif self.fun_activation == 1:
            # Гиперболический тангенс (tanh) в качестве функции активации
            self.activation_function = lambda x: (2 / (1 + numpy.exp(-x))) - 1
        elif self.fun_activation == 2:
            # ReLU (Rectified Linear Unit) в качестве функции активации
            self.activation_function = lambda x: numpy.maximum(0, x)
        elif self.fun_activation == 3:
            # Leaky ReLU в качестве функции активации
            self.activation_function = lambda x: leaky_relu(x)  # Используем Leaky ReLU
        elif self.fun_activation == 4:
            #  Softmax в качестве функции активации
            self.activation_function = lambda x: numpy.exp(x) / numpy.sum(numpy.exp(x), axis=0)
        elif self.fun_activation == 5:
            #Swish в качестве функции активации
            self.activation_function = lambda x: x * (1 + numpy.exp(-x))
        #Обратная ФА
        self.inverse_activation_function = lambda x: scipy.special.logit(x)
        pass

    # Тренировка
    def train(self, inputs_list, targets_list):
        # Преобразует список входных значений в 2-мерный массив
        inputs = numpy.array(inputs_list, ndmin=2).T
        # Преобразует массив также как и "inputs"
        targets = numpy.array(targets_list, ndmin=2).T

        # вычисление сигналов в скрытом слое
        hidden_inputs = numpy.dot(self.wih, inputs)

        # вычисление сигналов, исходящих от скрытого слоя
        hidden_outputs = self.activation_function(hidden_inputs)

        # вычисление сигналов в конечном выходном слое
        final_inputs = numpy.dot(self.who, hidden_outputs)

        # вычисление сигналов, поступающих из конечного выходного слоя
        final_outputs = self.activation_function(final_inputs)

        # Ошибка = целевое значение - фактическое
        output_errors = targets - final_outputs
        # Распределение пропорционально весовым коэффициентам связей
        hidden_errors = numpy.dot(self.who.T, output_errors)
        # Обновить весовые коэффициенты для связей между скрытым и выходными слоями
        self.who += self.lr * numpy.dot((output_errors * final_outputs *
                                         (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        # Обновить весовые коэффициенты для связей между входным и скрытым слоями
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs *
                                         (1.0 - hidden_outputs)), numpy.transpose(inputs))
        #print("Тренировка окончена")
        pass

    # опрос нейронной сети
    def query(self, inputs_list):
        # преобразовать список входных значений
        # в двумерный массив
        inputs = numpy.array(inputs_list, ndmin=2).T

        # Рассчитать входящие сигналы для входящего слоя
        hidden_inputs = numpy.dot(self.wih, inputs)
        # Рассчитать выходящие сигналы для скрытого слоя
        hidden_outputs = self.activation_function(hidden_inputs)

        # Рассчитать входящие сигналы для выходного слоя
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # Рассчитать исходящие сигналы для выходного слоя
        final_outputs = self.activation_function(final_inputs)
        #print("Опрос завершен")
        return final_outputs

    def save_hidden_activations(self):
        hidden_activations_dir = os.path.join("data", f"hidden_activations")
        os.makedirs(hidden_activations_dir, exist_ok=True)
        for i, neuron in enumerate(self.wih.T):
            filepath = os.path.join(hidden_activations_dir, f"hidden_neuron_{i}.csv")
            with open(filepath, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(neuron)

    # обратные запросы к нейронной сети
    # мы будем использовать одну и ту же терминологию для каждого элемента,
    # например, target - это значения справа от сети, хотя и используемые в качестве входных данных
    # например, hidden_output - это сигнал справа от средних узлов
    def backquery(self, targets_list):
        #print('Это таргет лист', targets_list)
        # перенести список целей в вертикальный массив
        final_outputs = numpy.array(targets_list, ndmin=2).T
        #print(final_outputs)
        # вычислить сигнал для конечного выходного слоя
        final_inputs = self.inverse_activation_function(final_outputs)
        #print(final_inputs)
        # вычислить сигнал из скрытого слоя
        hidden_outputs = numpy.dot(self.who.T, final_inputs)
        #print('После вычислить сигнал из скрытого слоя', self.who.T)
        # уменьшите их до 0,01 - .99
        hidden_outputs -= numpy.min(hidden_outputs)
        hidden_outputs /= numpy.max(hidden_outputs)
        hidden_outputs *= 0.98
        hidden_outputs += 0.01

        # вычислить сигнал для скрытого слоя
        hidden_inputs = self.inverse_activation_function(hidden_outputs)
        #print('Сигнал скрытого слоя:')
        #print(hidden_inputs)

        # вычислить сигнал из входного слоя
        количество_переменных = self.wih.T.size
        inputs = numpy.dot(self.wih.T, hidden_inputs)
        # уменьшите их до 0,01 - .99
        inputs -= numpy.min(inputs)
        inputs /= numpy.max(inputs)
        inputs *= 0.98
        inputs += 0.01
        #print("УГУ", inputs)
        return inputs

# Класс вычислений
class brain(QtCore.QThread):
    progressignal = QtCore.pyqtSignal(list)
    MNIST_finished = QtCore.pyqtSignal(str)
    image_finished = QtCore.pyqtSignal(str)



    def __init__(self, learning_rate=0.3, hidden_nodes=100, epochs=1, file_name="100.csv", funk_active = 0):
        super().__init__()
        self.epoch = epochs
        self.filename = file_name
        self.input_nodes = 784  # Кол-во входных узлов из-за разрешения 28х28
        self.output_nodes = 10  # Кол-во выходных узлов

        self.neyro = intell(self.input_nodes, hidden_nodes, self.output_nodes, learning_rate, funk_active)
        self.stop_training_flag = False  # Флаг для остановки процесса

        self.hidden_buttons = []
        self.output_buttons = []
        self.hidden_masks_shown = [False] * hidden_nodes  # Флаг для отслеживания визуализации масок скрытых нейронов
        self.output_masks_shown = [False] * self.output_nodes  # Флаг для отслеживания визуализации масок выходных нейронов
        self.hidden_mask_figs = [None] * hidden_nodes  # Список окон с масками скрытых нейронов
        self.output_mask_figs = [None] * self.output_nodes  # Список окон с масками выходных нейронов

    def run(self):
        # Разделяем название, делаем красиво
        #print("Прогоняем по тренировочному набору данных")
        train_list_file = (int(self.filename.split('.')[0]))
        #print(train_list_file)
        # Открываем файл
        train_data_file = open(self.filename, 'r')
        train_data_list = train_data_file.readlines()
        train_data_file.close()

        Iteration = self.epoch * train_list_file
        cho = Iteration / 100
        proccent = 0
        nu = 0
        #print(Iteration)

        # Перебираем все записи для нового тестового набора
        for e in range(self.epoch):
            for ini, record in enumerate(train_data_list):
                if self.stop_training_flag:  # Проверяем флаг остановки
                    # Действия при остановке, например, сброс прогресса и выход из цикла
                    self.progressignal.emit(["progress_reset"])  # сигнал для сброса прогресса в UI
                    return
                #print("Прогоняем по тренировочному набору данных")
                all_values = record.split(',')
                # Масштабируем БД
                inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
                # zeros -приравнивает элементы массива к 0
                targets = numpy.zeros(self.output_nodes) + 0.01
                # Целевое маркерное значение all_vaues[0]
                # т.е нужный нам элемент приравниваем к 0.99
                targets[int(all_values[0])] = 0.99
                self.neyro.train(inputs, targets)
                nu += 1
                #print(nu)
                if Iteration > 99:
                    if nu % cho == 0:
                        #print("good procent")
                        proccent += 1
                        self.progressignal.emit(["progress_increment", proccent])
                    else:
                        #print("no + procent")
                        pass
                else:
                    continue

        if Iteration < 100:
            for step in range(0, 100):
                #print("good procent")
                proccent += 1
                self.progressignal.emit(["progress_increment", proccent])

        print("Процент получается:" + str(proccent))

        MNIST_effect = self.test_MNIST() #отсутствие "()" показывает, что фунция просто присвоена, но не вызвана

        self.MNIST_finished.emit(str(MNIST_effect))
        proccent += 1
        self.progressignal.emit(["progress_increment", proccent])
        #Сохраняем
        self.neyro.save_hidden_activations()

    def test_MNIST(self):
    #Тестирование сети на MNIST
        # Открываем файл для нового тестового набора
        self.test_data_file = open(self.filename, 'r')
        self.test_data_list = self.test_data_file.readlines()
        self.test_data_file.close()

        # Наш журнал записи
        scorecard = []
        for record in self.test_data_list:
            all_values = record.split(',')
            correct_label = int(all_values[0])
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            #outputs = neyro.query(inputs)
            outputs = self.neyro.query(inputs)
            label = numpy.argmax(outputs)
            if (label == correct_label):
                scorecard.append(1)  # Верно
            else:
                scorecard.append(0)  # Неверно


        # Наш показатель
        print(scorecard)
        scorecard_array = numpy.asarray(scorecard)
        effect = scorecard_array.sum() / scorecard_array.size
        print("Эффективность = ", effect)
        self.test_all_MNIST
        return effect

    def test_all_MNIST(self):
        # Делаем для каждой цифры отдельно
        digit_scores = {digit: [0, 0] for digit in range(10)}  # {цифра: [верно, неверно]}
        for record in self.test_data_list:
            all_values = record.split(',')
            correct_label = int(all_values[0])
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            outputs = self.neyro.query(inputs)
            label = numpy.argmax(outputs)

            if label == correct_label:
                digit_scores[correct_label][0] += 1
            else:
                digit_scores[correct_label][1] += 1

        # Подсчет и вывод эффективности для каждой цифры
        for digit, scores in digit_scores.items():
            total = sum(scores)
            if total != 0:
                accuracy = scores[0] / total
            else:
                accuracy = 0.0
            print(f'Эффективность для цифры {digit}: {accuracy}')
        # Извлечение цифр и их эффективности из словаря digit_scores
        digits = list(digit_scores.keys())
        accuracies = []
        for digit in digits:
            total = sum(digit_scores[digit])
            if total == 0:
                accuracy = 0.0  # Если нет ни одного случая, устанавливаем эффективность равной 0
            else:
                accuracy = digit_scores[digit][0] / total
            accuracies.append(round(accuracy, 2))  # Округляем эффективность до сотых

        # Создание столбчатой диаграммы
        # Увеличение размера шрифта на осях и в подписях
        plt.rcParams['font.size'] = 18

        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.5
        index = range(len(digits))
        ax.bar(index, accuracies, bar_width)

        # Настройка подписей осей и заголовка
        ax.set_xlabel('Цифры')
        ax.set_ylabel('Эффективность распознавания')
        ax.set_title('Эффективность распознавания цифр из MNIST')

        # Установка меток на оси X
        ax.set_xticks(index)
        ax.set_xticklabels(digits)

        # Отображение эффективности на столбцах
        for i, accuracy in enumerate(accuracies):
            ax.text(i, accuracy + 0.01, str(accuracy), ha='center', va='bottom')

        # Отображение диаграммы
        plt.show()

    def test_own_image(self, image_files_names = 'my_own/my_image_2.jpg'):
        #Тестирование сети на собственных изображениях
        #создаем собственный набор данных для тестирования изображений
        our_own_dataset = []

        # Загружаем изображения в качестве тестового набора
        # Выполняет поиск файлов в каталоге, представленном переменной `image_files_names`, с использованием шаблона пути или имени файла.
        for image_file_name in glob.glob(image_files_names):
            print("loading ... ", image_file_name)
            label = int(image_file_name[-5:-4]) #Берем из имени картинки число


            img = Image.open(image_file_name)
            img = img.resize((28, 28))
            img_array = numpy.array(img.convert('L'))
            img_data = 255.0 - img_array.reshape(784)


            img_data = (img_data / 255.0 * 0.99) + 0.01
            print(numpy.min(img_data))
            print(numpy.max(img_data))


            record = numpy.append(label, img_data)
            our_own_dataset.append(record)




        item = 0
        # plot image
        #Преобразуем символы в числа за искл 1го с размером матрицы 28х28 для изображения
        image_array = numpy.asfarray(our_own_dataset[item][1:]).reshape((28, 28))
        #Покажем получившийся результат
        plt.imshow(image_array, cmap='Greys', interpolation='None')


        # Приблизительно правильный результат
        correct_label = our_own_dataset[item][0]
        # Вся остальная информация
        inputs = our_own_dataset[item][1:]

        outputs = self.neyro.query(inputs)
        print(outputs)


        label = numpy.argmax(outputs)
        print("Сеть сказала ", label)
        if (label == correct_label):
            print ("Умпешное попадание!")
        else:
            print ("Не угодала!")
            pass
        plt.show()
        return label

    # Пример использования для получения маски Скрытого нейрона
    def visualize_hidden_neuron(self, neuron_idx):
        # Закрываем ранее открытое окно с маской
        if self.hidden_mask_figs[neuron_idx] is not None:
            plt.close(self.hidden_mask_figs[neuron_idx])
            self.hidden_mask_figs[neuron_idx] = None

        hidden_activations_dir = os.path.join("data", f"hidden_activations")
        neuron_weights = []
        for i in range(self.neyro.wih.shape[1]):
            filepath = os.path.join(hidden_activations_dir, f"hidden_neuron_{i}.csv")
            with open(filepath, "r") as csvfile:
                reader = csv.reader(csvfile)
                weights = next(reader)
                neuron_weights.append(float(weights[neuron_idx]))

        neuron_weights = numpy.array(neuron_weights)
        neuron_weights = (neuron_weights - numpy.min(neuron_weights)) / (numpy.max(neuron_weights) - numpy.min(neuron_weights))
        neuron_weights = 0.01 + neuron_weights * 0.98
        neuron_image = neuron_weights.reshape(28, 28)
        # Закрываем все ранее открытые окна с масками

        print(f"Polushilas Скрытый: {neuron_idx}")
        if self.hidden_masks_shown[neuron_idx]:
            # Если маска уже была визуализирована, восстанавливаем исходный цвет кнопки
            self.hidden_buttons[neuron_idx].color = 'c'
            self.hidden_masks_shown[neuron_idx] = False
        else:
            # Если маска еще не была визуализирована, визуализируем ее и перекрашиваем кнопку в зеленый цвет
            self.hidden_buttons[neuron_idx].color = 'g'
            self.hidden_masks_shown[neuron_idx] = True
            hidden_mask_fig = plt.figure()
            plt.imshow(neuron_image, cmap='gray')
            plt.title(f"Маска скрытого нейрона {neuron_idx}")
            plt.show()
            self.hidden_mask_figs[neuron_idx] = hidden_mask_fig.number

        plt.draw()

    # Пример использования для получения маски выходного нейрона
    def visualize_output_neuron(self, label):
        # Закрываем ранее открытое окно с маской
        if self.output_mask_figs[label] is not None:
            plt.close(self.output_mask_figs[label])
            self.output_mask_figs[label] = None
        # создайте выходные сигналы для этой метки
        targets = numpy.zeros(self.output_nodes) + 0.01
        targets[label] = 0.99

        # получение данных изображения !(Получение выходов скрытого слоя для целевой метки)!
        hidden_outputs = self.neyro.backquery(targets)

        # Преобразуйте данные изображения в диапазон от 0 до 1
        image_data = (hidden_outputs - numpy.min(hidden_outputs)) / (numpy.max(hidden_outputs) - numpy.min(hidden_outputs))
        # Измените размерность данных изображения обратно в изображение 28x28
        image_data = image_data.reshape(28, 28)
        # Закрываем все ранее открытые окна с масками
        print(f"Polushilas выходной: {label}")

        if self.output_masks_shown[label]:
            # Если маска уже была визуализирована, восстанавливаем исходный цвет кнопки
            self.output_buttons[label].color = '#FF69B4'
            self.output_masks_shown[label] = False
        else:
            # Если маска еще не была визуализирована, визуализируем ее и перекрашиваем кнопку в зеленый цвет
            self.output_buttons[label].color = 'g'
            self.output_masks_shown[label] = True
            output_mask_fig = plt.figure()
            plt.imshow(image_data, cmap='gray')
            plt.title(f"Маска выходного нейрона {label}")
            plt.show()
            self.output_mask_figs[label] = output_mask_fig.number
        plt.draw()

    def visualize_hidden_layer(self, num_hidden_neurons, fig, ax):
        # Параметры для расположения кнопок
        rows = (num_hidden_neurons + 9) // 10  # Количество строк
        cols = 10  # Максимум 10 кнопок в строке
        button_radius = 0.03  # Радиус кнопок
        padding = 0.02  # Расстояние между кнопками

        # Создание интерактивных кнопок для скрытых нейронов
        for i in range(num_hidden_neurons):
            row = i // cols
            col = i % cols
            x = 0.1 + col * (2 * button_radius + padding)
            y = 0.9 - row * (2 * button_radius + padding)
            button_ax = plt.axes([x, y, 2 * button_radius, 2 * button_radius], projection='polar')
            button = Button(button_ax, label=str(i), color='c')
            button.label.set_fontsize(8)
            button.label.set_weight('bold')
            button.on_clicked(lambda event, neuron_idx=i: self.visualize_hidden_neuron(neuron_idx))

            self.hidden_buttons.append(button)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')


    def visualize_output_layer(self, fig, ax):
        # Параметры для расположения кнопок
        rows = 10  # 10 кнопок (по одной для каждой метке)
        cols = 1  # В одном столбце
        button_radius = 0.03  # Радиус кнопок
        padding = 0.02  # Расстояние между кнопками
        x_offset = 0.9  # Смещение по горизонтали от скрытого слоя

        # Создание интерактивных кнопок для выходных нейронов
        for label in range(10):
            row = label
            col = 0
            x = x_offset + col * (2 * button_radius + padding)
            y = 0.9 - row * (2 * button_radius + padding)
            button_ax = plt.axes([x, y, 2 * button_radius, 2 * button_radius], projection='polar')
            button = Button(button_ax, label=str(label), color='#FF69B4')
            button.label.set_fontsize(8)
            button.label.set_weight('bold')
            button.on_clicked(lambda event, label=label: self.visualize_output_neuron(label))

            self.output_buttons.append(button)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')

    def visualize_network(self, num_hidden_neurons):
        fig, ax = plt.subplots(figsize=(12, 5))

        # Визуализация скрытого слоя
        self.visualize_hidden_layer(num_hidden_neurons, fig, ax)

        # Визуализация выходного слоя
        self.visualize_output_layer(fig, ax)

        plt.show()