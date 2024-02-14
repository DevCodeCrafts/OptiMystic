"""
Author: DevCodeCrafts
Description: Random choice decider. Detects if it's a question of many choices (2 or more) and then selects one
              If it is just one choice, then it will give you a random choice such as the magic 8 ball
              Save answers into a document, detects different question and draws a line while saving answer
              Additional feature: flipping a coin or multiple coins
Created on Saturday, February 3, 2024, 6:52 PM 
"""

from datetime import datetime
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import random
import re
import sys
import os

modal_verbs = ["can", "could", "may", "might", "shall", "will", "would", "must", "should", "am"]
words_to_remove = [ "they", "she", "he", "I", "play", "do", "help"] + modal_verbs

logo_path = "Symb.png"
progImg = Image.open("ProgArt.png")
og_img = Image.open("SubmitButton.png")

def remove_words(text):
    # Construct a regular expression pattern to match words before and including the specified keywords, ignoring symbols
    pattern = re.compile(r'(?i)\b(?:' + '|'.join(words_to_remove) + r')\b[^\w\s]*')

    result =  pattern.sub('', text).strip()
    result = re.sub(r'^[^\w\s]*|[^\w\s]*$', '', result)  # Remove leading and trailing symbols
    return result

def remove_words_before_modal(text):
    # Construct a regular expression pattern to match all words and spaces before any modal verbs, ignoring symbols
    pattern = re.compile(r'.*?\b(?:' + '|'.join(modal_verbs) + r')\b', flags=re.IGNORECASE)

    result = pattern.sub('', text).strip()
    result = re.sub(r'^[^\w\s]*|[^\w\s]*$', '', result)  # Remove leading and trailing symbols
    return result

def type_effect(widget, text, speed=80, index=0):
    if index <= len(text):
        widget.configure(text=' ' + text[:index], anchor='w')
        widget.after(speed, lambda: type_effect(widget, text, speed, index + 1))

def read_8ball(filename="EightBallAns.txt"):
    filename = os.path.join(sys._MEIPASS, filename) if hasattr(sys, '_MEIPASS') else filename
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def flip_coin(input_text):
    match = re.search(r'flip a coin (\d+) times', input_text)    # Extract the number of times to flip the coin from the input text
    
    if match:
        num_flips = int(match.group(1))
        results = {"Heads": 0, "Tails": 0}

        # Simulate coin flips
        for _ in range(num_flips):
            result = random.choice(["Heads", "Tails"])
            results[result] += 1

        # Display the results
        result_text = f"You flipped a coin {num_flips} times.\n You landed on:\n\n Heads:   {results['Heads']} \n Tails:      {results['Tails']}   "
        # Prints result
        CoinOutput = ctk.CTkLabel(scroll_frame, 
                                  text=result_text, 
                                  font=ctk.CTkFont(size=18, weight="bold"), 
                                  text_color="#2F4858",
                                  justify='left')
        CoinOutput.pack(padx=50, pady=5, anchor='w')        # Positioning

        type_effect(CoinOutput, result_text, speed=80)      #Calling type_effect to apply effect to result text

        scroll_frame._parent_canvas.update_idletasks()
        scroll_frame._parent_canvas.configure(scrollregion=scroll_frame._parent_canvas.bbox("all"))
        scroll_frame._parent_canvas.yview_moveto(1.0)   # Auto scrolls to the bottom   
    else:
        messagebox.showinfo("Invalid Input", "Invalid coin flip command.") # Sends a pop-up with the given message

def print_bot_info(scroll_frame, logo_path, name, input_text):
    logoSize = (47, 47)  # Determining the resize
    logo_path = os.path.join(sys._MEIPASS, logo_path) if hasattr(sys, '_MEIPASS') else logo_path  # Adjusting the logo path
    botLogo = ctk.CTkImage(Image.open(logo_path), size=logoSize)  # Assign image and size to variable

    # Print Results
    bot_info = ctk.CTkLabel(scroll_frame,
                            image=botLogo,
                            compound="left",
                            text=name,
                            font=ctk.CTkFont(family="Robot 9000", size=22, weight="bold"),
                            text_color="#4F4537")
    bot_info.pack(anchor='w')  # Positioning

    # Prints your input
    Output = ctk.CTkLabel(scroll_frame,
                          text=input_text,
                          font=ctk.CTkFont(size=20, weight="bold"),
                          text_color="#3D4A3D",
                          wraplength=900,
                          justify='left')
    Output.pack(padx=50, pady=5, anchor='w')  # Positioning
    Input.delete(0, 'end')  # Clears Input Text Bar
    
# Prints input into scrollable frame while printing it's own name
def submit():

    puInput = Input.get() # Calls your input

    if puInput.endswith('?') or re.search(r'\sor\s|\s*,\s*|,$', puInput):
    
        print_bot_info(scroll_frame, "Symb.png", "Deciso", puInput)                 # Calls function and Prints bot logo and name
        cleaned_input = remove_words(remove_words_before_modal(puInput.lower()))
        typo_match = re.search(r'\b\w+\?\d*\b', cleaned_input)
        
        if typo_match:
            typo_word = typo_match.group()
            corrected_word = typo_word.rstrip('?1234567890')  # Remove "?" and digits
            cleaned_input = cleaned_input.replace(typo_word, corrected_word)
        
        if re.search(r'\sor\s|\s,\s|\s*,\s*', cleaned_input):
            choices = re.split(r'\sor\s|\s,\s|\s*,\s*', cleaned_input)  # Split choices
            choices = [choice.strip() for choice in choices if choice.strip()]  # Remove empty choices
            chosen_choice = random.choice(choices).capitalize()  # Randomly choose one of the non-empty choices

            # Print chosen choice
            MainOutput = ctk.CTkLabel(scroll_frame,
                                      text=chosen_choice,
                                      font=ctk.CTkFont(size=18, weight="bold"),
                                      text_color="#2F4858")
            MainOutput.pack(padx=50, pady=5, anchor='w')  # Positioning

            type_effect(MainOutput, chosen_choice)  # Apply typing effect
        else:
            eightBall = read_8ball()  # List of possible 8-ball answers
            chosen_answer = random.choice(eightBall)  # Randomly choose an 8-ball answer

            # Print randomly chosen 8-ball answer
            eightBallOutput = ctk.CTkLabel(scroll_frame,
                                           text=chosen_answer,
                                           font=ctk.CTkFont(size=18, weight="bold"),
                                           text_color="#2F4858")
            eightBallOutput.pack(padx=50, pady=5, anchor='w')

            type_effect(eightBallOutput, chosen_answer, speed=120)  # Apply typing effect

        # Update scroll region and auto-scroll to the bottom
        scroll_frame._parent_canvas.update_idletasks()
        scroll_frame._parent_canvas.configure(scrollregion=scroll_frame._parent_canvas.bbox("all"))
        scroll_frame._parent_canvas.yview_moveto(1.0)  # Auto-scroll to the bottom

    elif re.search(r'flip a coin \d+ times', puInput):
        print_bot_info(scroll_frame, "Symb.png", "Deciso", puInput)  # Print bot info and user input
        flip_coin(puInput)  # Handle coin flip command
    else:
        messagebox.showinfo("Invalid Input", "This is neither a question nor a list of choices.")  # Invalid input message
        return

def linksub(event):                                                                 # To call submit as an event to assign to keybind
    submit()

def resize_handler(event):                                                          # Function to handle window resizing
    new_width = app.winfo_width()
    new_height = app.winfo_height()

    # Resize everything when maximized
    main_frame.configure(width=new_width, height=new_height)
    scroll_frame.configure(width=new_width-85, height=new_height-205)
    DisDate.place(x=40, y=new_height - 30)
    Input.place_configure(width=new_width-114, height=42, y=new_height-74)
    submit_button.place(x=new_width - 80, y=new_height - 74)

now = datetime.now()                    # Assign Date to Variable

app = ctk.CTk()                         # Create the GUI
main_frame = Frame(app, bg="#52584D")   # Background Color
main_frame.pack(fill=BOTH, expand=YES)
app.geometry("1080x720")                # GUI Start up size
app.title("OptiMystic")                 # Title
app.resizable(True, True)

# Imports and resizes Program logo and text
OptiSize = (67,67)
progImg = Image.open(os.path.join(sys._MEIPASS, "ProgArt.png")) if hasattr(sys, '_MEIPASS') else Image.open("ProgArt.png")
progLogo = ctk.CTkImage(progImg, size=OptiSize)
prog_Info = ctk.CTkLabel(main_frame, 
                         image=progLogo, 
                         text=" OptiMystic",
                         font=ctk.CTkFont(family="Mechanismo", size=70, weight="bold"),
                         text_color="#A3CFCD",
                         compound='left')
prog_Info.pack(padx=40,anchor='w')

# Scrollable Frame
scroll_frame = ctk.CTkScrollableFrame(app, 
                                   fg_color="#9AB19A", 
                                   bg_color="#52584D", 
                                   width=985, height=500, 
                                   corner_radius=10, 
                                   scrollbar_fg_color='transparent')
scroll_frame.place(x=30, y=90)
    
# Shows the Date
s1 = now.strftime("%m/%d/%Y")
DisDate = ctk.CTkLabel(app, 
                       text=s1, 
                       font=ctk.CTkFont(size=14, slant="italic"), 
                       text_color="#D9C1BB", 
                       bg_color="#52584D")
DisDate.place(x=40, y=695)

# Input text bar
Input = ctk.CTkEntry(app, 
                     placeholder_text=" Type your Question or Choices Here", 
                     placeholder_text_color="Beige", 
                     width=960, height=40,
                     font=ctk.CTkFont(size=20))
Input.place(x=30, y=657)

# Submit button image
img_size = (35, 35)
og_img = Image.open(os.path.join(sys._MEIPASS, 'SubmitButton.png')) if hasattr(sys, '_MEIPASS') else Image.open('SubmitButton.png')
subPNG = ctk.CTkImage(og_img, size=img_size)

# Submit button itself
submit_button = ctk.CTkButton(app, 
                              text="", 
                              image=subPNG, 
                              command=submit, 
                              width=40, height = 30, 
                              fg_color="#F6EDD9", 
                              bg_color="#52584D", 
                              hover_color="#D0A54F")
submit_button.place(x=1000, y=657)

# Clicking enter activates submit button
app.bind('<Return>', linksub) 

# Bind the resize_handler function to the Configure event
app.bind("<Configure>", resize_handler)

# Runs the GUI
app.mainloop()