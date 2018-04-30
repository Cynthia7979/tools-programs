import Tkinter
import os
import shutil
from os.path import join


def main():
    window, path_entry = window_pack()
    window.mainloop()
    #path = get_path(path_entry)
    #d, others = generate_paths(path)
    #file_scanner(path, d, others)


def window_pack():
    root = Tkinter.Tk()

    caution_label = Tkinter.Label(root, text='Warning: This program will move every file in the folder')
    check_label = Tkinter.Label(root)
    enter_path_label = Tkinter.Label(root, text='Please enter your file path:')
    enter_path_entry = Tkinter.Entry(root)
    enter_path_button = Tkinter.Button(root, text='Confirm', command=lambda: check_path(enter_path_entry, check_label))

    enter_path_label.pack()
    enter_path_entry.pack()
    enter_path_button.pack()
    caution_label.pack()
    check_label.pack()

    return root, enter_path_entry


def check_path(path_entry, check_label):
    path = path_entry.get()
    if os.path.exists(path):
        check_label.config(text='This path is available, please wait...')
        d, others = generate_paths(path)
        file_scanner(path, d, others)
        check_label.config(text='Finished! You can close this window now')
    else:
        check_label.config(text='This path is unavailable!')
        path_entry.delete(0, Tkinter.END)
        #print 'unavailable'


def get_path(path_entry):
    return path_entry.get()


def generate_paths(root_path):
    d = {}
    categories = ('musics', 'images', 'videos', 'documents', 'executions')
    suffixes = [['mp3', 'wav', 'wma', 'flac', 'ape'],
                ['jpg', 'jpeg', 'png', 'bmp', 'gif'],
                ['avi', 'wmv', 'mp4', 'flv'],
                ['doc', 'docx', 'txt', 'ppt', 'pptx', 'pdf', 'zip', 'rar', '7z'],
                ['exe', 'bat', 'py']]
    for index in range(len(categories)):
        new_path = join(root_path, categories[index] + '/')
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        for suffix in suffixes[index]:
            d[suffix] = new_path
    others = join(root_path, 'others/')
    if not os.path.exists(others):
        os.makedirs(others)
    return d, others


def file_scanner(root_dir, d, others):
    for path,folders,files in os.walk(root_dir):
        for this_file in files:
            suffix = this_file[this_file.find('.') + 1:]
            this_path = join(path, this_file)
            print suffix
            if suffix in d.keys():
                shutil.move(this_path, join(d[suffix], this_file))
                #print 'moved!'
            else:
                shutil.move(this_path, join(others, this_file))
                #print 'moved others!'

if __name__ == '__main__':
    main()
