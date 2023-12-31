import tkinter as tk
from urlcalls import url_corr
from urlcalls import clean_message
from main import browser_emulator


def process_input():
    input_text = entry.get()
    print("Prompt Request:", input_text)

    if url_corr(clean_message(input_text)) == 0:
        error_label.config(text="Please specify your request")
    elif url_corr(clean_message(input_text)) == 1:
        error_label.config(text="This request is not possible in the current update.")
    else:
        error_label.config(text="")
        user_prompt = "hello"
        browser_emulator(url_corr(clean_message(input_text))[0], user_prompt)


# window
window = tk.Tk()
window.geometry("750x200")

# error message
error_label = tk.Label(window, fg="red")
error_label.pack()

entry = tk.Entry(window, width=60)
entry.pack(pady=20)

button = tk.Button(window, text="Enter your prompt here:", command=process_input)
button.pack()

# starting gui
window.mainloop()
