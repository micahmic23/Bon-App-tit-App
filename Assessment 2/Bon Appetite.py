#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 20:57:31 2024

@author: geronimojo

API Meal DB - Advanced Programming Assessment 2
"""
# Imports all modules and functions of the tkinter GUI toolkit from Python's Library.
import tkinter as tk

# Imports the ttk module to access Tk themed widgets.
from tkinter import ttk 

# Imports the image objects used to load the images.
from PIL import Image

# Imports imageTk needed to display the images.
from PIL import Image, ImageTk

# Imports imagedraw to implement 2D graphics for image objects and to allow text with fonts to display nicely over images.
from PIL import ImageDraw, ImageFont

# Imports BytesIO that helps convert binary image data into a form that the Pillow can understand.
from io import BytesIO

# Imports messagebox to display informational messages in the app.
from tkinter import messagebox

# Imports json to identify where the domains are imported by the domain being operated on.
import json

# Imports requests module to permits the user to send HTTP requests in python.
import requests

# Imports the pygame module to allow sounds to be implemented in the app.
import pygame

# Sets the main window for the Bon Appétit tkinter app.
main = tk.Tk() # Initializes the GUI toolkit.
main.title("Bon Appétit!") # Creates a title.
main.geometry("800x700") # Sets the window's width and height.
main.resizable(width = False, height = False) # Sets a fixed window size.

# Creates the logo for the tkinter app.
try: # Try and except pass implemented for the logo in case the logo image does not load. This guarantees the app will still run successfully everytime.
    icon = tk.PhotoImage(file="logo_Vfv_icon-5.png") # Stores the logo's image path in the variable 'icon' with the tkinter photoimage module to make use of images in the app.
    main.iconphoto(True, icon) # The image is displayed as the app's logo.
except Exception as e: # Creates an exception in case the image does not load. It displays an error message in the console.
    print(f"Error loading icon: {e}")

# Sets the pygame mixer
pygame.mixer.init()

# Stores the music file path in the variable BGM.
BGM = "/Users/geronimojo/Desktop/CC L5/CC L5 SEM 1/Advanced Programming/Assessment 2/Assets/Music/nhac-jazz-thu-gian-265063.mp3"

# Records the app's music state whenever it is playing or not (True/False). 
playingBGM = False

# A function to play and stop the app's background music.
def toggleBGM():
    # Using the global keyword to modify and read the variable set.
    global playingBGM 
    
    # An if else statement to create an instance whenever the button is pressed to play or stop the music.
    if playingBGM:
        pygame.mixer.music.stop() # Stops the music.
        musicBttn.config(text = "Play Music") # Changes the button's text to 'Play music'.
        playingBGM = False # Sets to false when music stops.
        print("Music has stopped") # Displays a message that the music has stopped.
    else: # Creates another statement.
        pygame.mixer.music.load(BGM) # Plays the music.
        pygame.mixer.music.play(-1) # # Plays it on loop.
        musicBttn.config(text = "Stop Music") # Changes the button's text to 'Stop music'.
        playingBGM = True # Sets to true when music plays again.
        print("Music is playing...♪ ♫ ♬") # Displays a message that the music is playing.
    
# Automatically loads the background music file as soon as the app is run.
pygame.mixer.music.load(BGM)
pygame.mixer.music.play(-1) # Plays the music on loop.
playingBGM = True # True when the music is played.
print("Music is playing...♪ ♫ ♬")

# Imports the meal API links.
baseURL = "https://www.themealdb.com/api/json/v1/1/search.php?s="
randomURL = f"https://www.themealdb.com/api/json/v1/1/random.php"  

# A function to display the meal informations and images.
def mealDisplay(meal, result_box, imgLabel):
    
    try:
        # Imports each meal information and details.
        meal_item = meal.get("strMeal", "N/A") # Meal name
        categ = meal.get("strCategory", "N/A") # Meal category
        Area = meal.get("strArea", "N/A") # Meal area
        instruct = meal.get("strInstructions", "N/A") # Meal instructions
        thmbnail = meal.get("strMealThumb", "") # Meal image
            
        # Displays each meal's information as a text in the variable it is assigned to.
        result_txt = f"Meal Name: {meal_item}\n"
        result_txt += f"Category: {categ}\n"
        result_txt += f"Area: {Area}\n"
        result_txt += f"Instructions: \n{instruct}\n"
        
        # Clears the current content displayed inside the text widget 'result_box' in order to display the new meal information text afterwards.
        # The new text is added using 'insert'. 
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, result_txt)
        
        # If else portion of the function that displays the image label as part of the meal information.
        # Checks if a meal's image is existing.
        if thmbnail:
            
            feedback = requests.get(thmbnail) # Sends a request to the feedback variable to retrieve the image.
            feedback.raise_for_status() # Brings up an error if the inquiry for the image is not succesful.
                    
            imgData = feedback.content # Takes in the raw image data from the feedback.
            image = Image.open(BytesIO(imgData)) # Loads the image using PIL and covers the image with BytesIO to act as a file.
            image = image.resize((250,250), Image.Resampling.LANCZOS) # Resizes the image using high definition image resampling.
            imgTk = ImageTk.PhotoImage(image) # Converting the image's format from PIL to photoimage that is suitable to display in tkinter.
            imgLabel.config(image = imgTk) # Updates the image label widget for the new image to be displayed.
            imgLabel.image = imgTk # An image reference is saved in the image label widget to prevent it from being stored in the trash.
        else:
            imgLabel.config(image = None) # When a meal image does not exist, the previous image is cleared in the imagelabel widget.
            imgLabel.image = None # Sets the 'imgLabel.image' to 'None' when a meal has no image available with it.
    except Exception as e:
        messagebox.showerror("Image Error", f"Unable to load image: {e}") # Displays an error message when handling any exceptions that take place.

# A define function to fetch and display meal information taken from the meal name given.         
# Parameters used:
# meal_item1 is the variable used for when a meal name is searched for.
# searchresult_box is for the text box widget used to display the meal information.
# searchimgLabel is the label widget used to display the meal's image.
def getMeal(meal_item1, searchresult_box, searchimgLabel):
    
    # Determines if the meal name is empty.
    if not meal_item1.strip():
        # Displays an error message to remind the user to enter a meal name.
        messagebox.showerror("Error", "Please enter a meal name.")
        return
    
    # Tries to retrieve meal data from the API.
    try:
        feedback = requests.get(baseURL + meal_item1) # Sends a request to the API database through the base url and meal name.
        feedback.raise_for_status() # Brings up an error if the inquiry for the meal's status code is not succesful.
        
        data = feedback.json() # Extracts the API feedback as json data.
        meal1 = data.get("meals") # Takes the 'meals' key from the json data.
        
        if meal1: # A conditional statement to check if the 'meals' key consists of data.
            searchresult_box.delete("1.0", tk.END)  # Clears the current content displayed inside the text widget 'result_box'.
            meals = meal1[0] # Takes the first meal searched from the meal list exisiting.
            
            # Imports each meal information and details for the search a meal portion of the app.
            meal_item1 = meals.get("strMeal", "N/A") # Meal name
            categ1 = meals.get("strCategory", "N/A") # Meal category
            Area1 = meals.get("strArea", "N/A") # Meal area
            instruct1 = meals.get("strInstructions", "N/A") # Meal instructions
            thmbnail1 = meals.get("strMealThumb", "") # Meal image
            
            # Displays the each meal's information as a text in the variable it is assigned to.
            searchresult_txt = f"Meal Name: {meal_item1}\n"
            searchresult_txt += f"Category: {categ1}\n"
            searchresult_txt += f"Area: {Area1}\n"
            searchresult_txt += f"Instructions: {instruct1}\n"
            
            searchresult_box.insert(tk.END, searchresult_txt) # Inserts the meal details into the result box widget.
            
            # Another conditional statement is created for the meal image within the get meal function.
            if thmbnail1: # Checks if a meal's image is existing.
                try: # Attempt to fetch a meal's image.
                    Feedback = requests.get(thmbnail1) # Sends a request to the feedback variable to retrieve the image.
                    Feedback.raise_for_status() # Brings up an error if the inquiry for the image is not succesful.
                    
                    imgData = Feedback.content # Takes in the raw image data from the feedback.
                    image = Image.open(BytesIO(imgData)) # Loads the image using PIL and covers the image with BytesIO to act as a file.
                    image = image.resize((200, 200), Image.Resampling.LANCZOS) # Resizes the image using high definition image resampling.
                    imgTk = ImageTk.PhotoImage(image) # Converting the image's format from PIL to photoimage that is suitable to display in tkinter.
                    searchimgLabel.config(image = imgTk) # Updates the search image label widget for the new image to be displayed.
                    searchimgLabel.image = imgTk # An image reference is saved in the image label widget to prevent it from being stored in the trash.
                    
                except Exception as imgError: # Creates an exception incase there is an error in loading or retrieving the meal image.
                    searchimgLabel.config(image = None) # Empties the image label when an error takes place.
                    searchimgLabel.image = None # Sets the meal image to None.
                    messagebox.showerror("Image Error", f"Failed to load image: {imgError}") # Displays an error message regarding the image that failed to load.
                    
        else: # An else statement if no data is found regarding the image.
            searchresult_box.delete("1.0", tk.END) # Empties out any data found in the result box.
            searchresult_box.insert(tk.END, "Uh-oh! No meal found, Try a different meal name.") # Inserts a message in the box saying that no data is found about the meal searched.
            searchimgLabel.config(image = None) # Empties the image label when an error takes place.
            searchimgLabel.image = None # Sets the meal image to None.
            
    except requests.exceptions.RequestException as reqError: # Deals with exceptions that involve API requests.
        messagebox.showerror("Request Error", f"Failed to retrieve data: {reqError}") # Prints an error message about being unable to retrieve the data.
        
    except Exception as e: # Deals with other exceptions that may occur.
        messagebox.showerror("Error", f"Oh no! An unexpected error occurred: {e}") # Prints an error message about an unexpected problem that has occured.
          
# A define function is used to retrieve and display a random meal.
# Parameters include:
# result_box is a text box widget wherein the meal's information is shown.
# imgLabel is a label widget where the meal's image is displayed.
def getRandom(result_box, imgLabel):
    
    try: # Tries to retrieve random meal data from the API.
        feedback = requests.get(randomURL) # Sends a request to the API database through the random meal url.
        feedback.raise_for_status() # Brings up an error if the inquiry for the random meal's status code is not succesful.
        data = feedback.json() # Extracts the API feedback as json data.
        meal = data.get("meals") # Takes the 'meals' key from the json data.
        
        if meal: # A conditional statement to check if the 'meals' key consists of data.
            mealDisplay(meal[0], result_box, imgLabel) # The mealDisplay function is used to display the meal's information and image.
            
        else: # A conditional statement if no meal data exists.
            result_box.delete("1.0", tk.END) # Empties any content found inside the result box widget.
            result_box.insert(tk.END,"No meal found. Try a different meal name.") # Inserts an error message that the meal searched is not found.
            imgLabel.config(image = None) # When a meal image does not exist, the previous image is cleared in the imagelabel widget.
            imgLabel.image = None # Sets the 'imgLabel.image' to 'None' when a meal has no image available with it.
            
    except requests.exceptions.RequestException as reqError: # Deals with exceptions that involve API requests.
        messagebox.showerror("Request Error", f"Unable to retrieve data: {reqError}") # Prints an error message about being unable to retrieve the data.
        
    except Exception as e: # Deals with other exceptions that may occur.
        messagebox.showerror("Error", f"An unexpected error has occured: {e}") # Prints an error message about an unexpected problem that has occured.

# A define function to allow the user to navigate through different frames.    
def shiftframe(frame): # The frame is set as a parameter.
    frame.tkraise() # A frame is brought to the top when accessed.
    
# A define function to display a messagebox about the app's information.
def infoapp():
    # Prepares the message to be displayed in the messagebox
    mssg = "Welcome to Bon Appétit! \n \n A simple desktop application filled with meals! \n \n Press the Main page to discover meals! \n \n Enjoy and Bon Appétit!"
    messagebox.showinfo("Instructions",mssg) # Displays the message above inside the messagebox given, under the title 'Instructions'.
    
# A define function to close the tkinter app.
def close():
    pygame.mixer.music.stop() # Stops the music when the app is closed.
    main.quit() # Stops the app's program from running.
    print("Au revoir!") # Displays a message when closed.
    
# A frame widget 'frame1' is created which will be the first frame displayed in the app.
frame1 = tk.Frame(main, width=800, height=700) 

refImages = {} # An empty dictionary is created to store image references to avoid it from being moved to the trash.

try:
    img_path = "1.png" # The image path is assigned as frame1's background image.
    bg_img = Image.open(img_path).resize((800,700), Image.Resampling.LANCZOS) # Opens the image and resizes it using the image resampling attribute.
    bg_pic = ImageTk.PhotoImage((bg_img)) # Converts the PIL image to a format suitable with Tkinter.
    refImages["frame1"] = bg_pic # Transfers the image reference in the dictionary to prevent trash collection.
    
    draw = ImageDraw.Draw(bg_img) # Sets an ImageDraw object for the background image to be drawn on.
    font_path = "PlayfairDisplay-Black.ttf" # The font path is assigned.
    font = ImageFont.truetype(font_path, 80) # Setting the font's size to 80.
    draw.text((200,50), "Bon Appétit!", fill = "black", font = font) # The font text is drawn on the background image in the position (200, 50).

    bg_pic = ImageTk.PhotoImage(bg_img) # Converts the PIL format image into an image with a format suitable for Tkinter
    refImages["frame1"] = bg_pic # Updates the image reference located in the dictionary.
    
    bg_label = tk.Label(frame1, image = bg_pic) # A label widget is created to display the background image inside 'frame1'.
    bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1) # Covers the whole area of 'frame1'. 
    
except Exception as e: # Incase an error happens while the image loads, an error message is displayed.
    print(f"Error loading images: {e}")

# The first button widget lets you navigate to the main page using the function 'shiftframe' created earlier. 
nxtBttn = tk.Button(frame1, text = "Go to Main page",bg="#773d00" ,fg="black",font=('Arial',40,'bold'),bd=0, command=lambda:shiftframe(mainframe))
nxtBttn.place(x = 235, y = 235)

# The second button widget displays a messagebox that shows the app's information. This is done by using the function 'infoapp'.
infoBttn = tk.Button(frame1, text = "App Information",fg="black", font=('Arial', 40,'bold'), command = infoapp)
infoBttn.place(x = 235, y = 310)

# The third button widget stops or plays the background music when toggled on. The function 'toggleBGM' makes this happen.
musicBttn = tk.Button(frame1, text = "Stop Music",fg="black", font=('Arial', 40,'bold'), command = toggleBGM)
musicBttn.place(x = 235, y = 390, width = 350)

# The fourth button widget exits the app using the function 'close'.
quitBttn = tk.Button(frame1, text = "Quit",fg="black", font=('Arial', 40,'bold'), command = close)
quitBttn.place(x = 235, y = 470, width = 350)

# Positions the frame in the top-left corner of the window.
frame1.place(x=0,y=0) 

# The second frame widget 'mainframe' is created and appears when pressing 'nxtBttn'.
mainframe = tk.Frame(main, width=800, height=700)

# The same concept is repeated here but is just replaced with new variables for mainframe's background image.
# An empty dictionary is created to store image references to avoid it from being moved to the trash.
refImages = {} 

try:
    img_path2 = "2.png" # The second image path is assigned as mainframe's background image.
    bg_img2 = Image.open(img_path2).resize((800,700), Image.Resampling.LANCZOS) # Opens the image and resizes it using the image resampling attribute.
    bg_pic2 = ImageTk.PhotoImage((bg_img2)) # Converts the PIL image to a format suitable with Tkinter.
    refImages["mainframe"] = bg_pic2 # Transfers the image reference in the dictionary to prevent trash collection.
    
    draw2 = ImageDraw.Draw(bg_img2) # Sets an ImageDraw object for the background image to be drawn on.
    font_path2 = "PlayfairDisplay-Black.ttf" # The font path is assigned.
    font2 = ImageFont.truetype(font_path2, 80) # Setting the font's size to 80.
    draw2.text((200,50), "Bon Appétit!", fill = "black", font = font2) # The font text is drawn on the background image in the position (200, 50).

    bg_pic2 = ImageTk.PhotoImage(bg_img2) # Converts the PIL format image into an image with a format suitable for Tkinter.
    refImages["mainframe"] = bg_pic2 # Updates the image reference located in the dictionary.
    
    bg_label2 = tk.Label(mainframe, image = bg_pic2) # A label widget is created to display the background image inside 'mainframe'.
    bg_label2.place(x = 0, y = 0, relwidth = 1, relheight = 1) # Covers the whole area of 'mainframe'. 
    
except Exception as e: # Incase an error happens while the image loads, an error message is displayed.
    print(f"Error loading images: {e}")

# The first button widget within the second frame lets you navigate to the third frame of the app called 'searchframe' where you can search for a specific meal.
mealBttn = tk.Button(mainframe, text = "Search a meal",bg="#773d00" ,fg="black",font=('Arial',40,'bold'),bd=0, command=lambda:shiftframe(searchframe))
mealBttn.place(x = 260, y = 260)

# The second button widget brings you to the fourth frame called 'randomframe' where you can get random meals.
randomBttn = tk.Button(mainframe, text = "Generate a random meal",fg="black", font=('Arial', 40,'bold'), command = lambda:shiftframe(randomframe))
randomBttn.place(x = 160, y = 340)

# The third button takes you back to the first frame 'frame1'.
backBttn = tk.Button(mainframe, text = "Go back",fg="black", font=('Arial', 40,'bold'), command=lambda:shiftframe(frame1) )
backBttn.place(x = 310, y = 425)

# Positions the frame in the top-left corner of the window.
mainframe.place(x = 0, y = 0)

# The third frame widget 'searchframe' is created and appears when pressing 'mealBttn'.
searchframe = tk.Frame(main, width=800, height=700)

# The same concept is repeated here, but is just replaced with new variables for searchframe's background image.
# An empty dictionary is created to store image references to avoid it from being moved to the trash.
refImages = {}

try:
    img_path3 = "3.png" # The third image path is assigned as searchframe's background image.
    bg_img3 = Image.open(img_path3).resize((800,700), Image.Resampling.LANCZOS) # Opens the image and resizes it using the image resampling attribute.
    bg_pic3 = ImageTk.PhotoImage((bg_img3)) # Converts the PIL image to a format suitable with Tkinter.
    refImages["searchframe"] = bg_pic3 # Transfers the image reference in the dictionary to prevent trash collection.
    
    draw3 = ImageDraw.Draw(bg_img3) # Sets an ImageDraw object for the background image to be drawn on.
    font_path3 = "PlayfairDisplay-Black.ttf" # The font path is assigned.
    font3 = ImageFont.truetype(font_path3, 80) # Setting the font's size to 80.
    draw3.text((170,50), "Search a meal!", fill = "black", font = font2) # The font text is drawn on the background image in the position (170, 50).

    bg_pic3 = ImageTk.PhotoImage(bg_img3) # Converts the PIL format image into an image with a format suitable for Tkinter.
    refImages["searchframe"] = bg_pic3 # Updates the image reference located in the dictionary.
    
    bg_label3 = tk.Label(searchframe, image = bg_pic3) # A label widget is created to display the background image inside 'searchframe'.
    bg_label3.place(x = 0, y = 0, relwidth = 1, relheight = 1) # Covers the whole area of 'searchframe'.
    
except Exception as e: # In case an error happens while the image loads, an error message is displayed.
    print(f"Error loading images: {e}")
   
# An entry widget is created to let the user enter in a meal name.  
food_entry = tk.Entry(searchframe, font = ("Arial" , 20))
food_entry.place(x = 230, y = 200, width = 280)
    
# A button widget is created to search the meal name entered in. The meal name's information is then requested using the function called 'getMeal'. 
# The three widgets are set as parameters to operate the function through them.
search_button = tk.Button(searchframe, text = "Search", font = ("Arial" , 20), bg = "white", command = lambda: getMeal(food_entry.get(), searchresult_box, searchimgLabel))
search_button.place(x = 520, y = 200)

# An image label is set to display the meal's image in.
searchimgLabel = tk.Label(searchframe)
searchimgLabel.place(x=490, y = 300)

# A text box widget is made to insert the meal's information results in.
searchresult_box = tk.Text(searchframe, wrap = "word", font = ("Arial" , 20), bg = "white", fg = "black")
searchresult_box.place(x = 70, y = 270, height = 280, width = 380)
    
# Another button widget is created to bring the user back to the first page.
backBttn2 = tk.Button(searchframe, text = "Go back", font = ("Arial" , 20), bg = "white", command = lambda: shiftframe(mainframe))
backBttn2.place(x = 360, y = 580)

# Positions the frame in the top-left corner of the window.
searchframe.place(x = 0, y = 0)

# The fourth frame widget 'randomframe' is created and appears when pressing 'randomBttn'.
randomframe = tk.Frame(main, width = 800, height = 700)

# The same concept is repeated here, but is just replaced with new variables for randomframe's background image.
# An empty dictionary is created to store image references to avoid it from being moved to the trash.
refImages = {}

try:
    img_path4 = "1.png" # The first image path is assigned again as randomframe's background image.
    bg_img4 = Image.open(img_path4).resize((800,700), Image.Resampling.LANCZOS) # Opens the image and resizes it using the image resampling attribute.
    bg_pic4 = ImageTk.PhotoImage((bg_img4)) # Converts the PIL image to a format suitable with Tkinter.
    refImages["randomframe"] = bg_pic4 # Transfers the image reference in the dictionary to prevent trash collection.
    
    draw4 = ImageDraw.Draw(bg_img4) # Sets an ImageDraw object for the background image to be drawn on.
    font_path4 = "PlayfairDisplay-Black.ttf" # The font path is assigned.
    font4 = ImageFont.truetype(font_path4, 60) # Setting the font's size to 60.
    draw4.text((130,50), "Get a random meal!", fill = "black", font = font4) # The font text is drawn on the background image in the position (130, 50).

    bg_pic4 = ImageTk.PhotoImage(bg_img4) # Converts the PIL format image into an image with a format suitable for Tkinter.
    refImages["randomframe"] = bg_pic4 # Updates the image reference located in the dictionary.
    
    bg_label4 = tk.Label(randomframe, image = bg_pic4) # A label widget is created to display the background image inside 'randomframe'.
    bg_label4.place(x = 0, y = 0, relwidth = 1, relheight = 1) # Covers the whole area of 'randomframe'.
    
except Exception as e: # In case an error happens while the image loads, an error message is displayed.
    print(f"Error loading images: {e}")

# The first button widget in the fourth frame 'randomframe' lets you generate random meals when interacted. This is done using the function 'getRandom'.
generateBttn = tk.Button(randomframe, text = "Get random meal", font = ("Arial" , 30, "bold"), bg = "white", command = lambda: getRandom(result_box, imgLabel))
generateBttn.place(x = 270, y = 180)

# An image label is set to display the meal's image in.
imgLabel = tk.Label(randomframe)
imgLabel.place(x=490, y = 260)

# A text box widget is made to insert the meal's information results in.
result_box = tk.Text(randomframe, wrap = "word", font = ("Arial" , 20), bg = "white", fg = "black")
result_box.place(x = 70, y = 250, height = 280, width = 380)

# Another button widget is created to bring the user back to the first page.
backBttn3 = tk.Button(randomframe, text = "Go back", font = ("Arial" , 20), bg = "white", command = lambda: shiftframe(mainframe))
backBttn3.place(x = 360, y = 580)

# Positions the frame in the top-left corner of the window.
randomframe.place(x = 0, y = 0)

# Displays the first frame when the app is opened.
shiftframe(frame1)

# Runs the main event on lopp for the app to run endlessly.
main.mainloop()