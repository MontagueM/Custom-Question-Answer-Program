from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
import os
from colorama import Fore, Style
import glob

image_number = 0
showing_question = True
ans_type = []
ans = []
images_to_show_mu = []
images_to_show_me = []
images_to_show = []
incorrect_array = []
size = [1000, 1000]
size_ans = [500, 500]

root = Tk()
root.geometry("1920x1080")
topframe = ttk.Frame(root)
topframe.pack(side="top")
mainframe = ttk.Frame(root)
mainframe.pack(pady=50)
bottomframe = ttk.Frame(root)
bottomframe.pack(side="bottom")

q_num = Label(topframe, image=None, text="Q1", font=("Segoe UI", 64))
q_num.pack(side="bottom", expand="yes")

panel = Label(mainframe, image=None, text=None, font=("Segoe UI", 72))
panel.pack(side="bottom", fill="both", expand="yes")  # Keeps the image in the centre

wrong_qs = Label(bottomframe, image=None, text="Wrong Qs:", font=("Segoe UI", 64))
wrong_qs.pack(side="top", expand="yes", pady=50)


def prev_image(*args):
    global img
    global image_number
    global showing_question
    if image_number > 0:
        image_number -= 1
        img = Image.open(images_to_show[image_number])
        img.thumbnail(size, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        showing_question = True
        q_num.configure(text="Q" + str(image_number+1))


def next_image(*args):
    global img
    global image_number
    global showing_question
    if image_number < len(images_to_show) - 1:
        image_number += 1
        img = Image.open(images_to_show[image_number])
        img.thumbnail(size, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        showing_question = True
        q_num.configure(text="Q" + str(image_number+1))


def show_hide_answer(*args):
    # print("Running")
    global img
    global image_number
    global showing_question
    if showing_question:
        showing_question = False
        if ans_type[image_number] == "text":
            panel.configure(image="")
            panel.configure(text=ans[image_number])
        else:
            img = Image.open(ans[image_number])
            img.thumbnail(size_ans, Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel.configure(image=img)
    else:
        showing_question = True
        panel.configure(text="")
        img = Image.open(images_to_show[image_number])
        img.thumbnail(size, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
    # print(showing_question)


def got_wrong(*args):
    global incorrect_array
    print_str = ""
    incorrect_array[image_number] = True
    for a, i in enumerate(incorrect_array, start=1):
        if i:
            print_str += " " + str(a)
    final_str = "Wrong Qs:" + print_str
    # print(final_str)
    wrong_qs.configure(text=final_str)


def open_image(*args):
    global showing_question
    if showing_question:
        img1 = Image.open(images_to_show[image_number])
        img1.show()
    else:
        img1 = Image.open(ans[image_number])
        img1.show()


prev_button = ttk.Button(mainframe, text="< Previous", command=prev_image)
prev_button.pack(side="left")
next_button = ttk.Button(mainframe, text="Next >", command=next_image)
next_button.pack(side="right")
answer_button = ttk.Button(mainframe, text="Show/Hide answer", command=show_hide_answer)
answer_button.pack(side="bottom")
wrong_button = ttk.Button(mainframe, text="Got it wrong", command=got_wrong)
wrong_button.pack(side="bottom")
show_image_if_small_button = ttk.Button(mainframe, text="Click to open image if too small", command=open_image)
show_image_if_small_button.pack(side="bottom")


def main(subject, questions_desired, skip):
    global img
    global images_to_show
    global ans
    global ans_type
    global incorrect_array
    # print(questions_desired)
    if skip:
        sub_to_look = "fp1"
        topic_to_look = "calculus_methods, conic, inequalities, numerical_methods, reducible_de, t-formulae, taylor, vectors"
        number_of_q = 999
    else:
        sub_to_look = input("\nWhich sub-subject? Type l for list: ").lower()
        if sub_to_look == "l":
            print(f"{Fore.GREEN}" + ", ".join(os.listdir(subject)) + f"{Style.RESET_ALL}")
            sub_to_look = input("\nWhich sub-subject? (e.g. macro, stats): ").lower()
        if os.path.isdir(subject + "/" + sub_to_look) is False:
            print("This sub-subject does not exist. Quitting.")
            quit()

        topic_to_look = input("\nWhich topic? (', ' separator) Type l for list: ").lower()
        if topic_to_look == "l":
            print(f"{Fore.GREEN}" + ", ".join(os.listdir(subject + "/" + sub_to_look)) + f"{Style.RESET_ALL}")
            topic_to_look = input("\nWhich topic? (e.g. macro, stats): ").lower()
        if os.path.isdir(subject + "/" + sub_to_look + "/" + topic_to_look) is False:
            print("This topic does not exist. Quitting.")
            quit()
        number_of_q = int(input("\nHow many questions? "))

    if questions_desired.get("multiple"):
        for topic in topic_to_look.split(", "):
            for file in glob.glob(subject + "/" + sub_to_look + "/" + topic + "/multiple/*.png"):
                string = file.split(".")[0].split("\\")[1]
                images_to_show_mu.append(subject + "/" + sub_to_look + "/" + topic + "/multiple/" + string + ".png")
            f = open(subject + "/" + sub_to_look + "/" + topic + "/multiple/ans.txt", 'r')
            for i in f.readlines():
                ans_type.append("text")
                ans.append(i)

    if questions_desired.get("medium"):
        for topic in topic_to_look.split(", "):
            for file in glob.glob(subject + "/" + sub_to_look + "/" + topic + "/medium/*.png"):
                string = file.split(".")[0].split("\\")[1]
                if string.isdigit():
                    images_to_show_me.append(subject + "/" + sub_to_look + "/" + topic + "/medium/" + string + ".png")
            for i in range(len(images_to_show_me)):
                ans_type.append("image")
                ans.append(subject + "/" + sub_to_look + "/" + topic + "/medium/" + str(i) + "_ans.png")

    elif questions_desired.get("maths"):
        for topic in topic_to_look.split(", "):  # For every subject listed (eg maths or maths and futher maths)
            print(topic)
            for file in glob.glob(subject + "/" + sub_to_look + "/" + topic + "/*.png"):  # Produce list of all pngs
                string = file.split(".")[0].split("\\")[1]  # Getting file name without .png
                if "ans" not in string:  # if string only has a digit and no _ans
                    print(string)
                    images_to_show.append(file)  # append to show images
                else:  # if an _ans:
                    ans_type.append("image")  # add the image to answers
                    print(string)
                    ans.append(subject + "/" + sub_to_look + "/" + topic + "/" + string + ".png")

    # print(ans)
    if questions_desired.get("maths") is False:
        images_to_show = images_to_show_mu + images_to_show_me

    # System that shuffles all three the same way
    # print(images_to_show)
    # print(ans)
    # print(ans_type)
    c = list(zip(images_to_show, ans, ans_type))
    # random.shuffle(c)
    images_to_show, ans, ans_type = zip(*c)
    images_to_show, ans, ans_type = images_to_show[:number_of_q], ans[:number_of_q], ans_type[:number_of_q]
    img = Image.open(images_to_show[image_number])
    img.thumbnail(size, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    incorrect_array = [False] * len(images_to_show)
    panel.configure(image=img)
    root.lift()
    root.bind('<Left>', prev_image)
    root.bind('<Right>', next_image)
    root.bind('<Up>', show_hide_answer)
    root.bind('<Down>', show_hide_answer)
    root.mainloop()


if __name__ == "__main__":
    print("Cannot run from itself.")
