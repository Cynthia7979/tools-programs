import tkinter as tk
import threading
from tkinter import N, S, E, W
from random import shuffle
from time import sleep


class StoppableThread(threading.Thread):
    def __init__(self, label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stopped = False
        self.paused = False
        self.label = label
        self.sec_elapsed = 0

    def run(self):
        try:
            while True:
                if self.stopped:
                    break
                if not self.paused:
                    # self.label.configure(text=f'Time (s): {counter[0]}')
                    # counter[0] += 1
                    # print(counter)
                    counter.set(counter.get() + 1)
                else:
                    print('pausing...')
                sleep(1)
        except RuntimeError:
            self.pause()
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    @staticmethod
    def reset():
        counter.set(0)

    def stop(self):
        self.stopped = True

    def pause(self):
        self.paused = True


def main():
    global counter

    root = tk.Tk()
    counter = tk.IntVar()
    grid_width, grid_height = (4, 6)

    elapsed_time_label = tk.Label(root, text='Time (s): ')
    elapsed_time_label.grid(row=1, column=1,
                            columnspan=grid_width+1)
    elapsed_time_secs = tk.Label(root, textvariable=counter)
    elapsed_time_secs.grid(row=1, column=2,
                           columnspan=grid_width+1)

    thread = StoppableThread(elapsed_time_label)
    thread.start()

    # button_column_span = int((grid_width+3)/2) if grid_width<grid_height else int((grid_width+5)/2)
    generate_btn = tk.Button(root, text='Generate Another',
                             command=lambda: generate_numbers(grid, thread))
    generate_btn.grid(row=grid_height+2, column=1,
                      columnspan=grid_width-1)
    configure_btn = tk.Button(root, text='Configure...',
                              command=lambda: configure_window(root))
    configure_btn.grid(row=grid_height+2, column=2,
                       columnspan=grid_width-1)

    grid = generate_grid(root, grid_width, grid_height)
    generate_numbers(grid, thread, end=grid_width*grid_height)

    root.mainloop()
    root.quit()
    thread.pause()
    thread.stop()


def generate_grid(master, width=5, height=5):
    grid = []
    for i in range(height):
        row = []
        for j in range(width):
            t = tk.Label(master,
                         background='white',
                         relief='ridge',
                         width=2,
                         font=('Berlin Sans FB', 28))
            t.grid(row=i + 2, column=j + 1,
                   ipadx=27, ipady=27,
                   sticky=N + S + E + W)
            row.append(t)
        grid.append(row)
    return grid


def generate_numbers(grid, thread, start=1, end=25):
    num_sequence = list(range(start, end + 1))
    shuffle(num_sequence)
    i = 0
    for row in grid:
        for cell in row:
            try:
                cell.configure(text=num_sequence[i])
            except IndexError:
                raise IndexError('Grid # of cells doesn\'t match up with sequence start and end')
            i += 1
    thread.reset()


def configure_window(master):
    window = tk.Toplevel(master)
    width_label = tk.Label(window, text='Width: ')
    width_label.grid(row=1, column=1)
    height_label = tk.Label(window, text='Height: ')
    height_label.grid(row=2, column=1)
    width_entry = tk.Entry(window)
    width_entry.grid(row=1, column=2)
    height_entry = tk.Entry(window)
    height_entry.grid(row=2, column=2)
    confirm_btn = tk.Button(window, text='Confirm')
    confirm_btn.grid(row=3, column=1, padx=10)

    def confirm(master_):
        pass


if __name__ == '__main__':
    main()
