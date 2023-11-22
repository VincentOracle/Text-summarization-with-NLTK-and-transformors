
#AUTHOR:WERE VINCENT 
#DATE:19th November 2023
#PROGRAM:Text summarization Apllication using NLTK and Transformers


#pip install Transformers #run the command in the terminal when the library is not installed
# Import all the required libraries
import tkinter as tk #Tkinter is the standard GUI (Graphical User Interface) toolkit that
#comes with Python. It provides a set of tools for creating graphical user interfaces,
# including windows, buttons, text fields, and other GUI elements
from tkinter import scrolledtext, messagebox, filedialog
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import heapq #This library provides an implementation of 
#the heap queue algorithm, also known as the priority queue algorithm.
import os
import docx
import PyPDF2
import pandas as pd

# Download NLTK data
# NLTK is used for natural language processing tasks in the code. 
# Specifically, it's used for tokenization (breaking text into words or sentences), 
# downloading stop words,punkt, and performing frequency analysis on words in the text.

nltk.download('punkt')
nltk.download('stopwords')

# Define the TextSummarizerApp class
class TextSummarizerApp:
    def __init__(self, master):
        # Initialize the application window
        self.master = master
        self.master.title("My Text Summarizer App")
        self.master.geometry("1000x600")  # Set window size

        # Styling
        self.master.configure(bg="#0000FF")  # Background color

        # Create a scrolled text widget for user input
        self.text_input = scrolledtext.ScrolledText(master, width=70, height=20, wrap=tk.WORD)
        self.text_input.pack(pady=10)

        # Create an "Upload File" button with styling
        self.upload_button = tk.Button(master, text="Upload File", command=self.upload_file, bg="#00FF00", fg="white", font=('Helvetica', 12, 'bold'))
        self.upload_button.pack(pady=5)

        # Create a "Summarize" button with styling
        self.summarize_button = tk.Button(master, text="Summarize", command=self.summarize_text, bg="#FF0000", fg="white", font=('Helvetica', 12, 'bold'))
        self.summarize_button.pack()

        # Create a label for the summary section
        self.summary_label = tk.Label(master, text="THE SUMMARY", bg="#f0f0f0")  # Background color
        self.summary_label.pack()

        # Create a scrolled text widget for displaying the summary
        self.summary_output = scrolledtext.ScrolledText(master, width=50, height=10, wrap=tk.WORD)
        self.summary_output.pack(pady=10)

        # Create labels for displaying word counts before and after summarization
        self.words_before_label = tk.Label(master, text="Words Before Summarization: 0", bg="#f0f0f0")
        self.words_before_label.pack()

        self.words_after_label = tk.Label(master, text="Words After Summarization: 0", bg="#f0f0f0")
        self.words_after_label.pack()

    # Function to handle file upload
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                           ("Word documents", "*.docx"),
                                                           ("PDF files", "*.pdf"),
                                                           ("Excel files", "*.xlsx;*.xls"),
                                                           ("CSV files", "*.xlsx;*.xls")])
        if file_path:
            with open(file_path, 'rb') as file:
                content = self.read_file_content(file, file_path)
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, content)

    # Function to read content from different file types
    def read_file_content(self, file, file_path):
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.txt':
            return file.read().decode('utf-8', errors='ignore')

        elif file_extension == '.docx':
            doc = docx.Document(file)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

        elif file_extension == '.pdf':
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            return text

        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file)
            return df.to_string(index=False)
        
        elif file_extension in ['.csv', '.csv']:
            df = pd.read_csv(file)
            return df.to_string(index=False)
        else:
            messagebox.showwarning("Unsupported File Type", "This application currently supports only .txt, .docx, .pdf, .xlsx, and .xls files.")
            return ''

    # Function to perform text summarization
    def summarize_text(self):
        input_text = self.text_input.get("1.0", tk.END)

        if not input_text.strip():
            messagebox.showwarning("Warning", "Please enter some text for summarization.")
            return

        # Count words before summarization
        words_before = len(word_tokenize(input_text))

        stop_words = set(stopwords.words("english"))
        words = word_tokenize(input_text)
        words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

        word_frequencies = FreqDist(words)

        sentences = sent_tokenize(input_text)
        sentence_scores = {sentence: sum(word_frequencies[word.lower()] for word in word_tokenize(sentence) if word.lower() in word_frequencies) for sentence in sentences}

        # Extract the top 5 sentences based on scores
        summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
        summary = " ".join(summary_sentences)

        # Count words after summarization
        words_after = len(word_tokenize(summary))

        # Display the summary in the scrolled text widget
        self.summary_output.delete("1.0", tk.END)
        self.summary_output.insert(tk.END, summary)

        # Update words labels
        self.words_before_label.config(text=f"Words Before Summarization: {words_before}")
        self.words_after_label.config(text=f"Words After Summarization: {words_after}")

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = TextSummarizerApp(root)
    root.mainloop()

#THE END OF IMPLEMENTATION