import os
import json
import shelve
import ttkbootstrap as ttk
import ttkbootstrap.widgets.scrolled as ttk_scrolled
import tkinter as tk
import tkinter.filedialog as dialog
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk


# No matter what, the application works in it's own directory 
# - this is one file script with files associated with it and
# there is no way it can be run with a different working directory.
os.chdir(os.path.dirname(__file__))


pads = {
    "padx": 4,
    "pady": 4,
}


building_manager = None # For GLOBAL USAGE
SHELVE_FILENAME = "buildings_manager.dat"

STATUS_BAR_INITIAL_TEXT = "-" * 100

class BuildingsManager(tk.Tk):

    def __init__(self):
        super().__init__()
        
        global building_manager
        building_manager = self # Set the GLOBAL USAGE reference

        # Resize the window to encompass all buildings:
        self.geometry("1440x900")

        
        self.title("Buildings Manager")

        ## Instance variables: ----------------------------------------------------------------------------------
        self.root_path = "" # <--- ### The ROOT FOLDER OF THE PROJECT. ###
        self.open_json = ""
        ## Reading root path from shelve:
        with shelve.open(SHELVE_FILENAME) as db:
            if "root_path" in db: self.root_path = db["root_path"]
            if "open_json" in db: self.last_loaded_json_file = db["open_json"]
        

        self.cols = 5 #                                    <-- COLUMNS OF BUILDINGS to display, other are rows 
        self.buildings_frames : list[BuildingFrame] = [] # <-- BUILDINGS FRAMES containing the data about buildings.

        ###### FRAMES CREATION calls #####
        self.properties_frame : PropertiesFrame = None

        # - UPPER FRAME
        self.upper_frame = ttk.Frame(self) 
        self.create_buttons_frame()     # BUTTONS
        self.create_buildings_frame()   # BUILDINGS
        self.create_properites_frame() # PROPERTIES
        self.upper_frame.pack(expand=True, fill=tk.BOTH, **pads)

        # - LOWER FRAME
        self.lower_frame = ttk.LabelFrame(self, text="Status Bar")
        self.create_status_bar()
        self.lower_frame.pack(fill=tk.X, **pads)

        # // Instantly issue a warning if root path is not set // #
        if not self.root_path:
            self.status_bar["text"] = "Please select a correct project root path for the buildings manager"
            self.status_bar.configure(bootstyle="danger")

        self.mainloop()


    ############## START OF FRAMES CREATION methods ##

    def create_buttons_frame(self):
        ''' Create a BUTTONS FRAME that sits at the left side of the UI '''
        # Project root path:
        self.buttons_frame   = ttk.LabelFrame(self.upper_frame, text="Actions")
        self.buttons_frame.pack(expand=False, fill=tk.BOTH, side=tk.LEFT, **pads)
        
        # Buildings loading and saving:
        self.set_project_root_folder_button = ttk.Button(self.buttons_frame, text="Set project root folder...", bootstyle="danger",
            command=self.set_project_root_folder)  # <-- BUTTON for setting project root folder for relative paths evaluation.
        self.set_project_root_folder_button.pack(fill=tk.BOTH, **pads)

        self.open_buildings_folder_button = ttk.Button(self.buttons_frame, text="Open Folder with images...",
            command=self.open_buildings_folder) # <-- BUTTON for opening buildings images FROM FOLDER containing those images.
        self.open_buildings_folder_button.pack(fill=tk.BOTH, **pads)

        self.save_buildings_button = ttk.Button(self.buttons_frame, text="Save Buildings to json...", 
            command=self.save_buildings_file_json) # <-- BUTTON for saving images into JSON file.
        self.save_buildings_button.pack(fill=tk.BOTH, **pads)

        self.load_buildings_json_button = ttk.Button(self.buttons_frame, text="Load Buildings from json...",
            command=self.load_buildings_file_json) # <-- BUTTON for loading buildings from JSON file.
        self.load_buildings_json_button.pack(fill=tk.BOTH, **pads)

        # Buildings adding:
        self.add_building_image = ttk.PhotoImage(file="add-building.png")
        self.add_building_button = ttk.Button(self.buttons_frame, image=self.add_building_image, command=self.add_building)
        self.add_building_button.pack(**pads)

        # Simple save
        self.save_button = ttk.Button(self.buttons_frame, text="Save", command=self.save, bootstyle="warning")
        self.save_button.pack(**pads)


    def create_buildings_frame(self):
        ''' Create a BUILDINGS FRAME that is on the right side of the UI '''
        self.buildings_frame = ttk_scrolled.ScrolledFrame(self.upper_frame)
        self.buildings_frame.pack( expand=True, fill=tk.BOTH, side=tk.LEFT, **pads)

    def create_properites_frame(self):
        project_root = os.path.dirname(__file__)
        empty_image = "building1.png"
        self.properties_frame = PropertiesFrame(self.upper_frame, project_root, empty_image, "Unnamed", 0)
        self.properties_frame.pack(fill=tk.Y, side=tk.LEFT, **pads)

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.lower_frame, text=STATUS_BAR_INITIAL_TEXT, bootstyle="primary")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, **pads)

    ## END OF FRAMES CREATION ###############


    def set_project_root_folder(self):
        self.root_path = dialog.askdirectory()
        with shelve.open(SHELVE_FILENAME) as db:
            if self.root_path: 
                db["root_path"] = self.root_path
                self.status_bar["text"] = STATUS_BAR_INITIAL_TEXT
                self.status_bar.configure(bootstyle="primary")

    

    def open_buildings_folder(self):
        ''' LOADING from building images inside directory '''
        if not self.root_path: return
        
        directory = dialog.askdirectory()
        if directory: self.read_buildings_directory(directory)


    
    def read_buildings_directory(self, directory):
        ''' READ from a directory after loading it '''
        if not self.root_path: return

        files : list[str] = os.listdir(directory)
        
        column = 0
        row = 0
        for file in files:
            if not file.endswith(".png"): continue # <-- Don't load any other files than PNG!!!!

            full_path = directory + os.sep + file
            rel_path = os.path.relpath(full_path, self.root_path)
            building_frame = BuildingFrame(self.buildings_frame, full_path, rel_path) 
            building_frame.grid(column=column, row=row, sticky=tk.NSEW, **pads)
            self.buildings_frames.append(building_frame) # <-- Appending to building frame the new entry loaded building.
            column += 1
            if column != 0 and column % self.cols == 0:
                column = 0
                row += 1
            

    ######################## THE MASTER SAVING AND LOADING FUNCTION TO/FROM FILE #############################
    #                                                __  ___ _                                               #
    #                                               |   \ o | |                                              #
    #                                               |    \_|  |                                              #
    #                                               |  _____  |                                              #
    #                                               |__|_~_|__|                                              #
    #                                                                                                        #
    ##########################################################################################################
    def save_buildings_file_json(self) -> str:
        ''' SAVING to json, return FILENAME where save occured '''
        if not self.root_path: return

        # We can't save if nothing is loaded or added
        if len(self.buildings_frames) == 0: 
            self.status_bar.configure(bootstyle="danger")
            self.status_bar["text"] = "NOTHING TO SAVE"
            self.after(3000, self.revert_status_bar)
            return

        ### Iterate over the BUILDINGS FRAMES and append data to BUILDINGS variable ###

        buildings = self.get_buildings_array()

        output = json.dumps(buildings, indent=4) # <-- Output the json to string and save it later on.
        
        output_file = dialog.asksaveasfile("w", defaultextension="txt")
        if not output_file: return None
        output_file.write(output)
        output_file.close()

        return output_file.name


    def get_buildings_array(self):
        buildings = []
        for frame in self.buildings_frames:
            building = {}
            building["path"]       = frame.file_rel_path.cget("text")
            building["name"]       = frame.name_var.get()
            building["population"] = frame.population_var.get()
            buildings.append(building)
        return buildings


    def load_buildings_file_json(self):
        ''' Read the json file containing data about buildings and load the into the BUILDINGS FRAME component'''
        if not self.root_path: return

        json_file = dialog.askopenfile(filetypes=[("Buildings file", "*.json")])
        if json_file:
            # If something was loaded - remove existing buildings
            for building_frame in self.buildings_frames:
                building_frame.grid_forget()
            self.buildings_frames.clear()

            # Now do the load:
            self.open_json = json_file.name
            with shelve.open(SHELVE_FILENAME) as db:
                db["open_json"] = json_file.name
            
            contents = json_file.read()

            buildings = json.loads(contents)
            column = 0
            row = 0
            missing_files = []
            for building in buildings:
                file_name     = self.root_path + os.sep + building["path"]
                file_rel_path = building["path"]
                building_name = building["name"]
                building_pop  = building["population"]
                try:
                    frame = BuildingFrame(self.buildings_frame, file_name, file_rel_path, building_name, building_pop)
                    self.buildings_frames.append(frame)
                    frame.grid(column=column, row=row)

                    column += 1
                    if column != 0 and column % self.cols == 0:
                        column = 0
                        row += 1        
                except FileNotFoundError:
                    missing_files.append(file_name)

            if len(missing_files) > 0:
                messagebox.showerror("Missing files", "\n".join(missing_files))
            

    #########
    #   |   #
    # --+-- # Adding buildings
    #   |   #
    #########
    def add_building(self):
        if not self.root_path: return

        # Ask for the image:
        building_image = dialog.askopenfile(filetypes=[("Png Image", "*.png")])
        building_file_path = building_image.name
        
        if not building_image: return
        # .. for the name of building:
        building_name = simpledialog.askstring("Building name", prompt="What is the building name?")
        if not building_name: return
        # .. and fot it's population:
        building_population = simpledialog.askinteger("Building population", "What is it's population")
        if not building_population: return

        # At this point we got the required informations,
        # so we can put the new building into buildings_frame
        frame = BuildingFrame(
            self.buildings_frame, 
            building_file_path, 
            os.path.relpath(building_file_path, self.root_path), 
            building_name, building_population)
        self.buildings_frames.append(frame)
        row = len(self.buildings_frames) // self.cols
        column = len(self.buildings_frames) % self.cols - 1
        frame.grid(column=column, row=row, **pads)

        
    #############
    # Saving - without file location asking
    # -----------
    # |   \ o | |
    # |    \_|  |
    # |  _____  |
    # |__|___|__|
    #
    ###########
    def save(self):
        ''' Perform save on currently loaded json file'''
        buildings = self.get_buildings_array()

        if not self.open_json: 
            self.open_json = self.save_buildings_file_json()
            if not self.open_json: return
            
            # -- Open json path available:
            with shelve.open(SHELVE_FILENAME) as db:
                db["open_json"] = self.open_json
            
        f = open(self.open_json, "w")
        f.write(json.dumps(buildings, indent=4))
        f.close()



    def revert_status_bar(self):
        self.status_bar.config(bootstyle="primary")
        self.status_bar['text'] = STATUS_BAR_INITIAL_TEXT


class BuildingFrame(ttk.Frame):
    def __init__(self, master, image_full_path, rel_path, name = "None", population = 0):
        super().__init__(master, borderwidth=2)

        MAX_SIZE = 120

        ## Image resizing:
        # -----------
        # |\       /|
        # | v_____v | The resizing is done when the image size is larger
        # | |     | | than MAX_SIZE pixels ^^^ (width or height).
        # | ^-----^ |
        # |/       \|
        # -----------

        pil_image = Image.open(image_full_path)
        w, h = pil_image.size

        def do_resize(w, h):
            return pil_image.resize((w, h), resample=Image.Resampling.NEAREST)

        if w > MAX_SIZE: pil_image = do_resize(MAX_SIZE, h)
        if h > MAX_SIZE: pil_image = do_resize(w, MAX_SIZE)

        image_tk = ImageTk.PhotoImage(pil_image)
        self.image_tk = image_tk # <-- Need to keep the reference for images to be displayed.
        
        # The component:
        # - Image
        # - Path
        # - Name (inferred)
        # - Population
        # - Data
        
        top_separator = ttk.Separator(self)
        top_separator.pack(expand=True, fill=tk.X)

        filler = tk.Frame(self)
        filler.pack(expand=True, fill=tk.BOTH)

        # -------------- The component logic -------------- #
        self.image_path = image_full_path

        self.image = ttk.Label(self, image=image_tk)
        self.image.pack(expand=True, **pads)

        self.image.bind("<Double 1>", self.show_in_properties)
        
        self.file_rel_path = ttk.Label(self, text=rel_path)
        self.file_rel_path.pack(**pads)

        ## Entries frame - for name of the building and it's population:
        entries_frame = ttk.Frame(self) 

        label_name = ttk.Label(entries_frame, text="Name:")
        label_name.grid(column=0, row= 0, **pads)
        self.name_var = ttk.StringVar(value=name) # <-- NAME entry.
        self.name = ttk.Entry(entries_frame, textvariable=self.name_var)
        self.name.grid(column=1, row=0)

        label_population = ttk.Label(entries_frame, text="Pop:")
        label_population.grid(column=0, row=1, **pads)
        self.population_var = ttk.IntVar(value=population) # <-- POPULATION entry.
        self.population = ttk.Entry(entries_frame, textvariable=self.population_var)
        self.population.grid(column=1, row=1)

        entries_frame.pack(**pads)

        # End of entries frame

        filler = tk.Frame(self)
        filler.pack(expand=True, fill=tk.BOTH)

        # DELETE BUTTON:
        self.delete_button = ttk.Button(self, command=self.delete, text="delete", bootstyle="danger")
        self.delete_button.pack()


    def delete(self):
        self.grid_forget()
        building_manager.buildings_frames.remove(self)

    
    def show_in_properties(self, event):
        building_manager.properties_frame.set(
            building_manager.root_path,
            self.file_rel_path.cget("text"),
            self.name_var.get(),
            self.population_var.get()
        )

        
class PropertiesFrame(ttk.LabelFrame):

    # PROPERTIES PANEL to the right side of the manager UI. 
    #
    # |---------------------|
    # | btns | bldgs |/prps/|
    # |      |       |/HERE/|
    # |      |       |//////|
    # |      |       |//////|
    # |---------------------|

    def __init__(self, master, project_root, rel_path, building_name = "Unnamed", building_pop = 0):
        super().__init__(master)
        self.building_image = None # BUILDING IMAGE in the properties panel 
        self.basename       = None # BASENAME WIDGETH with the base name of the image (e.g. "building1.png")
        self.rel_path       = None # RELATIVE PATH to project's root folder
        self.building_name  = None # BUILDING NAME 
        self.building_pop   = None # BUILDING POPULATION
        
        ## TOP LABEL ##
        label = tk.Label(self, text="PROPERTIES")
        label.pack(**pads)

        self.image = ImageTk.PhotoImage(Image.open(project_root + os.sep + rel_path)) # <-- Keep it for reference counting.
        self.building_image = ttk.Label(self, image=self.image)
        self.building_image.pack(**pads)

        self.rel_path = ttk.Label(self, text=rel_path)
        self.rel_path.pack(**pads)

        # Entry input data frame - START ###

        entry_frame = ttk.Frame(self) # Inner frame for the properties - describes the selected entry
        
        name_label = ttk.Label(entry_frame, text="Name:")
        name_label.grid(column=0, row=0, **pads)
        self.name_var = ttk.StringVar(value=building_name)
        self.building_name = ttk.Entry(entry_frame, textvariable=self.name_var)
        self.building_name.grid(column=1, row=0, **pads)

        pop_label = ttk.Label(entry_frame, text="Pop:")
        pop_label.grid(column=0, row=1)
        self.pop_var = ttk.StringVar(value=building_pop)
        self.building_pop = ttk.Entry(entry_frame, textvariable=self.pop_var)
        self.building_pop.grid(column=1, row=1, **pads)

        entry_frame.pack()

        # Entry input data frame - END ###


    def set(self, project_root, relpath, building_name, building_pop):
        image = ImageTk.PhotoImage(Image.open(project_root + os.sep + relpath)) # <-- Keep it for reference counting.
        self.building_image["image"] = image
        self.name_var.set(building_name)
        self.pop_var.set(building_pop)

if __name__ == "__main__":
    BuildingsManager()
    