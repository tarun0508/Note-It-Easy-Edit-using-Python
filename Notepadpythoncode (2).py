import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr

class Notepad:
    def _init_(self, root):
        self.root = root
        self.text_area = tk.Text(root)
        self.text_area.pack(expand=True, fill='both')

        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.speech_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.speech_menu.add_command(label="Transcribe Speech", command=self.transcribe_speech)
        self.menu_bar.add_cascade(label="Speech", menu=self.speech_menu)

        self.root.config(menu=self.menu_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(content)

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def transcribe_speech(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            self.text_area.delete(1.0, tk.END)  # Clear previous text
            print("Speak now...")
            try:
                audio = r.listen(source, timeout=3)  # Listen for audio with timeout
                print("Transcribing...")
                text = r.recognize_google(audio)
                self.text_area.insert(tk.END, text)
                print("Transcription complete.")
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio.")
            except sr.RequestError as e:
                print("Could not request results from the speech recognition service; {0}".format(e))
            except sr.WaitTimeoutError:
                print("No speech detected within the timeout.")

root = tk.Tk()
root.title("NOTEIT-EASYEDIT")
notepad = Notepad(root)
root.mainloop()