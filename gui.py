import os
import subprocess
import cv2
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from vmouse import VirtualMouse
from face.train import FaceDetectorTrainer
import face.utils as face_utils
from settings import settings, default_settings, saveSettings, saveDefaultSettings

ctk.set_appearance_mode('System')
# ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')

FONT = ('Helvetica', 14)
FINGERS = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

class Grid(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = 'transparent'
            
        super().__init__(parent, **kwargs)

        self._count = 0
        self._row = 0
        self.rowconfigure(self._row, weight=1)

    def add(self, widget, **kwargs):
        if 'weight' in kwargs:
            weight = kwargs['weight']
            del kwargs['weight']
        else:
            weight = 1
        if 'sticky' not in kwargs:
            kwargs['sticky'] = 'we'
        if 'row' in kwargs:
            del kwargs['row']
        if 'column' in kwargs:
            del kwargs['column']
        self.columnconfigure(self._count, weight=weight)
        widget.grid(row=0, column=self._count, **kwargs)
        self._count += 1

    def addRow(self):
        self._row += 1
        self.rowconfigure(self._row, weight=1)

class MultiComboBox(ctk.CTkFrame):
    def __init__(self, parent, variable, state='normal', **kwargs):
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = 'transparent'

        self._value_var = variable[0]
        self._value_var.trace('w', lambda *args: self.valueChanged)
        self._text_var = ctk.StringVar()
        self._option_vars = {}
            
        super().__init__(parent, **kwargs)

        self._menubutton = tk.Menubutton(self, textvariable=self._text_var, indicatoron=True, borderwidth=1, relief='raised', state=state)
        menu = tk.Menu(self._menubutton, tearoff=True)
        self._menubutton.configure(menu=menu)
        self._menubutton.pack(padx=10, pady=10, fill='x')

        values = [int(x) for x in self._value_var.get()]
        for i in range(len(FINGERS)):
            finger = FINGERS[i]
            value = values[i]
            self._option_vars[finger] = ctk.IntVar(value=value)
            menu.add_checkbutton(label=finger, variable=self._option_vars[finger], onvalue=1, offvalue=0, command=self.onChange)

        codes, names = self.getSelectedOptions()
        self._text_var.set(names)

    def setState(self, state):
        self._menubutton.configure(state=state)

    def onChange(self):
        codes, names = self.getSelectedOptions()
        self._text_var.set(names)
        self._value_var.set(codes)

    def valueChanged(self):
        values = [int(x) for x in self._value_var.get()]
        names = []
        for i in range(len(FINGERS)):
            finger = FINGERS[i]
            value = values[i]
            if value == 1:
                names.append(finger)
            self._option_vars[finger].set(value)
        names_str = ', '.join(names)
        self._text_var.set(names_str if len(names_str) else '-')

    def getSelectedOptions(self):
        codes_str = ''
        names = []
        for name, var in self._option_vars.items():
            value = var.get()
            codes_str += str(value)
            if value == 1:
                names.append(name)
        names_str = ', '.join(names)
        return codes_str, names_str if len(names_str) else '-'


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._app_title = 'Virtual Mouse'

        self.geometry('960x640')
        self.title('Virtual Mouse GUI')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        self.rowconfigure(0, weight=1)

        self._nav_vars = {}
        self._nav_inputs = {}

        self.createVariables()
        self.createElements()
        self.showFaceInfo(settings['face_method'])

    def createElements(self):
        # Create left side navigation panel
        nav_panel = ctk.CTkFrame(self)

        ctk.CTkLabel(nav_panel, text='Virtual Mouse', font=('Consolas', 18, 'bold')).pack(padx=10, pady=20)

        # Application launch button
        ctk.CTkButton(nav_panel, text='Start', font=FONT, command=self.launchApp).pack(pady=(10, 20), side=ctk.BOTTOM)

        # Reset settings button
        ctk.CTkButton(nav_panel, text='Reset Settings', font=FONT, command=self.recreateWindow).pack(pady=10, side=ctk.BOTTOM)

        nav_panel.grid(row=0, column=0, padx=(20, 5), pady=20, sticky='nswe')

        # Create settings panel with tab navigation
        tabview = ctk.CTkTabview(self)

        # Create general settings tab
        tab_general = tabview.add('General')

        # Mouse Sensitivity
        mouse_sensitivity_wrap = Grid(tab_general)
        mouse_sensitivity_wrap.add(ctk.CTkLabel(mouse_sensitivity_wrap, text='Mouse Sensitivity', font=FONT), weight=2, sticky='w')
        mouse_sensitivity_wrap.add(ctk.CTkSlider(mouse_sensitivity_wrap, variable=self._mouse_sensitivity_var, from_=0.5, to=5, number_of_steps=45), weight=3)
        mouse_sensitivity_wrap.add(ctk.CTkLabel(mouse_sensitivity_wrap, textvariable=self._mouse_sensitivity_str_var), weight=1)
        mouse_sensitivity_wrap.pack(padx=10, pady=10, fill='x')

        # Camera source
        camera_src_wrap = Grid(tab_general)
        camera_src_wrap.add(ctk.CTkLabel(camera_src_wrap, text='Camera Source', font=FONT), sticky='w')
        camera_src_wrap.add(ctk.CTkEntry(camera_src_wrap, textvariable=self._camera_src_var), weight=2)
        camera_src_wrap.pack(padx=10, pady=10, fill='x')

        # Create face settings tab
        tab_face = tabview.add('Face Recognition')

        # Face status
        face_status_input = ctk.CTkCheckBox(tab_face, text='Enable face recognition', font=FONT, variable=self._face_status_var, onvalue='on', offvalue='off')
        face_status_input.pack(padx=10, pady=10, fill='x')

        # Face method
        face_method_wrap = Grid(tab_face)
        face_method_wrap.add(ctk.CTkLabel(face_method_wrap, text='Method', font=FONT), sticky='w')
        face_method_wrap.add(ctk.CTkComboBox(face_method_wrap, values=list(face_utils.METHODS.keys()), variable=self._face_method_var))
        face_method_wrap.pack(padx=10, pady=10, fill='x')

        # Face status info
        ctk.CTkLabel(tab_face, textvariable=self._face_info_var, anchor='w', font=FONT).pack(padx=10, pady=10, fill='x')

        # Face action buttons
        btn_frame = ctk.CTkFrame(tab_face, fg_color='transparent')
        self._delete_face_btn = ctk.CTkButton(btn_frame, text='Delete Face Data', font=FONT, fg_color='#ff0000', hover_color='#aa0000', command=self.deleteFaceData)
        ctk.CTkButton(btn_frame, text='Register Your Face', font=FONT, command=self.registerFace).pack(side=ctk.RIGHT)
        btn_frame.pack(padx=10, pady=10, fill='x', side=ctk.BOTTOM)

        # Create mouse settings tab
        tab_mouse = tabview.add('Mouse Functions')

        # Navigation type
        nav_type_input = ctk.CTkCheckBox(tab_mouse, text='Enable two hands navigation', font=FONT, variable=self._nav_type_var, onvalue=2, offvalue=1)
        nav_type_input.pack(padx=10, pady=10, fill='x')

        # Main navigation hand
        main_hand_wrap = Grid(tab_mouse)
        main_hand_wrap.add(ctk.CTkLabel(main_hand_wrap, text='Main Hand', font=FONT), sticky='w')
        self._main_hand_input = ctk.CTkComboBox(main_hand_wrap, values=['Left', 'Right'], variable=self._main_hand_var, state='disabled' if settings['hands'] == 1 else 'normal')
        main_hand_wrap.add(self._main_hand_input)
        main_hand_wrap.pack(padx=10, pady=10, fill='x')

        # Navigation items
        nav_label_wrap = Grid(tab_mouse)
        nav_label_wrap.add(ctk.CTkLabel(nav_label_wrap, text='', font=FONT))
        nav_label_wrap.add(ctk.CTkLabel(nav_label_wrap, text='Left Hand', font=FONT))
        nav_label_wrap.add(ctk.CTkLabel(nav_label_wrap, text='Right Hand', font=FONT))
        nav_label_wrap.pack(padx=10, pady=(10, 0), fill='x')

        # Nav item: move
        nav_move_wrap = Grid(tab_mouse)
        nav_move_wrap.add(ctk.CTkLabel(nav_move_wrap, text='Move', font=FONT), sticky='w')
        self._nav_inputs['move'] = [
            MultiComboBox(nav_move_wrap, [self._nav_vars['move'][0]]),
            MultiComboBox(nav_move_wrap, [self._nav_vars['move'][1]], 'disabled' if settings['hands'] == 1 else 'normal')
        ]
        nav_move_wrap.add(self._nav_inputs['move'][0], sticky='we')
        nav_move_wrap.add(self._nav_inputs['move'][1], sticky='we')
        nav_move_wrap.pack(padx=10, pady=10, fill='x')

        # Nav item: faster_move
        nav_faster_move_wrap = Grid(tab_mouse)
        nav_faster_move_wrap.add(ctk.CTkLabel(nav_faster_move_wrap, text='Faster Move', font=FONT), sticky='w')
        self._nav_inputs['faster_move'] = [
            MultiComboBox(nav_faster_move_wrap, [self._nav_vars['faster_move'][0]]),
            MultiComboBox(nav_faster_move_wrap, [self._nav_vars['faster_move'][1]], 'disabled' if settings['hands'] == 1 else 'normal')
        ]
        nav_faster_move_wrap.add(self._nav_inputs['faster_move'][0])
        nav_faster_move_wrap.add(self._nav_inputs['faster_move'][1])
        nav_faster_move_wrap.pack(padx=10, pady=10, fill='x')

        # Nav item: left_click
        nav_left_click_wrap = Grid(tab_mouse)
        nav_left_click_wrap.add(ctk.CTkLabel(nav_left_click_wrap, text='Left click', font=FONT), sticky='w')
        self._nav_inputs['left_click'] = [
            MultiComboBox(nav_left_click_wrap, [self._nav_vars['left_click'][0]]),
            MultiComboBox(nav_left_click_wrap, [self._nav_vars['left_click'][1]], 'disabled' if settings['hands'] == 1 else 'normal')
        ]
        nav_left_click_wrap.add(self._nav_inputs['left_click'][0])
        nav_left_click_wrap.add(self._nav_inputs['left_click'][1])
        nav_left_click_wrap.pack(padx=10, pady=10, fill='x')

        # Nav item: right_click
        nav_right_click_wrap = Grid(tab_mouse)
        nav_right_click_wrap.add(ctk.CTkLabel(nav_right_click_wrap, text='Right Click', font=FONT), sticky='w')
        self._nav_inputs['right_click'] = [
            MultiComboBox(nav_right_click_wrap, [self._nav_vars['right_click'][0]]),
            MultiComboBox(nav_right_click_wrap, [self._nav_vars['right_click'][1]], 'disabled' if settings['hands'] == 1 else 'normal')
        ]
        nav_right_click_wrap.add(self._nav_inputs['right_click'][0])
        nav_right_click_wrap.add(self._nav_inputs['right_click'][1])
        nav_right_click_wrap.pack(padx=10, pady=10, fill='x')

        # Nav item: double_left_click
        nav_double_left_click_wrap = Grid(tab_mouse)
        nav_double_left_click_wrap.add(ctk.CTkLabel(nav_double_left_click_wrap, text='Double Left Click', font=FONT), sticky='w')
        self._nav_inputs['double_left_click'] = [
            MultiComboBox(nav_double_left_click_wrap, [self._nav_vars['double_left_click'][0]]),
            MultiComboBox(nav_double_left_click_wrap, [self._nav_vars['double_left_click'][1]], 'disabled' if settings['hands'] == 1 else 'normal')
        ]
        nav_double_left_click_wrap.add(self._nav_inputs['double_left_click'][0])
        nav_double_left_click_wrap.add(self._nav_inputs['double_left_click'][1])
        nav_double_left_click_wrap.pack(padx=10, pady=10, fill='x')

        # Nav item: drag_and_drop
        nav_drag_and_drop_wrap = Grid(tab_mouse)
        nav_drag_and_drop_wrap.add(ctk.CTkLabel(nav_drag_and_drop_wrap, text='Drag & Drop', font=FONT), sticky='w')
        self._nav_inputs['drag_and_drop'] = [
            MultiComboBox(nav_drag_and_drop_wrap, [self._nav_vars['drag_and_drop'][0]]),
            MultiComboBox(nav_drag_and_drop_wrap, [self._nav_vars['drag_and_drop'][1]], 'disabled' if settings['hands'] == 1 else 'normal')
        ]
        nav_drag_and_drop_wrap.add(self._nav_inputs['drag_and_drop'][0])
        nav_drag_and_drop_wrap.add(self._nav_inputs['drag_and_drop'][1])
        nav_drag_and_drop_wrap.pack(padx=10, pady=10, fill='x')

        # Nav item: scroll
        nav_scroll_wrap = Grid(tab_mouse)
        nav_scroll_wrap.add(ctk.CTkLabel(nav_scroll_wrap, text='Scroll', font=FONT), sticky='w')
        self._nav_inputs['scroll'] = [
            MultiComboBox(nav_scroll_wrap, [self._nav_vars['scroll'][0]]),
            MultiComboBox(nav_scroll_wrap, [self._nav_vars['scroll'][1]], 'disabled' if settings['hands'] == 1 else 'normal')
        ]
        nav_scroll_wrap.add(self._nav_inputs['scroll'][0])
        nav_scroll_wrap.add(self._nav_inputs['scroll'][1])
        nav_scroll_wrap.pack(padx=10, pady=10, fill='x')

        tabview.set('General')
        tabview.grid(row=0, column=1, padx=(5, 20), pady=(3, 20), sticky='nswe')

    def createVariables(self):
        # Mouse sensitivity
        self._mouse_sensitivity_var = ctk.DoubleVar(value=settings['mouse_sensitivity'])
        self._mouse_sensitivity_str_var = ctk.StringVar(value=settings['mouse_sensitivity'])
        self.handleChange('mouse_sensitivity', self._mouse_sensitivity_var)

        # Camera source
        self._camera_src_var = ctk.StringVar(value=settings['camera'])
        self.handleChange('camera', self._camera_src_var)

        # Face status
        self._face_status_var = ctk.StringVar(value='on' if settings['face'] else 'off')
        self.handleChange('face', self._face_status_var)

        # Face method
        self._face_method_var = ctk.StringVar(value=settings['face_method'])
        self.handleChange('face_method', self._face_method_var)

        # Face status info
        self._face_info_var = ctk.StringVar()

        # Navigation type
        self._nav_type_var = ctk.IntVar(value=settings['hands'])
        self.handleChange('hands', self._nav_type_var)

        # Main navigation hand
        self._main_hand_var = ctk.StringVar(value=settings['main_hand'])
        self.handleChange('main_hand', self._main_hand_var)

        # Navigation items
        self._nav_vars['move'] = [
            ctk.StringVar(value=settings['navigation']['move'][0]),
            ctk.StringVar(value=settings['navigation']['move'][settings['hands']-1])
        ]
        self._nav_vars['faster_move'] = [
            ctk.StringVar(value=settings['navigation']['faster_move'][0]),
            ctk.StringVar(value=settings['navigation']['faster_move'][settings['hands']-1])
        ]

        self._nav_vars['left_click'] = [
            ctk.StringVar(value=settings['navigation']['left_click'][0]),
            ctk.StringVar(value=settings['navigation']['left_click'][settings['hands']-1])
        ]

        self._nav_vars['right_click'] = [
            ctk.StringVar(value=settings['navigation']['right_click'][0]),
            ctk.StringVar(value=settings['navigation']['right_click'][settings['hands']-1])
        ]

        self._nav_vars['double_left_click'] = [
            ctk.StringVar(value=settings['navigation']['double_left_click'][0]),
            ctk.StringVar(value=settings['navigation']['double_left_click'][settings['hands']-1])
        ]

        self._nav_vars['drag_and_drop'] = [
            ctk.StringVar(value=settings['navigation']['drag_and_drop'][0]),
            ctk.StringVar(value=settings['navigation']['drag_and_drop'][settings['hands']-1])
        ]

        self._nav_vars['scroll'] = [
            ctk.StringVar(value=settings['navigation']['scroll'][0]),
            ctk.StringVar(value=settings['navigation']['scroll'][settings['hands']-1])
        ]

        for name, ls_var in self._nav_vars.items():
            self.handleNavChange(name, ls_var)

    def handleChange(self, key, var):
        var.trace('w', lambda *args: self.changeSetting(key, var))

    def handleNavChange(self, name, ls_var):
        ls_var[0].trace('w', lambda *args: self.changeNavSetting(name, [ls_var[0].get()] if settings['hands'] == 1 else [ls_var[0].get(), ls_var[1].get()]))
        ls_var[1].trace('w', lambda *args: self.changeNavSetting(name, [ls_var[0].get()] if settings['hands'] == 1 else [ls_var[0].get(), ls_var[1].get()]))

    def changeSetting(self, key, var):
        value = var.get()

        if key == 'camera':
            if len(value) == 0:
                return
        elif key == 'face':
            value = value == 'on'
            if value == settings[key]:
                return
        elif key == 'face_method':
            if len(value) == 0 or value == settings[key]:
                return
            self.showFaceInfo(value)
        elif key == 'hands':
            self._main_hand_input.configure(state='disabled' if value == 1 else 'normal')
            for nav_input in self._nav_inputs.values():
                nav_input[1].setState('disabled' if value == 1 else 'normal')
            for name, nav_var in self._nav_vars.items():
                if value == 1:
                    self.changeNavSetting(name, [nav_var[0].get()])
                else:
                    self.changeNavSetting(name, [nav_var[0].get(), nav_var[1].get()])
        elif key == 'mouse_sensitivity':
            value = round(value, 1)
            self._mouse_sensitivity_str_var.set(value)
            
        settings[key] = value
        saveSettings()

    def changeNavSetting(self, name, value):
        if len(value) == 0:
            return

        settings['navigation'][name] = value
        saveSettings()

    def checkCamera(self, source):
        cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            return False

        ret, _ = cap.read()

        cap.release()

        return ret

    def launchApp(self):
        if not self.checkCamera(int(settings['camera'])):
            messagebox.showerror('Error', 'This video source is unavailable')
            return
            
        subprocess.Popen(['python', 'vmouse.py'])

    def showFaceInfo(self, value):
        if self.faceIsRegistered(value):
            self._face_info_var.set('Your face is registered.')
            self._delete_face_btn.pack(side=ctk.LEFT)
        else:
            self._face_info_var.set('To use this functionality, please register your face.')
            self._delete_face_btn.pack_forget()

    def faceIsRegistered(self, method):
        path_dir = face_utils.PATHS['models_dir']
        path_file = face_utils.METHODS[method]['file']
        return os.path.isfile(os.path.join(path_dir, path_file))

    def deleteFaceData(self):
        if messagebox.askyesno('Question', 'Are you sure to delete the recognised face data?'):
            method = settings['face_method']
            path_dir = face_utils.PATHS['models_dir']
            path_file = face_utils.METHODS[method]['file']
            path = os.path.join(path_dir, path_file)
            if os.path.isfile(path):
                os.remove(path)
            self.showFaceInfo(method)

    def registerFace(self):
        if not self.checkCamera(int(settings['camera'])):
            messagebox.showerror('Error', 'This video source is unavailable')
            return
            
        trainer = FaceDetectorTrainer()
        face_utils.deleteTrainingImages()
        trainer.captureImages()
        trainer.train()
        face_utils.deleteTrainingImages()

        self.showFaceInfo(settings['face_method'])

    def recreateWindow(self):
        saveDefaultSettings()

        for widget in self.winfo_children():
            widget.destroy()

        self.createVariables()
        self.createElements()
        self.showFaceInfo(settings['face_method'])

if __name__ == "__main__":
    GUI().mainloop()