

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import heapq

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

class TextSummarizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("My Text Summarizer App")
        self.master.geometry("1000x600")  # Set window size

        # Styling
        self.master.configure(bg="#0000FF") # Background color

        self.text_input = scrolledtext.ScrolledText(master, width=70, height=20, wrap=tk.WORD)
        self.text_input.pack(pady=10)

        self.upload_button = tk.Button(master, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=5)

        self.summarize_button = tk.Button(master, text="Click to Summarize", command=self.summarize_text)
        self.summarize_button.pack()

        self.summary_label = tk.Label(master, text="Summary:", bg="#f0f0f0")  # Background color
        self.summary_label.pack()

        self.summary_output = scrolledtext.ScrolledText(master, width=50, height=10, wrap=tk.WORD)
        self.summary_output.pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, content)

    def summarize_text(self):
        input_text = self.text_input.get("1.0", tk.END)

        if not input_text.strip():
            messagebox.showwarning("Warning", "Please enter some text for summarization.")
            return

        stop_words = set(stopwords.words("english"))
        words = word_tokenize(input_text)
        words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

        word_frequencies = FreqDist(words)

        sentences = sent_tokenize(input_text)
        sentence_scores = {sentence: sum(word_frequencies[word.lower()] for word in word_tokenize(sentence) if word.lower() in word_frequencies) for sentence in sentences}

        summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
        summary = " ".join(summary_sentences)

        self.summary_output.delete("1.0", tk.END)
        self.summary_output.insert(tk.END, summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextSummarizerApp(root)
    root.mainloop()




