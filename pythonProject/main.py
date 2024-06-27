import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import pyttsx3
from textblob import TextBlob

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to analyze paragraph sentiment, speak with emotion modulation, and plot parameter variations
def analyze_and_visualize_emotion(paragraph):
    sentences = paragraph.split(".")  # Split paragraph into sentences
    overall_sentiment = 0
    pitch_values = []
    volume_values = []
    rate_values = []

    for idx, sentence in enumerate(sentences):
        sentiment = TextBlob(sentence).sentiment
        overall_sentiment += sentiment.polarity

        # Adjust voice parameters based on sentiment of each sentence
        voice_params = {
            'rate': 175,  # Normal speech rate
            'volume': 1.0,  # Normal volume
            'pitch': 50,  # Normal pitch
            'voice': engine.getProperty('voices')[0]  # Default voice
        }

        if sentiment.polarity > 0:
            # Positive sentiment
            voice_params['rate'] = 185  # Increase speech rate for positive sentiment
            voice_params['volume'] = 1.4  # Increase volume for enthusiasm
            voice_params['pitch'] = 70  # Raise pitch for excitement
        elif sentiment.polarity < 0:
            # Negative sentiment
            voice_params['rate'] = 150  # Decrease speech rate for negative sentiment
            voice_params['volume'] = 0.9  # Decrease volume for somberness
            voice_params['pitch'] = 30  # Lower pitch for sadness

        pitch_values.append(voice_params['pitch'])
        volume_values.append(voice_params['volume'])
        rate_values.append(voice_params['rate'])

        # Set voice parameters
        for param, value in voice_params.items():
            engine.setProperty(param, value)

        engine.say(sentence.strip())  # Speak the sentence

    # Adjust overall voice parameters based on the overall sentiment of the paragraph
    overall_sentiment /= len(sentences)  # Calculate average sentiment
    if overall_sentiment > 0:
        # Positive overall sentiment
        engine.say("Overall, the paragraph has a positive tone. Great to hear that!")
    elif overall_sentiment < 0:
        # Negative overall sentiment
        engine.say("Overall, the paragraph has a negative tone. I'm sorry to hear that.")

    engine.runAndWait()

    # Plotting the variation in parameters
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.plot(pitch_values)
    for i, (x, y) in enumerate(zip(range(len(pitch_values)), pitch_values)):
        plt.text(x, y, f'({i}, {y:.1f})', fontsize=8, color='red')  # Annotate points with coordinates
    plt.title('Pitch Variation')
    plt.xlabel('Sentence')
    plt.ylabel('Pitch')

    plt.subplot(3, 1, 2)
    plt.plot(volume_values)
    for i, (x, y) in enumerate(zip(range(len(volume_values)), volume_values)):
        plt.text(x, y, f'({i}, {y:.1f})', fontsize=8, color='red')  # Annotate points with coordinates
    plt.title('Volume Variation')
    plt.xlabel('Sentence')
    plt.ylabel('Volume')

    plt.subplot(3, 1, 3)
    plt.plot(rate_values)
    for i, (x, y) in enumerate(zip(range(len(rate_values)), rate_values)):
        plt.text(x, y, f'({i}, {y:.1f})', fontsize=8, color='red')  # Annotate points with coordinates
    plt.title('Speech Rate Variation')
    plt.xlabel('Sentence')
    plt.ylabel('Speech Rate')

    plt.tight_layout()
    plt.show()

def play_audio():
    paragraph = text_entry.get("1.0", tk.END).strip()
    if paragraph:
        analyze_and_visualize_emotion(paragraph)
    else:
        messagebox.showwarning("Warning", "Please enter a paragraph.")

# Create the main window
root = tk.Tk()
root.title("Tone Tuner")
root.configure(bg="#222")

# Center the window on the screen
window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a frame for the content
content_frame = tk.Frame(root, bg="white", bd=3, relief=tk.SUNKEN)
content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create a label for the title
title_label = tk.Label(content_frame, text="Tone Tuner", font=("Arial", 20), bg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

# Create a text entry field
text_entry = tk.Text(content_frame, width=40, height=10, bg="#ccc", bd=2, relief=tk.GROOVE)
text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a button to play audio
play_button = tk.Button(content_frame, text="Play", command=play_audio, font=("Arial", 12), bg="#007bff", fg="white", bd=0)
play_button.grid(row=2, column=0, columnspan=2, pady=(0, 20), padx=10)

# Run the Tkinter event loop
root.mainloop()