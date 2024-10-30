## Image Selection

# Import necessary modules
import os
import random
from psychopy import visual, event, core, gui

# Folder containing images
image_folder = r'./'  # Update with your image folder path

# Get all images from the folder
all_images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith('.jpg')]

# Randomly select 36 images without replacement
selected_images = random.sample(all_images, 36)

# Define the emotion map based on the third last character in the filename
emotion_map = {
    'n': 'Neutrality',
    's': 'Sadness',
    'd': 'Disgust',
    'f': 'Fear',
    'a': 'Anger',
    'h': 'Happiness'
}

# List to store participant's responses
responses = []

# Create a window
win = visual.Window(size=(800, 600), color='black')

# Create clickable squares (polygons) for the emotion options
option_squares = [visual.Rect(win, width=0.3, height=0.3, pos=(-0.5, -0.5), fillColor='white'),
                  visual.Rect(win, width=0.3, height=0.3, pos=(0.5, -0.5), fillColor='white'),
                  visual.Rect(win, width=0.3, height=0.3, pos=(-0.5, 0.5), fillColor='white'),
                  visual.Rect(win, width=0.3, height=0.3, pos=(0.5, 0.5), fillColor='white')]

# Create text stimuli for the options
option_texts = [visual.TextStim(win, text='', pos=(-0.5, -0.5), color='black'),
                visual.TextStim(win, text='', pos=(0.5, -0.5), color='black'),
                visual.TextStim(win, text='', pos=(-0.5, 0.5), color='black'),
                visual.TextStim(win, text='', pos=(0.5, 0.5), color='black')]

# Create an image stimulus to display the current image
image_stimulus = visual.ImageStim(win)

# Create a window
win = visual.Window(size=(800, 600), color='black')

# Create clickable squares (polygons) for the emotion options with increased separation
option_squares = [visual.Rect(win, width=0.4, height=0.2, pos=(-0.6, -0.6), fillColor='white'),
                  visual.Rect(win, width=0.4, height=0.2, pos=(0.6, -0.6), fillColor='white'),
                  visual.Rect(win, width=0.4, height=0.2, pos=(-0.6, -0.9), fillColor='white'),
                  visual.Rect(win, width=0.4, height=0.2, pos=(0.6, -0.9), fillColor='white')]

# Create text stimuli for the options with increased separation
option_texts = [visual.TextStim(win, text='', pos=(-0.6, -0.6), color='black'),
                visual.TextStim(win, text='', pos=(0.6, -0.6), color='black'),
                visual.TextStim(win, text='', pos=(-0.6, -0.9), color='black'),
                visual.TextStim(win, text='', pos=(0.6, -0.9), color='black')]

# Create an image stimulus to display the current image
image_stimulus = visual.ImageStim(win)

# Experiment loop for 36 trials
for trial_num, current_image in enumerate(selected_images):
    # Set the image stimulus to the current image and scale it to full resolution
    image_stimulus.image = current_image
    print(f"Trial {trial_num + 1}: {current_image}")
    image_stimulus.size = (1.0, 1.0)  # Adjusting to fit the window while preserving the aspect ratio

    # Extract the correct emotion based on the third last character of the filename
    correct_emotion_key = os.path.basename(current_image)[-7]  # Adjust this if necessary
    
    # Check if the key exists in the emotion_map, otherwise skip the file
    if correct_emotion_key not in emotion_map:
        print(f"Warning: Unexpected emotion key '{correct_emotion_key}' in file {current_image}. Skipping this trial.")
        continue  # Skip this iteration if the key isn't valid

    correct_emotion = emotion_map[correct_emotion_key]

    # Shuffle emotion options and ensure the correct one is included
    random.seed(current_image)
    options = list(emotion_map.values())
    random.shuffle(options)
    
    if correct_emotion not in options:
        options[random.randint(0, 3)] = correct_emotion

    # Set the text for the clickable options below the image with more separation
    for i in range(4):
        option_texts[i].text = options[i]

    # Draw the image and options for the current trial
    image_stimulus.draw()
    for square, text in zip(option_squares, option_texts):
        square.draw()
        text.draw()
    
    win.flip()

    # Wait for a valid click response
    response = None
    while response is None:
        mouse = event.Mouse(win=win)
        if mouse.isPressedIn(option_squares[0]):
            response = option_texts[0].text
        elif mouse.isPressedIn(option_squares[1]):
            response = option_texts[1].text
        elif mouse.isPressedIn(option_squares[2]):
            response = option_texts[2].text
        elif mouse.isPressedIn(option_squares[3]):
            response = option_texts[3].text

    # Check if the participant's choice is correct
    is_correct = (response == correct_emotion)

    # Store the response data
    responses.append({
        'image': current_image,
        'correct': correct_emotion,
        'participant_choice': response,
        'accuracy': int(is_correct)
    })

    # Clear the event buffer to prevent unwanted key presses from carrying over
    event.clearEvents()

# End of experiment, generate the report
with open('results.txt', 'w') as f:
    f.write("Image,Correct Emotion,Participant Choice,Accuracy\n")
    for response in responses:
        f.write(f"{response['image']},{response['correct']},{response['participant_choice']},{response['accuracy']}\n")

# Close the window
win.close()
core.quit()