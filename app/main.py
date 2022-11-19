from tkinter import *
from tkinter import messagebox
from idlelib.tooltip import Hovertip
from tensorflow import keras
import pickle


window = Tk()
FONT = "Arial 12 bold"
DEF_FLOAT_VAL = "0.00"
LABEL_PADX = (0, 1)
VALUE_PADX = (0, 1)
VALUE_WIDTH = 15

window.geometry("300x200")

columns = {0: ("IW", "величина сварочного тока"),
           1: ("IF", "ток фокусировки электронного пучка"),
           2: ("VW", "скорость сварки"),
           3: ("FP", "расстояние от поверхности образцов до электронно-оптической системы"),
           4: ("Depth", "глубина шва"),
           5: ("Width", "ширина шва"),
           }

values = {}
labels = {}
tips = {}

def get_fileame(name):
    return "models/{}.sav".format(name)

def add_elements():
    for key in columns.keys():
        index = key
        label_name = columns[index][0] + ":"
        labels[index] = Label(window, text=label_name, font=FONT, anchor='w')  # bold
        labels[index].grid(row=index, column=0, padx=LABEL_PADX, sticky="W")
        tips[index] = Hovertip(labels[index], columns[index][1])

        values[index] = Entry(window, width=VALUE_WIDTH)
        values[index].focus_set()
        values[index].insert(0, DEF_FLOAT_VAL)
        values[index].grid(row=index, column=1, padx=VALUE_PADX)

def retrieve_input():
    fl_IW = float(values[0].get())
    fl_IF = float(values[1].get())
    fl_VW = float(values[2].get())
    fl_FP = float(values[3].get())

    # Импорт нейронки падает на либах
    # Классический способ решения подобных проблем - забить и использовать можель sklearn
    loaded_model = keras.models.load_model('nn_model')
    # loaded_model = pickle.load(open(get_fileame("AdaBoostRegressor"), 'rb'))

    prediction = loaded_model.predict([[fl_IW, fl_IF, fl_VW, fl_FP]])

    val = prediction[0]
    depth = val[0]
    width = val[1]
    values[4].delete(0, 10)
    values[4].insert(0, str(round(depth, 5)))
    values[5].delete(0, 10)
    values[5].insert(0, str(round(width, 9)))
    message = f"Depth:{depth} Width: {width}"
    print(type(prediction))
    messagebox.showinfo(title="Prediction", message=message)


def main():
    add_elements()

    ok_btn = Button(window,
                    text="Predict",
                    width=20,
                    command=retrieve_input)

    ok_btn.grid(row=6, column=0, padx=(20, 20))


if __name__ == '__main__':
    main()
    window.mainloop()

