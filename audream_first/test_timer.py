from tkinter import Tk, Label, Button
timer_running = False  # запущен ли таймер
default_seconds = 120  # изначальное положение(2 мин 00 сек)
timer_seconds = default_seconds  # текущее положение таймера, сек

def timer_start_pause():
    global timer_running
    timer_running = not timer_running  # работа или пауза
    if timer_running:  # работа
        timer_tick()

def timer_reset():
    global timer_running, timer_seconds
    timer_running = False  # стоп
    timer_seconds = default_seconds  # изначальное положение
    show_timer()

def timer_tick():
    global timer_seconds
    if timer_running and timer_seconds:
        label.after(1000, timer_tick)  # перезапустить через 1 сек
        # уменьшить таймер
        timer_seconds -= 1
        show_timer()

def show_timer():
    '''отобразить таймер'''
    m = timer_seconds // 60
    s = timer_seconds - m * 60
    label['text'] = '%02d:%02d' % (m, s)

root = Tk()
label = Label(root, font='Monospace 30')
label.pack()
Button(root, text='start/pause', command=timer_start_pause).pack()  # запуск/пауза отсчета
Button(root, text='reset', command=timer_reset).pack()  # сброс

timer_reset()
root.mainloop()