from pytube import YouTube
import tkinter
from tkinter import messagebox, ttk
import customtkinter
import threading

root_tk = tkinter.Tk()
root_tk.geometry("400x300")  # Adjusted height to accommodate the progress bar
root_tk.config(background='blue')
root_tk.title("YouTube Downloader")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    root_tk.update_idletasks()


def downloading_video(url):
    try:
        youtube_object = YouTube(url, on_progress_callback=on_progress)
        stream = youtube_object.streams.get_highest_resolution()
        stream.download()
        messagebox.showinfo('Download Complete', 'The download has completed successfully.')
    except Exception as e:
        messagebox.showerror('Error occurred', 'Check internet or try again')


def button_function():
    url = entry.get()

    if not url:
        messagebox.showerror('Error', 'Please enter a URL')
        return

    proceed_downloading = messagebox.askokcancel('Download Ready', 'Do you want to proceed with the download?')
    if proceed_downloading:
        downloading_thread = threading.Thread(target=downloading_video, args=(url,))
        downloading_thread.start()
    else:
        messagebox.showinfo("Download", "Canceled")


entry = customtkinter.CTkEntry(master=root_tk)
entry.grid(row=0, column=0, padx=20, pady=20, sticky='ew')  # Added padding and set sticky to 'ew' for center alignment

# Button widget configuration with increased size and matching height
button = customtkinter.CTkButton(master=root_tk, corner_radius=10, command=button_function)
button.grid(row=0, column=1, padx=20, pady=20, sticky='ew')  # Added padding and set sticky to 'ew' for center alignment

# Progress bar configuration
progress_var = tkinter.DoubleVar()
progress_bar = ttk.Progressbar(master=root_tk, variable=progress_var, maximum=100)
progress_bar.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky='ew')  # Added padding and set sticky to 'ew' for center alignment
root_tk.mainloop()
