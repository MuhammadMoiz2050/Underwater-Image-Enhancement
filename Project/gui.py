import tkinter as tk
from tkinter import filedialog, Label, messagebox,ttk
import project
from PIL import ImageTk, Image
from tqdm import tqdm
import time

file_flag = ""

def open_file():
    global file_flag
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = ( ("PNG files", "*.png"),("jpeg files","*.jpg"),("all files","*.*")))
    # print(filename) # for testing purposes only
    file_flag = filename
    print(file_flag)

    if filename:
        # open the selected image and display it
        img = Image.open(filename)
        img = img.resize((700, 600), Image.ANTIALIAS) # resize the image to fit in the tkinter window
        img = ImageTk.PhotoImage(img)
        

        no_image_label.config(text="")
        no_image_label.config(image = img)
        no_image_label.image = img

        # place the image in the center of the frame
        w, h = img.width(), img.height()
        no_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=w, height=h)
        
    else:
        print("No file selected")

def run_progress():
    # create progress bar window
    progress_window = tk.Toplevel(root)
    progress_window.geometry("300x100")
    progress_window.title("Progress Bar")

    # add label and progress bar
    progress_label = tk.Label(progress_window, text="Enhancing...")
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=10)

    # simulate progress
    progress = 0
    while progress < 100:
        progress += 20
        progress_bar['value'] = progress
        progress_window.update()
        time.sleep(0.5)

    # close progress bar window
    progress_window.destroy()


def enhance_img():
    print(file_flag)
    if file_flag!="":
        project.main(file_flag)

        img = Image.open("finaloutput.jpg")
        img = ImageTk.PhotoImage(img)

        no_image_label.config(text="")
        no_image_label.config(image = img)
        no_image_label.image = img

        # place the image in the center of the frame
        w, h = img.width(), img.height()
        no_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=w, height=h)    

    else:
        print("error")
        messagebox.showerror("Error", "Please select an image before proceeding.")

def run_all():
    run_progress()
    enhance_img()

# Create the main window
root = tk.Tk()

# # Add a label to the window
# label = tk.Label(root, text="Hello, world!")
# label.pack()
root.configure(bg='#24C6EB')
root.geometry('1000x600')


frame = tk.Frame(root, bg = "white")
frame.place(relwidth=0.8, relheight=0.7,relx=0.1,rely=0.1)

no_image_label = Label(frame, bg = "white", text="No image selected")
no_image_label.pack(pady=50)

# panel = Label(frame)
# panel.pack()

button_frame = tk.Frame(root,bg='#24C6EB')
button_frame.pack(side='bottom')

button = tk.Button(button_frame, text="Open File", padx=10, pady=5, command=open_file)
button.pack(side = "left", padx=20, pady=10)

button = tk.Button(button_frame, text="Enhance", padx=10, pady=5, command=run_all)
button.pack(side="left", padx=20, pady=10)


# Run the main event loop
root.mainloop()