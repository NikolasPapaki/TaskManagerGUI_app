import customtkinter as ctk
import inspect
from Frames import *
import re
import os
import json

def button_formating(text):
    """Add spaces before uppercase letters in camel case strings."""
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text.replace('Frame', ''))

class ApplicationInterface:
    def __init__(self, parent):
        self.parent = parent

        # Load settings and set current theme
        self.settings = self.load_settings()
        current_theme = self.settings.get("theme", "dark")  # Default to "dark" if no theme is found
        ctk.set_appearance_mode(current_theme)

        # Determine the position of the sidebar
        self.sidebar_side = self.settings.get("sidebar_side", "left").lower()
        self.sidebar_width = 250

        # Create the sidebar frame with the specified width
        self.sidebar = ctk.CTkFrame(self.parent, width=self.sidebar_width)

        # Create the main content area to take the remaining space
        self.content_area = ctk.CTkFrame(self.parent)

        # Adjust the packing of sidebar and content area based on the sidebar side
        self.update_sidebar_position()

        # Set the sidebar's minimum and maximum width to prevent resizing
        self.sidebar.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

        # Create buttons for the sidebar in a custom order
        self.create_sidebar_buttons()

        # Initialize the first frame
        self.current_frame = None
        self.show_frame(HomeFrame)

    def load_settings(self):
        """Load settings from the JSON file, or return an empty dictionary if the file does not exist."""
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                return json.load(file)
        return {}

    def update_sidebar_position(self):
        """Update the packing order of the sidebar and content area."""
        if self.sidebar_side == "left":
            self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
            self.content_area.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)
        elif self.sidebar_side == "right":
            self.sidebar.pack(side=ctk.RIGHT, fill=ctk.Y)
            self.content_area.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        else:
            raise ValueError(f"Invalid value for sidebar_side: {self.sidebar_side}. Use 'left' or 'right'.")

    def create_sidebar_buttons(self):
        # Create a list to hold the button details
        buttons = []

        # Retrieve all classes from the frames module
        for name, obj in inspect.getmembers(inspect.getmodule(inspect.currentframe())):
            if inspect.isclass(obj) and issubclass(obj, ctk.CTkFrame):
                buttons.append((name, obj))

        # Sort the buttons based on the ORDER constant
        buttons.sort(key=lambda x: getattr(x[1], 'ORDER', float('inf')))  # Use ORDER attribute for sorting

        # Create buttons based on the sorted list
        for (text, frame_class) in buttons:
            button = ctk.CTkButton(self.sidebar, text=button_formating(text), command=lambda f=frame_class: self.show_frame(f))
            button.pack(pady=5, padx=10, fill=ctk.X)

    def show_frame(self, frame_class):
        # Destroy the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Create a new frame and display it
        self.current_frame = frame_class(self.content_area)
        self.current_frame.pack(fill=ctk.BOTH, expand=True)

