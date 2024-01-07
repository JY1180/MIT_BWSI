import math
import tkinter as tk
from tkPDFViewer import tkPDFViewer as pdf
from gameplay.paramedic import Paramedic
from gameplay.protector import Protector
from ui_elements.button_menu import ButtonMenu
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.clock import Clock
from endpoints.machine_interface import MachineInterface
from ui_elements.game_viewer import GameViewer
from ui_elements.machine_menu import MachineMenu
from os.path import join
import pygame
from pygame import mixer
import threading
from gameplay.enums import ActionCost
from ui_elements.instructions import Instructions
from endpoints.data_logger import DataLogger

stop_siren_event = threading.Event()


class UI(object):

    def __init__(self, data_parser, scorekeeper, data_fp, is_disable):
        #  Base window setup
        w, h = 1280, 800
        self.root = tk.Tk()
        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(str(w) + 'x' + str(h))
        self.root.resizable(False, False)
        self.logger = DataLogger()
        self.chose_suggest = False
        self.chose_info = False
        self.paramedic = Paramedic(self.root)
        self.protector = Protector(self.root)
        self.humanoid = data_parser.get_random()
        self.used_paramedic = False
        self.used_protector = False
        if not is_disable:
            self.machine_interface = MachineInterface(self.root, w, h)

        def playBlood():
            mixer.init()
            pygame.init()
            mixer.music.load("blood_sound_trimmed.wav")
            mixer.music.play()

        #  Add buttons and logo
        user_buttons = [("Skip", lambda: [scorekeeper.skip(self.humanoid),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper, ActionCost.SKIP),
                                          scorekeeper.skip_update_morality(self.humanoid)]),
                        ("Squish", lambda: [playBlood(),
                                            scorekeeper.squish(self.humanoid),
                                            self.inc_count(True),
                                            self.update_ui(scorekeeper),
                                            self.get_next(
                                                data_fp,
                                                data_parser,
                                                scorekeeper, ActionCost.SQUISH),
                                            scorekeeper.squish_update_morality(self.humanoid)]),
                        ("Save", lambda: [scorekeeper.save(self.humanoid),
                                          self.cure(self.humanoid, self.paramedic, scorekeeper),
                                          self.protect(self.humanoid, self.protector, scorekeeper),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper, ActionCost.SAVE),
                                          scorekeeper.save_update_morality(self.humanoid)]),
                        ("Scram", lambda: [scorekeeper.scram_update_morality(),
                                           scorekeeper.scram(),
                                           self.inc_count(False),
                                           self.update_ui(scorekeeper),
                                           self.get_next(
                                               data_fp,
                                               data_parser,
                                               scorekeeper, ActionCost.SCRAM)]),
                        ("Paramedic", lambda: [scorekeeper.addtoifparamedic(), self.display_paramedic(scorekeeper)]),
                        ("Protector", lambda: [scorekeeper.addtoifprotector(), self.display_protector(scorekeeper)])]

        self.button_menu = ButtonMenu(self.root, user_buttons)

        instruction_button = ["Instructions", lambda: [self.open_instructions(self.root)]]
        self.instructions = Instructions(self.root, instruction_button)

        if not is_disable:
            machine_buttons = [("Suggest", lambda: [scorekeeper.addtosuggestcount(),
                                                    self.machine_interface.suggest(self.humanoid, scorekeeper),
                                                    self.update_ui(scorekeeper), self.suggest_chosen()
                                                    ]),
                               ("Act", lambda: [scorekeeper.addtoactcount(),
                                                self.machine_interface.act(scorekeeper, self.humanoid),
                                                self.update_ui(scorekeeper),
                                                self.get_next(
                                                    data_fp,
                                                    data_parser,
                                                    scorekeeper, ActionCost)]),
                               ("Info", lambda: [scorekeeper.addtoinfocount(),
                                                 self.machine_interface.humanoid_info(scorekeeper, self.humanoid),
                                                 self.update_ui(scorekeeper), self.info_chosen()])]

            self.machine_menu = MachineMenu(self.root, machine_buttons)

        #  Display central photo
        self.game_viewer = GameViewer(self.root, 0, w, h, data_fp, self.humanoid)  # set filter count to 0
        self.root.bind("<Delete>", self.game_viewer.delete_photo)

        # Display the countdown
        init_h = (12 - (math.floor(scorekeeper.remaining_time / 60.0)))
        init_m = 60 - (scorekeeper.remaining_time % 60)
        self.clock = Clock(self.root, w, h, init_h, init_m)

        # Display ambulance capacity
        self.capacity_meter = CapacityMeter(self.root, w, h, data_parser.capacity)

        self.root.mainloop()

    def display_paramedic(self, scorekeeper):
        self.used_paramedic = True
        scorekeeper.has_paramedic = True
        self.button_menu.buttons[4].pack_forget()  # makes button disappear
        self.button_menu.buttons[5].pack_forget()  # makes button disappear
        self.paramedic.render_serum()  # creates serum bar
        scorekeeper.ambulance["paramedic"] = 1  # takes up one space in ambulance
        self.capacity_meter.canvas.itemconfig(self.capacity_meter.units[-1], fill="lightblue", stipple="")  # sky blue

    def cure(self, humanoid, paramedic, scorekeeper):
        if humanoid.is_zombie():  # can only cure if zombie
            if self.used_paramedic and paramedic.serum_count > 0:
                if paramedic.update_serum() > 0.5:  # 50% chance of curing zombie
                    scorekeeper.ambulance["healthy"] += 1
                    scorekeeper.morality_score *= 1.2
                else:
                    scorekeeper.ambulance["zombie"] += 1
                    scorekeeper.morality_score *= 0.8
                paramedic.update_fill(paramedic.serum_count)
            elif not self.used_protector and self.used_paramedic:
                scorekeeper.ambulance["zombie"] += 1  # adds normally
            elif not self.used_protector and not self.used_paramedic:
                scorekeeper.ambulance["zombie"] += 1  # adds normally

    def display_protector(self, scorekeeper):
        self.used_protector = True
        self.button_menu.buttons[4].pack_forget()  # makes button disappear
        self.button_menu.buttons[5].pack_forget()  # makes button disappear
        self.protector.render_lives()
        scorekeeper.ambulance["protector"] = 1  # takes up one space in ambulance
        self.capacity_meter.canvas.itemconfig(self.capacity_meter.units[-1], fill="green", stipple="")

    def protect(self, humanoid, protector, scorekeeper):
        if humanoid.is_zombie():  # can only cure if zombie
            if self.used_protector:
                if protector.kill() > 0:
                    scorekeeper.ambulance["corpse"] += 1
                else:
                    scorekeeper.ambulance["zombie"] += 1
                protector.update_fill(protector.health)

    def open_instructions(self, root):
        instructions_window = tk.Toplevel(root)
        instructions_window.title("Instructions")
        open_pdf = pdf.ShowPdf().pdf_view(instructions_window, pdf_location=r"game_instructions.pdf", width=85,
                                          height=50)
        open_pdf.pack()
        instructions_window.mainloop()

    def inc_count(self, show_filter):
        if show_filter:  # if filter is on
            self.game_viewer.count += 1
        else:
            self.game_viewer.count = 0  # reset filter

    def update_ui(self, scorekeeper):
        h = (12 - (math.floor(scorekeeper.remaining_time / 60.0)))
        m = 60 - (scorekeeper.remaining_time % 60)
        self.clock.update_time(h, m)
        if self.used_paramedic:  # if paramedic is activated
            self.capacity_meter.update_fill(scorekeeper.get_current_capacity() - 1)  # excludes paramedic index
            if self.paramedic.serum_count == 0:
                self.capacity_meter.canvas.itemconfig(self.capacity_meter.units[-1], fill="", stipple="")
                # permanently takes up space
            else:
                self.capacity_meter.canvas.itemconfig(self.capacity_meter.units[-1], fill="lightblue", stipple="")
                # visually changes paramedic square
        elif self.used_protector:
            self.capacity_meter.update_fill(scorekeeper.get_current_capacity() - 1)
            if self.protector.health == 0:
                self.capacity_meter.canvas.itemconfig(self.capacity_meter.units[-1], fill="", stipple="")
                # permanently takes up space
            else:
                self.capacity_meter.canvas.itemconfig(self.capacity_meter.units[-1], fill="green", stipple="")
                # visually changes paramedic square
        else:
            self.capacity_meter.update_fill(scorekeeper.get_current_capacity())
            self.button_menu.buttons[4].config(state="normal")  # shows button after scram
            self.button_menu.buttons[5].config(state="normal")  # shows button after scram

    def on_resize(self, event):
        w, h = 0.6 * self.root.winfo_width(), 0.7 * self.root.winfo_height()
        self.game_viewer.canvas.config(width=w, height=h)

    def suggest_chosen(self):
        self.chose_suggest = True

    def info_chosen(self):
        self.chose_info = True

    stop_siren_event = threading.Event()

    def playSiren():

        mixer.init()
        pygame.init()

        siren_sound = pygame.mixer.Sound("AmazingMusic.mp3")

        siren_channel = siren_sound.play(loops=-1)

        stop_siren_event.wait()
        siren_channel.stop()

    siren_thread = threading.Thread(target=playSiren)
    siren_thread.daemon = True
    siren_thread.start()

    def get_next(self, data_fp, data_parser, scorekeeper, actiontype):
        remaining = len(data_parser.unvisited)
        zombie_capacity_reached = scorekeeper.get_zombie_count()
        state, action = self.machine_interface.get_model_suggestion(self.humanoid,
                                                                    scorekeeper.at_capacity())

        # fixed bug if you
        # don't suggest before: wrong action
        if action == actiontype or actiontype is None:  # if user action matches machine
            scorekeeper.addtocorrectmoves()

        self.logger.add_data(actiontype, scorekeeper.get_current_capacity(), self.chose_suggest, action,
                             self.chose_info, state,
                             self.used_paramedic, self.used_protector, self.game_viewer.count)
        self.chose_suggest = False
        self.chose_info = False

        # Ran out of humanoids? Disable skip/save/squish

        if not scorekeeper.at_capacity():
            scorekeeper.add_action()

        if remaining == 0 or scorekeeper.remaining_time <= 0 or zombie_capacity_reached:
            self.capacity_meter.update_fill(0)
            self.game_viewer.delete_photo(None)
            self.logger.save_player_data_to_csv("player_data.csv")
            self.game_viewer.display_score(scorekeeper.get_score(), scorekeeper)
            stop_siren_event.set()

        else:
            humanoid = data_parser.get_random()
            # Update visual display
            self.humanoid = humanoid
            fp = join(data_fp, self.humanoid.fp)
            self.game_viewer.create_photo(fp)

        # Disable button(s) if options are no longer possible

        self.machine_menu.disable_buttons(scorekeeper.remaining_time, scorekeeper.at_capacity(),
                                          zombie_capacity_reached)
        self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity(),
                                         zombie_capacity_reached)
