#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 17:23:03 2018

@author: Jakub Popielarz
"""

import random
try:
    import tkinter
    from tkinter import filedialog
except ImportError:
    print("Python 3 and tkinter are required to run this program.")
    exiting = input("[e]xit")
    while(exiting != "E" ):
        exiting = input("[e]xit")

class GameOfLife(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

        self.game_on = False

        self.title("Game of life")
        try:
            gol_icon = tkinter.PhotoImage(file="GoL_icon.gif")
            self.tk.call("wm", "iconphoto", self._w, gol_icon)
            self.iconphoto = gol_icon
        except tkinter.TclError:
            pass

        self.resizable(0, 0)

        self.start_size = 50
        self.default_size = self.set_size = self.start_size
        self.default_rand = self.set_rand = True
        self.default_time = self.set_time = 300
        self.default_conditions = self.set_conditions = {'b': [3], 's': [2, 3]}
        self.cell_size = 10

        self.container = tkinter.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.previous_screen = Menu

        self.screens = {}

        self.screens[Menu] = Menu(self.container, self)
        self.screens[Game] = Game(self.container, self, self.set_size,
                                  self.set_rand, self.set_time,
                                  self.set_conditions)
        self.screens[Settings] = Settings(self.container, self,
                                          self.screens[Game])
        self.screens[About] = About(self.container, self)

        for screen in self.screens:
            self.screens[screen].grid(row=0, column=0, sticky="news")

        self.show_screen(Menu, Menu)

    def show_screen(self, screen, from_screen):
        self.previous_screen = from_screen

        if screen == Settings:
            self.screens[screen].mode(self.previous_screen)

        if self.game_on:
            self.screens[Menu].continue_button.configure(state="normal")

        frame = self.screens[screen]
        frame.tkraise()

class Menu(tkinter.Frame):
    def __init__(self, parent, controller):
        self.controller = controller

        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text="The Game of Life", font=(None, 40))
        label.pack()

        new_game_button = tkinter.Button(self, text="New game",
                                         command=self.new_game)
        self.continue_button = tkinter.Button(self, text="Continue",
                                              state="disabled",
                                              command=lambda:
                                                  controller.show_screen(Game, Menu))
        settings_button = tkinter.Button(self, text="Settings",
                                         command=self.open_settings)
        about_button = tkinter.Button(self, text="About",
                                      command=lambda:
                                          controller.show_screen(About, Menu))
        exit_button = tkinter.Button(self, text="Exit",
                                     command=controller.destroy)
        new_game_button.pack(fill="x")
        self.continue_button.pack(fill="x")
        settings_button.pack(fill="x")
        about_button.pack(fill="x")
        exit_button.pack(fill="x")

    def new_game(self):
        self.controller.game_on = True

        self.controller.screens[Game].grid_remove()
        self.controller.screens[Game].__init__(self.controller.container,
                                               self.controller,
                                               self.controller.set_size,
                                               self.controller.set_rand,
                                               self.controller.set_time,
                                               self.controller.set_conditions)
        self.controller.screens[Game].grid(row=0, column=0, sticky="news")
        self.controller.show_screen(Game, Menu)

    def open_settings(self):
        self.controller.screens[Settings].grid_remove()
        self.controller.screens[Settings].__init__(self.controller.container,
                                                   self.controller,
                                                   self.controller.screens[Game])
        self.controller.screens[Settings].grid(row=0, column=0, sticky="news")
        self.controller.show_screen(Settings, Menu)

class About(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        frame_size = 10
        about_frame = tkinter.Frame(self, width=frame_size)
        about_frame.grid_propagate(False)
        about_frame.pack(side="top", fill="both", expand=True)


        about_frame.grid_rowconfigure(0, weight=1)
        about_frame.grid_columnconfigure(0, weight=1)

        about = tkinter.Text(about_frame, wrap="word")
        scroll = tkinter.Scrollbar(about_frame, command=about.yview)
        about.configure(yscrollcommand=scroll.set)

        scroll.grid(column=1, sticky="ns")
        about.grid(row=0, column=0, sticky="news")

        try:
            with open("about.txt") as about_file:
                text = about_file.read()
        except FileNotFoundError:
            text = """About file not found. 
For info about Game Of Life visit https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life"""

        about.insert("insert", text)
        about.configure(state="disabled")

        menu_button = tkinter.Button(self, text="Back to menu",
                                     command=lambda:
                                         controller.show_screen(Menu, About))

        menu_button.pack(side="bottom", fill="x")

class Settings(tkinter.Frame):
    def __init__(self, parent, controller, game):
        tkinter.Frame.__init__(self, parent)

        self.controller = controller
        self.game = game

        self.time_ok = True
        self.born_ok = True
        self.survives_ok = True
        self.conditions_ok = False
        self.size_ok = True
        self.all_ok = False

        time_label_text = "Time between generations [milliseconds]:"
        self.time_label = tkinter.Label(self, text=time_label_text)
        self.time_entry = tkinter.Entry(self)
        self.time_entry.insert(0, self.game.time)

        self.time_label.grid(row=1, sticky=tkinter.E, columnspan=2)
        self.time_entry.grid(row=1, column=2)

        conditions_label_text = """
Separate numbers with a single coma (for example: '2,3')
Cells can have between 0 and 8 neighbours (inclusive)"""
        born_label_text = "Cell is born, if it's number of neighbours equals:"
        survives_label_text = "Cell survives, if it's number of neighbours equals:"
        self.conditions_label = tkinter.Label(self,
                                              text=conditions_label_text)
        self.born_label = tkinter.Label(self, text=born_label_text)
        self.born_entry = tkinter.Entry(self)
        self.born_entry.insert(0, ",".join(str(x) for x in self.game.conditions['b']))
        self.survives_label = tkinter.Label(self, text=survives_label_text)
        self.survives_entry = tkinter.Entry(self)
        self.survives_entry.insert(0, ",".join(str(x) for x in self.game.conditions['s']))

        self.conditions_label.grid(row=2, columnspan=3)
        self.born_label.grid(row=3, sticky=tkinter.E, columnspan=2)
        self.born_entry.grid(row=3, column=2)
        self.survives_label.grid(row=4, sticky=tkinter.E, columnspan=2)
        self.survives_entry.grid(row=4, column=2)

        tkinter.Label(self, text="").grid(row=5)

        self.size_label = tkinter.Label(self,
                                        text="Number of cells in a row/column (min. 1):")
        self.size_entry = tkinter.Entry(self)
        self.size_entry.insert(0, self.game.size)

        self.size_label.grid(row=6, sticky=tkinter.E, columnspan=2)
        self.size_entry.grid(row=6, column=2)

        self.default_button = tkinter.Button(self, text="Restore defaults",
                                             command=self.restore_defaults)
        self.cancel_button = tkinter.Button(self, text="Cancel",
                                            command=lambda:
                                                controller.show_screen(
                                                    controller.previous_screen,
                                                    Settings))
        self.apply_buton = tkinter.Button(self, text="Apply",
                                          command=self.apply)

        self.default_button.grid(row=7)
        self.cancel_button.grid(row=7, column=1)
        self.apply_buton.grid(row=7, column=2)

        self.default_entry_fg_color = self.time_entry.cget("foreground")

    def mode(self, previous_screen):
        if previous_screen == Menu:
            self.default_button.config(state="disabled")
            disclaimer = tkinter.Label(self, foreground="cyan",
                                       text="Set defaults for current session")
            disclaimer.grid(row=0, columnspan=3)

    def validate_time(self):
        invalid = False
        if self.time_entry.get() != "":
            try:
                if int(self.time_entry.get()) <= 0:
                    invalid = True
            except ValueError:
                invalid = True
        if invalid:
            self.time_ok = False
            self.time_entry.config(foreground="red")
        else:
            self.time_ok = True
            self.time_entry.config(foreground=self.default_entry_fg_color)

    def validate_conditions(self):
        self.validate_born()
        self.validate_survives()

        if self.born_ok and self.survives_ok:
            self.conditions_ok = True

    def validate_born(self):
        invalid_born = False
        born_str = self.born_entry.get()

        if born_str != "":
            born_arr = born_str.split(",")

            try:
                for i in born_arr:
                    i = int(i)
                    if (i > 8) or (i < 0):
                        invalid_born = True
            except ValueError:
                invalid_born = True

        if invalid_born:
            self.born_ok = False
            self.born_entry.config(foreground="red")
        else:
            self.born_ok = True
            self.born_entry.config(foreground=self.default_entry_fg_color)

    def validate_survives(self):
        invalid_survives = False

        survives_str = self.survives_entry.get()

        if survives_str != "":
            survives_arr = survives_str.split(",")

            try:
                for i in survives_arr:
                    i = int(i)
                    if (i > 8) or (i < 0):
                        invalid_survives = True
            except ValueError:
                invalid_survives = True

        if invalid_survives:
            self.survives_ok = False
            self.survives_entry.config(foreground="red")
        else:
            self.survives_ok = True
            self.survives_entry.config(foreground=self.default_entry_fg_color)

    def validate_size(self):
        invalid = False
        if self.size_entry.get() != "":
            try:
                if int(self.size_entry.get()) <= 0:
                    invalid = True
            except ValueError:
                invalid = True
        if invalid:
            self.size_ok = False
            self.size_entry.config(foreground="red")
        else:
            self.size_ok = True
            self.size_entry.config(foreground=self.default_entry_fg_color)

    def validate(self):
        self.validate_time()
        self.validate_conditions()
        self.validate_size()

        if self.time_ok and self.conditions_ok and self.size_ok:
            self.all_ok = True

    def change_conditions(self):
        self.game.conditions = self.controller.set_conditions
        conditions_text = 'B' + "".join(str(x) for x in self.game.conditions['b'])
        conditions_text += '/S' + "".join(str(x) for x in self.game.conditions['s'])
        self.game.conditions_label.config(text=conditions_text)
        self.game.graphics = BoardGraphics(self.game.size, self.game.cell_size,
                                           self.game.rand, self.game.conditions)

    def change_size(self):
        tmp = self.game.graphics_array
        size = self.controller.set_size

        scrollregion_size = self.game.cell_size * self.controller.set_size

        self.game.canvas.config(scrollregion=(0, 0,
                                              scrollregion_size,
                                              scrollregion_size))

        if (self.controller.set_size > self.game.size and
                self.controller.set_size > self.controller.start_size):
            new_canvas_size = self.controller.start_size*self.controller.cell_size
            self.game.canvas.config(width=new_canvas_size,
                                    height=new_canvas_size)
        else:
            self.game.canvas.config(width=scrollregion_size,
                                    height=scrollregion_size)

        self.game.graphics = BoardGraphics(size, self.game.cell_size,
                                           0, self.game.conditions)
        self.game.graphics_array = self.game.graphics.create_board(self.game.canvas)

        if self.game.size < size:
            for i in range(self.game.size):
                for j in range(self.game.size):
                    if tmp[i][j].alive:
                        self.game.graphics_array[i][j].reset_cell(self.game.canvas)
                        self.game.graphics_array[i][j].breed_cell(self.game.canvas)
        else:
            for i in range(size):
                for j in range(size):
                    if tmp[i][j].alive:
                        self.game.graphics_array[i][j].reset_cell(self.game.canvas)
                        self.game.graphics_array[i][j].breed_cell(self.game.canvas)

        self.game.size = size

    def apply(self):
        self.validate()
        if self.all_ok:
            time = self.time_entry.get()
            if time != "":
                self.controller.set_time = self.game.time = int(time)
                if self.controller.previous_screen == Menu:
                    self.controller.default_time = int(time)

            born_arr = self.born_entry.get().split(",")
            survives_arr = self.survives_entry.get().split(",")

#           deduplicate elements in conditions arrays
            if born_arr != [""]:
                born_arr = list(set([int(x) for x in born_arr]))
            if survives_arr != [""]:
                survives_arr = list(set([int(x) for x in survives_arr]))

            born_arr.sort()
            survives_arr.sort()

            if born_arr != [""] and survives_arr != [""]:
                conditions = {'b': born_arr,
                              's': survives_arr}
                self.controller.set_conditions = conditions
                if self.controller.previous_screen == Menu:
                    self.controller.default_conditions = conditions
                self.change_conditions()

            size = self.size_entry.get()
            if size != "":
                self.controller.set_size = int(size)
                if self.controller.previous_screen == Menu:
                    self.controller.default_size = int(size)
                self.change_size()

            self.controller.show_screen(self.controller.previous_screen, Settings)

    def restore_defaults(self):
        self.time_entry.delete(0, tkinter.END)
        self.time_entry.insert(0, self.controller.default_time)

        self.born_entry.delete(0, tkinter.END)
        self.born_entry.insert(0, ",".join(str(x) for x in
                                           self.controller.default_conditions['b']))
        self.survives_entry.delete(0, tkinter.END)
        self.survives_entry.insert(0, ",".join(str(x) for x in
                                               self.controller.default_conditions['s']))

        self.size_entry.delete(0, tkinter.END)
        self.size_entry.insert(0, self.controller.default_size)

class Cell():
    def __init__(self, canvas, size, x0, y0):
        self.size = size
        self.x0 = x0
        self.y0 = y0

        self.alive_colour = 'black'
        self.dead_colour = 'white'
        self.outline_colour = 'cyan'

        self.alive = False
        self.kill = False
        self.bring_to_life = False
        self.object = self.create_cell(canvas)

    def create_cell(self, canvas):
        cell = canvas.create_rectangle(self.x0, self.y0,
                                       self.x0+self.size, self.y0+self.size,
                                       fill=self.dead_colour,
                                       outline=self.outline_colour)
        return cell

    def kill_cell(self, canvas):
        canvas.itemconfig(self.object, fill=self.dead_colour)
        self.bring_to_life = False
        self.kill = False
        self.alive = False

    def breed_cell(self, canvas):
        canvas.itemconfig(self.object, fill=self.alive_colour)
        self.bring_to_life = False
        self.kill = False
        self.alive = True

    def determine_state(self, canvas):
        if not self.alive and self.bring_to_life:
            self.breed_cell(canvas)
        elif self.alive and self.kill:
            self.kill_cell(canvas)

    def reset_cell(self, canvas):
        self.alive = False
        self.kill = False
        self.bring_to_life = False
        self.object = self.create_cell(canvas)

class BoardGraphics():
    def __init__(self, size, cell_size, rand, conditions):
        self.size = size
        self.cell_size = cell_size
        self.rand = rand
        self.conditions = conditions

    def create_board(self, canvas):
        board = []
        for i in range(self.size):
            board.append([])
            for j in range(self.size):
                cell_x0 = i * self.cell_size
                cell_y0 = j * self.cell_size
                cell = Cell(canvas, self.cell_size, cell_x0, cell_y0)
                board[i].append(cell)
        if self.rand:
            self.randomize_board(board, canvas)

        return board

    def randomize_board(self, board, canvas):
        for i in range(self.size):
            for j in range(self.size):
                tmp_rand = random.randint(0, 1)
                if tmp_rand == 1:
                    board[i][j].breed_cell(canvas)

        return board

    def neighbours(self, cell_x, cell_y, board):
        neigh = 0
        for i in range(cell_x-1, cell_x+2):
            for j in range(cell_y-1, cell_y+2):
                if i >= 0 and j >= 0:
                    try:
                        if board[i][j].alive:
                            neigh += 1
                    except IndexError:
                        continue
        if board[cell_x][cell_y].alive:
            neigh -= 1

        return neigh

    def check_cells(self, board):
        for i in range(self.size):
            for j in range(self.size):
                neigh = self.neighbours(i, j, board)
                if not board[i][j].alive and (
                        neigh in self.conditions['b']):
                    board[i][j].bring_to_life = True
                elif board[i][j].alive and (
                        neigh in self.conditions['s']):
                    continue
                else:
                    board[i][j].kill = True
        return board

    def update_board(self, board, canvas):
        for i in range(self.size):
            for j in range(self.size):
                board[i][j].determine_state(canvas)

        return board

    def clear_board(self, board, canvas):
        for i in board:
            for cell in i:
                cell.reset_cell(canvas)

        return board

class Game(tkinter.Frame):
    def __init__(self, parent, controller, size, rand,
                 time_interval, conditions):
        tkinter.Frame.__init__(self, parent)

        self.controller = controller

        self.default_size = self.size = size
        self.rand = rand
        self.default_time = self.time = time_interval
        self.default_conditions = self.conditions = conditions

        self.running = False

        self.cell_size = controller.cell_size

        self.step = 0

        self.button_frame = tkinter.Frame(self)
        self.button_frame.grid()
        self.button_names = ["Start", "Stop", "Clear", "Randomize",
                             "Save state to file", "Load state from file"]
        self.buttons = []
        self.upper_buttons = tkinter.Frame(self.button_frame)
        self.upper_buttons.grid()
        self.lower_buttons = tkinter.Frame(self.button_frame)
        self.lower_buttons.grid()
        self.create_buttons()

        try:
            settings_image = tkinter.PhotoImage(file="settings.gif")
            self.settings_button = tkinter.Button(self.upper_buttons,
                                                  image=settings_image,
                                                  command=self.settings_action)
            self.settings_button.image = settings_image
        except tkinter.TclError:
            self.settings_button = tkinter.Button(self.upper_buttons,
                                                  text="Settings",
                                                  command=self.settings_action)

        self.buttons.append(self.settings_button)
        self.menu_button = tkinter.Button(self.lower_buttons, text="Back to menu",
                                          command=lambda:
                                              controller.show_screen(Menu, Game))
        self.buttons.append(self.menu_button)

        upper_buttons_list = self.upper_buttons.winfo_children()

        for i in range(len(upper_buttons_list)):
            upper_buttons_list[i].grid(row=0, column=i)

        lower_buttons_list = self.lower_buttons.winfo_children()

        for i in range(len(lower_buttons_list)):
            lower_buttons_list[i].grid(row=0, column=i)

        self.settings_button.grid(row=0, column=5)
        self.menu_button.grid(row=0, column=5)

        self.generations = tkinter.Label(self, text='Generation: 0')
        self.generations.grid(row=2, sticky="W")

        conditions_text = 'B' + "".join(str(x) for x in self.conditions['b'])
        conditions_text += '/S' + "".join(str(x) for x in self.conditions['s'])
        self.conditions_label = tkinter.Label(self, text=conditions_text)
        self.conditions_label.grid(row=2, sticky="E")

        self.canvas_frame = tkinter.Frame(self)

        canvas_size = self.cell_size * controller.default_size
        scrollregion_size = self.cell_size * self.size

        self.canvas = tkinter.Canvas(self.canvas_frame, bd=0, bg='white',
                                     width=canvas_size,
                                     height=canvas_size)

        self.canvas.bind("<Button-1>", self.click_action)

        vertical_scroll = tkinter.Scrollbar(self.canvas_frame,
                                            orient="vertical",
                                            command=self.canvas.yview)
        horizontal_scroll = tkinter.Scrollbar(self.canvas_frame,
                                              orient="horizontal",
                                              command=self.canvas.xview)
        self.canvas.config(xscrollcommand=horizontal_scroll.set,
                           yscrollcommand=vertical_scroll.set)
        self.canvas.config(scrollregion=(0, 0, scrollregion_size,
                                         scrollregion_size))

        vertical_scroll.pack(side="right", fill="y")
        horizontal_scroll.pack(side="bottom", fill="x")
        self.canvas.pack()

        canvas_frame_size = controller.start_size * self.cell_size
        canvas_frame_size += int(vertical_scroll.cget("width")) + 5

        self.canvas_frame.config(width=canvas_frame_size, height=canvas_frame_size)
        self.canvas_frame.propagate(0)

        self.canvas_frame.grid()

        self.graphics = BoardGraphics(self.size, self.cell_size,
                                      self.rand, self.conditions)
        self.graphics_array = self.graphics.create_board(self.canvas)

        self.run(once=True)

    def click_action(self, event):
        if not self.running:
            cell_x = event.x // self.cell_size
            cell_y = event.y // self.cell_size

            if self.graphics_array[cell_x][cell_y].alive:
                self.graphics_array[cell_x][cell_y].kill = True
            else:
                self.graphics_array[cell_x][cell_y].bring_to_life = True

            self.graphics_array[cell_x][cell_y].determine_state(self.canvas)

    def create_buttons(self):
        button_width = 10
        for i in range(len(self.button_names)):
            action = self.return_button_action(self.button_names[i])
            if i // 4 == 0:
                button = tkinter.Button(self.upper_buttons,
                                        text=self.button_names[i],
                                        command=action)
                button.configure(width=button_width)
            else:
                button = tkinter.Button(self.lower_buttons,
                                        text=self.button_names[i],
                                        command=action)
                button.configure(width=2*button_width)
            self.buttons.append(button)
        self.update_buttons()

    def update_buttons(self):
        for i in self.buttons:
            if self.running:
                if i.cget('text') == "Stop":
                    i.configure(state="normal")
                else:
                    i.configure(state="disabled")
            else:
                if i.cget('text') == "Stop":
                    i.configure(state="disabled")
                else:
                    i.configure(state="normal")

    def return_button_action(self, name):
        if name == "Start":
            return self.start_action
        elif name == "Stop":
            return self.stop_action
        elif name == "Clear":
            return self.clear_action
        elif name == "Randomize":
            return self.randomize_action
        elif name == "Save state to file":
            return self.save_action
        elif name == "Load state from file":
            return self.load_action
        return self.empty

    def start_action(self):
        self.running = True
        self.update_buttons()
        self.run()

    def stop_action(self):
        self.running = False
        self.update_buttons()

    def clear_action(self):
        self.graphics_array = self.graphics.clear_board(self.graphics_array,
                                                        self.canvas)
        self.step = 0
        self.update_step()

    def randomize_action(self):
        self.clear_action()
        self.graphics_array = self.graphics.randomize_board(self.graphics_array,
                                                            self.canvas)

    def save_action(self):
        savefile = filedialog.asksaveasfile(mode="w", defaultextension=".txt",
                                            title="Save state to file",
                                            filetypes=[('Presets', '.txt'),
                                                       ('All files', '.*')])
        if savefile:
            conditions_str = ""
            for key in self.conditions:
                conditions_str += "." + key + "."
                conditions_str += ".".join(str(x) for x in self.conditions[key])
            savefile.write(conditions_str + "\n")

            savefile.write(str(self.size)+"\n")
            for i in range(self.size):
                for j in range(self.size):
                    if self.graphics_array[j][i].alive:
                        savefile.write("*")
                    else:
                        savefile.write(".")
                savefile.write("\n")

    def load_action(self):
        loadfile = filedialog.askopenfile(mode="r", title="Load state from file",
                                          filetypes=[('Presets', '.txt'),
                                                     ('All files', '.*')])
        if loadfile:
            self.clear_action()

            first_line = loadfile.readline()
            try:
                preset_size = int(first_line)
            except ValueError:
                first_line = first_line[:-1]
                conditions_arr = first_line.split(".")
                conditions_arr.pop(0)

                for i in range(len(conditions_arr)):
                    try:
                        conditions_arr[i] = int(conditions_arr[i])
                    except ValueError:
                        pass

                conditions_dict = {}

                for i in conditions_arr:
                    if isinstance(i, str):
                        key = i
                        conditions_dict[key] = []
                    else:
                        conditions_dict[key].append(i)

                preset_size = int(loadfile.readline())

            try:
                self.conditions = conditions_dict
            except UnboundLocalError:
                pass

            if preset_size > self.size:
                self.size = preset_size

            scrollregion_size = self.cell_size * self.size
            self.canvas.config(scrollregion=(0, 0,
                                             scrollregion_size,
                                             scrollregion_size))

            if (self.controller.set_size > self.size and
                    self.controller.set_size > self.controller.start_size):
                new_canvas_size = self.controller.start_size*self.controller.cell_size
                self.canvas.config(width=new_canvas_size,
                                   height=new_canvas_size)
            else:
                self.canvas.config(width=scrollregion_size,
                                   height=scrollregion_size)

            self.graphics = BoardGraphics(self.size, self.cell_size,
                                          0, self.conditions)
            self.graphics_array = self.graphics.create_board(self.canvas)

            i = 0

            for line in loadfile:
                for j in range(len(line[:-1])):
                    if line[j] == "*":
                        self.graphics_array[j][i].reset_cell(self.canvas)
                        self.graphics_array[j][i].breed_cell(self.canvas)
                    elif line[j] == ".":
                        self.graphics_array[j][i].reset_cell(self.canvas)
                        self.graphics_array[j][i].kill_cell(self.canvas)
                i += 1

    def settings_action(self):
        self.controller.screens[Settings].grid_remove()
        self.controller.screens[Settings].__init__(self.controller.container,
                                                   self.controller,
                                                   self.controller.screens[Game])
        self.controller.screens[Settings].grid(row=0, column=0, sticky="news")
        self.controller.show_screen(Settings, Game)

    def empty(self):
        pass

    def update_step(self):
        self.step += 1
        step_num = "{: >4}".format(str(self.step))
        str_step = "Generation: " + step_num
        self.generations.config(text=str_step)

    def run(self, once=False):
        if self.running or once:
            self.update_step()
            self.graphics_array = self.graphics.check_cells(self.graphics_array)
            self.graphics_array = self.graphics.update_board(self.graphics_array,
                                                             self.canvas)
            if not once:
                self.after(self.time, self.run)

if __name__ == "__main__":
    game_of_life = GameOfLife()
    game_of_life.mainloop()
