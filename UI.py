# PEP---80-characters-80-characters-80-characters-80-characters-80-characters---
import sys
import main
import tkinter
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, \
                              QTabWidget, QLayout, QHBoxLayout, QVBoxLayout, QGroupBox, \
                              QSlider, QCheckBox, QPushButton, QLabel, QLineEdit, \
                              QInputDialog, QMessageBox, \
                              QListWidget, QListWidgetItem
                                
from PySide6.QtGui import Qt, QIcon
from PySide6.QtCore import Slot

class PasswordDisplay: 
    """
    Desc : 
        Classe encapsulant des méthodes de display pour les mots de passe : 
        Show ou Hide. A placer dans une méthode d'evenements comme le process 
        contenant les méthodes "check_box_clicked" & "make_box_available".
    Args : 
        qline_edit (QLineEdit) : Le widget QLineEdit dont on veut masquer
        ou montrer les caractères.
    Return : 
        None.
    
    """
    def __init__(self,qline_edit) :

        self.qline_edit = qline_edit

    def hide(self) : 
        self.qline_edit.setEchoMode(QLineEdit.Password)

    def show(self) : 
        self.qline_edit.setEchoMode(QLineEdit.Normal)

class myWindow(QMainWindow) : 

    def __init__(self, title, icon_path) :
        """
        Desc : 
            Initialise la classe myWindow avec son titre principal ainsi
            que son icône. 
            Procède à la construction des parties pilières de l'UI.
        Args : 
            title (str) : Titre de la fenêtre principale.
            icon_path (str) : Chemin vers l'icone principale.
        Return : 
            None.

        """
        super().__init__()
        self.main_title = title
        self.main_icon = icon_path
        self.setWindowTitle(self.main_title)
        self.setWindowIcon(QIcon(self.main_icon))

        # Size variables :
        self.max_item_height = 40
        self.min_line_edit_height = 40
        self.window_min_height = 500
        self.window_min_width = 450

        # Icon variables :
        self.not_available_color = "#8c8c8c"
        self.available_color = "#000000"

        self.warning_window_icon = "icons/warning-icon.ico"
        self.save_not_available_icon = "icons/save_not_available.ico"     
        self.save_password_button_icon = "icons/save_icon.ico"     
        self.copy_not_available_icon = "icons/copy_not_available.ico"     
        self.copy_password_button_icon = "icons/copy.ico"    
        self.password_hide_icon = "icons/eyeclosedlogo.ico"
        self.password_show_icon = "icons/eyeopenlogo.ico"
        self.generate_password_button_icon = "icons/update.ico"
        self.password_line_edit_icon = "icons/lock.ico"
        self.modify_password_button_icon = "icons/modify.ico"
        self.delete_password_button_icon = "icons/trash.ico"

        self.password_icon = self.password_hide_icon

        # Data variables : 
        self.user_data_file = "password_data/password_data.json"

        # Window construction :
        self.create_central_widget()

        self.create_section_all_methods_items()
        self.create_section_essential_properties_layout()
        self.create_section_optionnal_properties_layout()
        self.create_section_generate_password_layout()
        self.create_section_copy_save_buttons_layout()
        
        # SAVED SECTION CONSTRUCTION &&

        self.create_saved_section_password_layout()

        self.tabs_main_layout()

    def create_warning_box(self, message = ""):
        """
        Desc : 
            Ouvre une fenêtre de warning contenant un message
        Args : 
            message (str) : le message à l'attention de l'utilisateur.
        Return : 
            None.
        """
        error_box = QMessageBox()
        error_box.setWindowTitle("Warning Message")
        error_box.setWindowIcon(QIcon(self.warning_window_icon))
        error_box.setText(message)
        error_box.exec()

    def create_central_widget(self) : 
        """
        Desc : 
            Section : MainWindow
            Créer le widget central et l'associe à un layout central. Set 
            également la taille minimum de l'objet.
        Args : 
            None.
        Return : 
            None.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.central_layout = QHBoxLayout(central_widget)
        self.setMinimumSize(self.window_min_height,self.window_min_width)

    def tabs_main_layout(self) : 
        """
        Desc : 
            Section : MainWindow
            Créer un GroupBox contenant un ou plusieurs layout(s).
        Args : 
            title (str) : Le titre du GroupBox.

            layout_list (lst) : Une liste contenant les layouts à ajouter dans 
                                le GroupBox.
        Return : 
            Un objet "groupbox" de type GroupBox.
        
        """
        all_tabs_dict = {
                        "Generate":[self.essential_groupbox,
                                        self.optionnal_groupbox,
                                        self.generate_password_groupbox,
                                        self.validate_buttons_groupbox
                                        ],
                        "Saved":[self.saved_password_groupbox # SAVED SECTION CONSTRUCTION &&
                                    ]}
        self.all_tabs = self.create_menu_tab(tab_dict=all_tabs_dict)
        self.central_layout.addWidget(self.all_tabs)

    # Widgets in Layouts : Definitions :
    
    def create_lenght_slider(self, title = "Default slider", min = 4, max = 30) : 
        """
        Desc : 
            Section : Generate
            Créer un layout composé horizontalement de : 
                - Un Label pour titrer le slider.
                - Un Slider.
                - Un GroupBox contenant un Label connecté qui affiche la 
                valeur du slider.
        Args : 
            title (str) : Le titre du slider.
            min (int) : valeur minimale du slider.
            max (int) : valeur maximale du slider.
        Return : 
            Un objet "slider_layout" de type QLayout et contenant tous les 
            widgets.
        """
        slider_layout = QHBoxLayout()

        slider = QSlider(orientation = Qt.Horizontal,
                         maximum = max,
                         minimum = min)
        slider_middle_value = int(max/2)
        slider.setValue(slider_middle_value)
        label = QLabel(title)
        self.connected_label = QLabel(str(slider_middle_value))
        connected_label_layout = QHBoxLayout()
        connected_label_layout.addWidget(self.connected_label)
        connected_label_groupbox = QGroupBox()
        connected_label_groupbox.setLayout(connected_label_layout)

        slider_layout.addWidget(label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(connected_label_groupbox)

        slider.valueChanged.connect(self.slider_value_changed)

        return slider,slider_layout

    def create_check_box(self, title = "Default check box") : 
        """
        Desc : 
            Section : Generate
            Créer un layout composé horizontalement de : 
                - Une CheckBox et son titre.
        Args : 
            title (str) : Le titre de la CheckBox.
            
        Return : 
            Un objet "check_box_layout" de type QLayout et contenant tous les 
            widgets.
        """
        check_box_layout = QHBoxLayout()
        check_box = QCheckBox(title)
        check_box_layout.addWidget(check_box)

        return check_box,check_box_layout

    def create_line_edit(self, title = "Default line edit", read_only = False) :
        """
        Desc : 
            Section : Generate
            Créer un layout composé horizontalement de : 
                - Un Label.
                - Un LineEdit
        Args : 
            title (str) : Le titre de la CheckBox.
            read_only (bool) : Options d'edit du LineEdit activée ou non
        Return : 
            Un objet "line_edit_layout" de type QLayout et contenant tous les 
            widgets.
        """

        line_edit_layout = QHBoxLayout()
        label = QLabel(title)
        line_edit = QLineEdit()
        line_edit_layout.addWidget(label)
        line_edit_layout.addWidget(line_edit)

        if read_only == True : 
            line_edit.setReadOnly()

        return line_edit,line_edit_layout

    def create_push_button(self, title = None, icon = None, 
                           min_width = 40, max_width = 1000,
                           min_height = 40, max_height = 1000) : 
        """
        Desc : 
            Section : Generate
            Crée un QPushButton avec une icone personnalisé et des dimensions
            spécifiques et modifiables.

        Args : 
            title (str): Texte sur le bouton
            icon (str) : Chemin vers l'icone
            min_width, max_witdh, min_height, max_height (int) : Dimensions (px)
        Return : 
            Un widget de type QPushButton.
        """
        push_button = QPushButton(title,icon=(QIcon(icon)))
        push_button.setMinimumHeight(min_height)
        push_button.setMaximumHeight(max_height)

        push_button.setMinimumWidth(min_width)
        push_button.setMaximumWidth(max_width)

        return push_button
        
    # Create Widgets Application :

    def create_section_all_methods_items(self) : 
        """
        Desc : 
            Section : Generate
            Lance toutes les fonctions de créations de widgets et layouts et 
            initialise l'état de ces derniers .
        Args : 
            None.
        Return : 
            None.
        """
        self.letters_check_box_list = self.create_check_box("Letters")
        self.letters_check_box = self.letters_check_box_list[0]
        self.letters_check_box_layout = self.letters_check_box_list[1]
        self.check_box_clicked()
        self.letters_check_box.setChecked(True)

        self.numbers_check_box_list = self.create_check_box("Numbers")
        self.numbers_check_box = self.numbers_check_box_list[0]
        self.numbers_check_box_layout = self.numbers_check_box_list[1]
        self.numbers_check_box.setChecked(True)

        self.specials_check_box_list = self.create_check_box("Specials")
        self.specials_check_box = self.specials_check_box_list[0]
        self.specials_check_box_layout = self.specials_check_box_list[1]

        self.mixed_case_check_box_list = self.create_check_box("Mixed Case (Need Letters)")
        self.mixed_case_check_box = self.mixed_case_check_box_list[0]
        self.mixed_case_check_box_layout = self.mixed_case_check_box_list[1]
        self.mixed_case_check_box.setChecked(True)

        self.cuts_check_box_list = self.create_check_box("Cuts")
        self.cuts_check_box= self.cuts_check_box_list[0]
        self.cuts_check_box_layout = self.cuts_check_box_list[1]
        self.cuts_check_box.setChecked(True)

        self.lenght_slider_list = self.create_lenght_slider("Length")
        self.lenght_slider = self.lenght_slider_list[0]
        self.lenght_slider_layout = self.lenght_slider_list[1]

        self.include_chars_list = self.create_line_edit("Include")
        self.include_chars = self.include_chars_list[0]
        self.include_chars_layout = self.include_chars_list[1]

        self.exclude_chars_list = self.create_line_edit("Exclude")
        self.exclude_chars = self.exclude_chars_list[0]
        self.exclude_chars_layout = self.exclude_chars_list[1]

        self.generate_password_button = self.create_push_button(title = "Generate Password", 
                                                       icon = self.generate_password_button_icon,max_width=500)
        
        self.view_password = self.create_push_button(title = "", icon = self.password_icon)

        self.copy_password_button = self.create_push_button(title = "Copy", 
                                                            icon = self.copy_not_available_icon)    
        self.copy_password_button.setStyleSheet(f"color : {self.not_available_color}")

        self.save_password_button = self.create_push_button(title = "Save", 
                                                            icon = self.save_not_available_icon)
        self.save_password_button.setStyleSheet(f"color : {self.not_available_color}")

    # Create Main Containers : Tabs :

    def create_menu_tab(self, 
                        tab_dict = {"Default_Title" : []}, 
                        direction = "V") : 
        """
        Desc : 
            Section : Generate
            Créer des onglets à partir d'un dictionnaire contenant les informations
            pour chaque item.

        Args : 
            tab_dict (dict) : Dictionnaire contenant les informations pour 
            chaque item :
                - Le titre de l'onglet.
                - Une liste de layout ou widgets à ajouter à l'onglet en cours.

            direction (str) : "V" pour un placement vertical des widgets/layout.
                               ou 
                              "H" pour un placement horizontal des widgets/layout.
        Return : 
            Un objet "tab" de type QTabWidget.
        QtWidget Process : 
            ## QTabWidget
        
        """
        tab = QTabWidget() 

        for title,list_items in tab_dict.items() : 
            main_widget = QWidget()
            tab.addTab(main_widget,title)
            if direction == "V" : 
                main_layout = QVBoxLayout()
            elif direction == "H" : 
                main_layout = QHBoxLayout()
            else : 
                raise ValueError("ERROR : La direction ne peut être que \"V\""
                                 " ou \"H\"")
            
            if list_items : 
                for item in list_items : 
                    if isinstance(item,QWidget) or isinstance(item,QGroupBox) : 
                        main_layout.addWidget(item)
                    if isinstance(item,QVBoxLayout) or isinstance(item,QHBoxLayout) : 
                        main_layout.addLayout(item)
            
            main_widget.setLayout(main_layout)
        
        return tab

    # Create Containers : GroupBox and Layouts :

    def create_groupbox(self,title = "Default Groupbox", layout_list = []):
        """
        Desc : 
            Section : Generate
            Créer un GroupBox contenant un ou plusieurs layout(s).
        Args : 
            title (str) : Le titre du GroupBox.

            layout_list (lst) : Une liste contenant les layouts à ajouter dans 
                                le GroupBox.
        Return : 
            Un objet "groupbox" de type GroupBox.
        
        """
        groupbox = QGroupBox(title)

        for layout in layout_list : 
            groupbox.setLayout(layout)

        return groupbox
    
    def create_section_essential_properties_layout(self):
        """
        Desc : 
            Section : Generate
            Crée la section de parametre essentiels pour le programme.
            Crée un GroupBox contenant un ou plusieurs layout(s). 
            En vue d'être ajouté plus tard à une tab dans la fonction tabs_main_layout()
        Args : 
            title (str) : Le titre du GroupBox.

            layout_list (lst) : Une liste contenant les layouts à ajouter dans 
                                le GroupBox.
        Return : 
            Un objet "groupbox" de type GroupBox.
        
        """
        self.essential_layout = QVBoxLayout()
        self.essential_layout.addLayout(self.lenght_slider_layout)
        self.essential_check_box_layout = QHBoxLayout()
        for layout in [self.letters_check_box_layout,
                       self.numbers_check_box_layout,
                       self.specials_check_box_layout
                       ]:
            self.essential_check_box_layout.addLayout(layout)
        self.essential_layout.addLayout(self.essential_check_box_layout)
        self.essential_groupbox = self.create_groupbox(title = "Essential Settings", 
                                                       layout_list = [self.essential_layout])

    def create_section_optionnal_properties_layout(self):
        """
        Desc : 
            Section : Generate
            Crée la section de parametre optionnels pour le programme.
            Crée un GroupBox contenant un ou plusieurs layout(s). 
            En vue d'être ajouté plus tard à une tab dans la fonction tabs_main_layout()
        Args : 
            title (str) : Le titre du GroupBox.

            layout_list (lst) : Une liste contenant les layouts à ajouter dans 
                                le GroupBox.
        Return : 
            Un objet "groupbox" de type GroupBox.
        
        """
        self.optionnal_layout = QVBoxLayout()
        widget_lists_list = [[self.mixed_case_check_box_layout, self.cuts_check_box_layout],
                             [self.include_chars_layout,self.exclude_chars_layout]
                             ]
        for widget_list in widget_lists_list : 
            optionnal_sub_layout = QHBoxLayout()
            for layout in widget_list: 
                optionnal_sub_layout.addLayout(layout)
            self.optionnal_layout.addLayout(optionnal_sub_layout)
            self.optionnal_groupbox = self.create_groupbox(title = "Optionnal Settings", 
                                                       layout_list = [self.optionnal_layout])

    def password_display_action(self) : 
        """
        Desc : 
            Section : Generate
            Crée un mot de passe à partir de la classe Password importée du module 
            principal "main".
            Set ensuite le mot de passe dans le line edit adéquat.
        Args : 
            None.
        Return : 
            None.
        """
        self.password_display = PasswordDisplay(self.password_line_edit)
        self.password_display.hide()
        self.view_password.clicked.connect(self.show_hide_password)

    def create_section_generate_password_layout(self):
        """
        Desc : 
            Section : Generate
            Crée la section de génération de mot de passe à partir des boutons existants.
            Crée un bouton "Generate", un qline edit contenant le mot de passe généré,
            un bouton qui permet de hide/show le mot de passe, un label qui indique à 
            l'utilisateur si le mot de passe fort ou faible. 
            Ces layouts et widgets sont contenus dans un groupbox.
            
        Args : 
            None.
        Return : 
            None.
        
        """
        # Edit du bouton generate et création de son layout : 

        self.generate_button_clicked()
        self.generate_password_button.setMinimumWidth(250)
        self.generate_password_layout = QVBoxLayout()
        self.generate_password_layout.addWidget(self.generate_password_button,alignment = Qt.AlignmentFlag.AlignHCenter)

        # 1) Création du line edit contenant le mot de passe (sans passer par la
        # méthode disponible car pas besoin de label associé au line_edit)
        # 2) Connection au Slot rendant available ou non les boutons save et copy
        # en fonction du contenu du line edit

        self.password_line_edit = QLineEdit()
        self.password_line_edit.setMinimumHeight(self.min_line_edit_height)
        self.password_line_edit.setClearButtonEnabled(True)
        self.password_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_line_edit.textChanged.connect(self.change_save_button_icon)
        
        # Edit du bouton show/view qui permettra de voir ou non le mot de passe :
        # Définition de l'action du bouton : 
        
        self.password_display_action()

        # Création du layout qui accueillera le line edit mais aussi le bouton view/show
        # Ajout du layout line edit au layout principal de generate password et création 
        # du groupbox qui accueillera ce dernier.

        self.password_line_edit_layout = QHBoxLayout()
        self.password_line_edit_layout.addWidget(self.password_line_edit)
        self.password_line_edit_layout.addWidget(self.view_password)

        self.generate_password_layout.addLayout(self.password_line_edit_layout)

        self.generate_password_groupbox = self.create_groupbox(title = "Generate Password", 
                                                       layout_list = [self.generate_password_layout])

    def create_section_copy_save_buttons_layout(self):
        """
        Desc : 
            Section : Generate
            Crée la section de copy et save à partir des boutons existants et le layout 
            auquel ces derniers sont associés.
            Ce layout est contenu dans un groupbox.
            
        Args : 
            None.
        Return : 
            None.
        
        """
        # Edit des boutons copy et save et création de leur layout et groupbox: 

        self.copy_password_button.setMinimumWidth(150)
        self.copy_button_clicked()
        self.save_password_button.setMinimumWidth(150)
        self.save_button_clicked()

        self.validate_buttons_layout = QHBoxLayout()
        self.validate_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.validate_buttons_layout.addWidget(self.copy_password_button)
        self.validate_buttons_layout.addWidget(self.save_password_button)

        self.validate_buttons_groupbox = self.create_groupbox(title = "", 
                                                              layout_list = [self.validate_buttons_layout])

    # Signals / Actions / Connection Widgets :

    def check_box_clicked(self):
        """
        Desc : 
            Section : Generate
            Méthode de connexion : 
            Connecte la méthode d'évenement "make_box_available" au click de 
            la CheckBox "Letters".
        Args : 
            None.
        Return : 
            None.
        """
        self.letters_check_box.clicked.connect(self.make_box_available)

    def generate_button_clicked(self):
        """
        Desc : 
            Section : Generate
            Méthode de connexion : 
            Connecte la méthode d'évenement "create_password" au click du 
            bouton "Generate".
        Args : 
            None.
        Return : 
            None.
        """
        self.generate_password_button.clicked.connect(self.create_password)

    def copy_button_clicked(self):
        """
        Desc : 
            Section : Generate
            Méthode de connexion : 
            Connecte la méthode d'évenement "copy_password" au click du 
            bouton "Copy".
        Args : 
            None.
        Return : 
            None.
        """
        self.copy_password_button.clicked.connect(self.copy_password)

    def save_button_clicked(self) : 
        """
        Desc : 
            Section : Generate
            Méthode de connexion : 
            Connecte la méthode d'évenement "save_password" au click du 
            bouton "Save".
        Args : 
            None.
        Return : 
            None.
        """
        self.save_password_button.clicked.connect(self.save_password)

    def add_password_to_json_file(self) : 
        """
        Desc : 
            Section : Generate
            Méthode de sauvegarde : 
            Met à jour le dictionnaire avec les nouvelles entrées et modifie
            entièrement le password_data.json en mettant à jour le fichier.
        Args : 
            None.
        Return : 
            None.
        """
        self.new_reference_to_save_text = self.new_reference_to_save.text()
        self.new_password_to_save_text = self.new_password_to_save.text()

        self.data_base[self.new_reference_to_save_text] = self.new_password_to_save_text
        
        json_dict = json.dumps(self.data_base,indent = 4)
        with open(self.user_data_file, "w") as outfile:
            outfile.write(json_dict)

    @Slot()
    def slider_value_changed(self,value) : 
        """
        Desc : 
            Section : Generate
            Méthode d'évènement : 
            Set au label dynamique la valeur du slider en fonction du déplacement de 
            l'utilisateur.
        Args : 
            value (int) : La valeur retournée par le slider.
        Return : 
            None.
        
        """
        self.slider_value = value
        self.connected_label.setText(str(value))

    @Slot()
    def make_box_available(self,value):
        """
        Desc : 
            Section : Generate
            Méthode d'évènement : 
            Set la disponibilité de la CheckBox "Mixed Case" en fonction de l'état
            de la CheckBox "Letters" : Si elle est cochée alors la Mixed Case est 
            disponible. Le cas échéant, elle est grisée et ne peux être cochée.
        Args : 
            value (bool) : La valeur retournée par la box.
        Return : 
            None.
        """
        if value == False : 
            self.mixed_case_check_box.setCheckable(False)
            self.mixed_case_check_box.setStyleSheet(f"color:{self.not_available_color}")

        else : 
            self.mixed_case_check_box.setCheckable(True)
            self.mixed_case_check_box.setStyleSheet(f"color:{self.available_color}")

    @Slot()
    def show_hide_password(self) : 
        """
        Desc : 
            Section : Generate
            Méthode d'évènement : 
            Set la visibilité du mot de passe en fonction du click du bouton.
            Query le statut du qline edit.
        Args : 
            None.
        Return : 
            None.
        """
        password_display_current_state = str(self.password_line_edit.echoMode())
        if password_display_current_state == "EchoMode.Password" : 
            self.password_display.show()
            self.password_icon = self.password_show_icon
        else : 
            self.password_display.hide()
            self.password_icon = self.password_hide_icon

        self.view_password.setIcon(QIcon(self.password_icon))

    @Slot()
    def create_password(self) : 
        """
        Desc : 
            Section : Generate
            Méthode d'évènement : 
            Crée un mot de passe à partir de la classe Password.
            Set ensuite le mot de passe dans le line edit adéquat.
        Args : 
            None.
        Return : 
            None.
        """

        self.password = main.Password(length = self.lenght_slider.value(),
                                      include_letters = self.letters_check_box.isChecked(),
                                      include_numbers = self.numbers_check_box.isChecked(),
                                      include_special_chars = self.specials_check_box.isChecked(),
                                      include_mixed_case = self.mixed_case_check_box.isChecked(),
                                      include_cuts = self.cuts_check_box.isChecked(),
                                      include_chars = self.include_chars.text(),
                                      exclude_chars = self.exclude_chars.text()
                                      )
        
        self.password = self.password.generate()
        self.password_line_edit.setText(self.password)
        self.password_output = self.password_line_edit.text()

    @Slot()
    def copy_password(self) : 
        """
            Section : Generate
        Desc : 
            Méthode d'évènement : 
            Permet de copier le mot de passe généré dans le presse-papier à 
            l'aide de tkinter. D'
        Args : 
            None.
        Return : 
            None.
        """
        self.password_output = self.password_line_edit.text()

        if self.password_output != "" : 
            print("Password copied is : ",self.password_output)
            copy_to_clipboard = tkinter.Tk() # Create Tk object
            copy_to_clipboard.withdraw() # To disable window generated by Tk
            copy_to_clipboard.clipboard_clear()
            copy_to_clipboard.clipboard_append(self.password_output)
            copy_to_clipboard.update() # Value stays in the clipboard after window 
                                    # is closed
            copy_to_clipboard.destroy() 

    @Slot()
    def save_password(self):
        """
        Desc : 
            Section : Generate
            Méthode d'évènement : 
            Permet d'ajouter à la liste de l'interface les nouvelles entrées :
            - Mot de passe
            - Reference de mot de passe
            Récupère le mot de passe créé, puis ouvre un QDialog pour récupérer
            la référence auprès de l'utilisateur.
            A partir de ces données, on crée le nouveau layout horizontal,
            Puis on l'ajoute à la QListWidget,
            Puis on ajoute les données au self.data_array_dict qui contient
            des identifiants pour chaque QWidget.
            Si rien n'est entré dans le QDialog, un QMessageBox s'ouvre pour
            informer l'utilisateur que rien n'a été sauvegardé.
        Args : 
            value (int) : La valeur retournée par le slider.
        Return : 
            None.
        
        """
        self.password_output = self.password_line_edit.text()

        if self.password_output : 
            reference_dialog = QInputDialog()
            reference_dialog.setWindowTitle("Reference Name")
            reference_dialog.setWindowIcon(QIcon(self.main_icon))
            reference_dialog.setLabelText("Password reference name : ")
            reference_dialog.exec()
            self.reference_output = reference_dialog.textValue()

            if self.reference_output : 

                new_row =self.create_existing_passwords_row_layout(reference = self.reference_output,
                                                                password = self.password_output)
                self.new_password_to_save = new_row[0]
                self.new_reference_to_save = new_row[1]
                layout = new_row[2]
                self.add_to_password_list(layout,self.saved_section_password_listwidget)
                self.add_password_to_json_file()
                last_id = int(list(self.data_array_dict.keys())[-1])
                self.data_array_dict[last_id+1] = new_row[0]
                self.data_array_dict[last_id+2] = new_row[1]
            else : 
                self.create_warning_box("Saving aborted.")

    @Slot()
    def change_save_button_icon(self,value) : 
        """
        Desc : 
            Section : Generate
            Méthode d'évènement : 
            Change l'icone et la couleur des boutons "Save" et "Copy" en 
            fonction du contenu rempli ou vide du Generate QLineEdit.
        Args : 
            value (str) : La valeur retournée par le QLineEdit.
        Return : 
            None.
        
        """
        if value :
            self.copy_password_button.setIcon(QIcon(self.copy_password_button_icon))
            self.copy_password_button.setStyleSheet(f"color:{self.available_color}")
            self.save_password_button.setIcon(QIcon(self.save_password_button_icon))
            self.save_password_button.setStyleSheet(f"color:{self.available_color}")
        else : 
            self.save_password_button.setIcon(QIcon(self.save_not_available_icon))
            self.save_password_button.setStyleSheet(f"color : {self.not_available_color}")
            self.copy_password_button.setIcon(QIcon(self.copy_not_available_icon))
            self.copy_password_button.setStyleSheet(f"color : {self.not_available_color}")

    class CreateSection() :
        
        def __init__(self) : 
            pass

    class SavedSection() :
        
        def __init__(self) : 
            pass

        # SAVED SECTION CONSTRUCTION &&

    def get_password_dict_from_json(self, password_file_url): 
        """
        Desc : 
            Section : Saved
            Méthode d'acquisition : 
            Permet de récupérer les mots de passe présents dans le fichier
            json.
        Args : 
            password_file_url (str) : url du fichier .json contenant les 
                                      données.
        Return : 
            Un dictionnaire avec comme clé la référence et comme valeur
            le mot de passe associé.
        """
        password_file = open(password_file_url)
        password_data = json.load(password_file)
        return password_data

    def save_password_dict_to_json(self, password_file_url): 
        """
        Desc : 
            Section : Saved
            Méthode de sauvegarde : 
            Permet d'update le fichier json avec le nouveau dictionnaire 
            de stockage "self.data_base", recréé à partir du dictionnaire 
            de gestion "self.data_array_dict".
        Args : 
            password_file_url (str) : url du fichier .json contenant les 
                                      données.
        Return : 
            None.
        
        """
        self.data_base = {}
        
        for id,data in self.data_array_dict.items() : 
            if id%2 != 0 : 
                self.data_base[self.data_array_dict[id+1].text()] = data.text()
        
        json_dict = json.dumps(self.data_base,indent = 4)
        with open(password_file_url, "w") as outfile:
            outfile.write(json_dict)

    def create_saved_content_line_edit(self,
                                       content = "DefaultPassword",
                                       hidden = True, 
                                       read_only = True) : 
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Crée un QLine Edit avec un content
        Args : 
            password_file_url (str) : url du fichier .json contenant les données.
            hidden (bool) : set if password is hidden by default or not.
            read_only (bool) : set Qline Edit read only.

        Return : 
            Un dictionnaire avec comme clé la référence et comme valeur
            le mot de passe associé.
        """
        content = str(content)
        saved_content = QLineEdit(content)
        saved_content.setMaximumHeight(self.max_item_height)
        if hidden :
            saved_content.setEchoMode(QLineEdit.Password)
        if read_only :
            saved_content.setReadOnly(True)
        return saved_content

    def create_modify_password_button(self):
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Crée le QPushButton qui permet d'éditer les mots de passe pour 
            chaque layout qui se trouve dans la QListWidget de la section 
            "Saved" du programme.
            Set un adjectif de statut qui permettra de savoir le
            current state du bouton et qui sera modifié à chaque click du 
            button.
        Args : 
            None.
        Return : 
            Un widget de type QPushButton.
        """

        modify_button = self.create_push_button(title = "", 
                                                icon = self.modify_password_button_icon,
                                                max_height = self.max_item_height)
        self.edit_sender_button_content = "Edit"
        return modify_button

    def create_delete_password_button(self):
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Crée le QPushButton qui permet de supprimer les mots de passe pour 
            chaque layout qui se trouve dans la QListWidget de la section 
            "Saved" du programme.

        Args : 
            None.
        Return : 
            Un widget de type QPushButton.
        """
        delete_button = self.create_push_button(title = "", 
                                                icon = self.delete_password_button_icon,
                                                max_height = self.max_item_height)
        return delete_button

    def save_changes_section(self,widget_list) : 
        """
        Desc : 
            Section : Saved
            Méthode d'action : 
            1) Modifie le display et le statut des QLine Edit quand le 
            bouton au statut "Save" est cliqué : 
                a) Set les QlineEdit en readOnly et 
                b) Change l'echoMode de celui identifié comme le password 
                pour cacher le texte.
            2) Passe la méthode qui permet d'update le fichier json.
        Args : 
            widget_list : liste des QlineEdit du parent du button cliqué.
        Return : 
            None.
        """
        for widget in widget_list :
            widget.setReadOnly(True)
            for id, data in self.data_array_dict.items() : 
                if widget == data : 
                    if id%2 != 0 :
                        widget.setEchoMode(QLineEdit.Password)

        print("self.data_array_dict est le dictionnaire essentiel de GESTION")
        print("self.data_base est le dictionnaire essentiel de STOCKAGE")

        self.save_password_dict_to_json(self.user_data_file)

    def make_editable_section(self,widget_list) : 
        """
        Desc : 
            Section : Saved
            Méthode d'action : 
            Modifie le display et le statut des QLine Edit quand le 
            bouton au statut "Edit" est cliqué : 
                a) Set les QlineEdit en write
                b) Change l'echoMode de celui identifié comme le password 
                pour afficher le texte.
        Args : 
            widget_list : liste des QlineEdit du parent du button cliqué.
        Return : 
            None.
        """
        for widget in widget_list :
            if widget.isReadOnly() : 
                widget.setReadOnly(False)
                widget.setEchoMode(QLineEdit.Normal)
    @Slot()
    def modify_action_button(self) : 
        """
        Desc : 
            Section : Saved
            Méthode d'évènement : 
            Permet de retrouver les QlineEdit correspondants au bouton cliqué
            afin de pouvoir lancer les méthodes d'actions permettant de rendre
            les QLineEdit soit éditables, soit de les remettre dans leur 
            statut initial et de sauvegarder les changements apportés.
        Args : 
            None.
        Return : 
            None.
        """
        sender_button = self.sender() # Permet de savoir quel bouton 
                                      # a envoyé le signal
        button_parent = sender_button.parentWidget() # Trouve le parent du 
                                                     # bouton émeteur, ici  
                                                     # c'est un Qwidget
        line_edit_list = button_parent.findChildren(QLineEdit)
        # La méthode "findChildren trouve les enfants du parent # QWidget de 
        # type QLineEdit

        if self.edit_sender_button_content == "Edit" :
            sender_button.setIcon(QIcon(self.save_password_button_icon))
            self.make_editable_section(line_edit_list)
            self.edit_sender_button_content = "Save"

        elif self.edit_sender_button_content == "Save" : 
            sender_button.setIcon(QIcon(self.modify_password_button_icon))
            self.save_changes_section(line_edit_list)
            self.edit_sender_button_content = "Edit"

    def delete_action_button(self) : 
        pass

    def create_save_password_button(self):
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Permet de créer le QPushButton "Save" de la section "Saved".
        Args : 
            None.
        Return : 
            Un QWidget de type QPushButton.
        """
        save_button = self.create_push_button(title = "", 
                                                icon = self.save_password_button_icon,
                                                max_height = self.max_item_height)
        return save_button

    def create_existing_passwords_row_layout(self,reference,password):
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Utilisée dans : self.save_password()
            Utilisée dans : self.create_saved_content()
            
            Permet de créer le layout complet d'une ligne de QListWidget de
            la section "Saved" : 
                a) Création des deux lineEdit remplis et customisés dans la 
                méthode de création "create_saved_content_line_edit".
                b) Création des deux boutons Edit et Delete, et association
                de leur méthode d'evenement respectives
                c) Création du layout horizontal et accueil de tous les 
                widgets.
        Args : 
            reference (str) : Le contenu string déjà présent dans le 
                              dictionnaire self.data_base, ou bien issu de la 
                              fenetre input remplie par l'utilisateur lors de
                              la sauvegarde.
            password (str) :  Le contenu string déjà présent dans le 
                              dictionnaire self.data_base, ou bien issu de la 
                              QlineEdit remplie par l'outil lors de la 
                              génération du mot de passe ou de bien directement
                              rempli par l'utilisateur.
        Return : 
            Une liste composée des deux QLineEdit et du layout horizontal.
        """
        password_line_edit = self.create_saved_content_line_edit(content = password)
        reference_line_edit = self.create_saved_content_line_edit(content = reference, 
                                                                  hidden = False)
        button_line_edit = self.create_modify_password_button()
        button_line_edit.clicked.connect(self.modify_action_button)
        button_line_delete = self.create_delete_password_button()
        button_line_delete.clicked.connect(self.delete_action_button)

        existing_passwords_layout = QHBoxLayout()
        existing_passwords_layout.addWidget(password_line_edit)
        existing_passwords_layout.addWidget(reference_line_edit)
        existing_passwords_layout.addWidget(button_line_edit)
        existing_passwords_layout.addWidget(button_line_delete)

        return password_line_edit, reference_line_edit, existing_passwords_layout

    def create_saved_content(self) : 
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Utilisée dans : self.create_saved_section_password_layout()
                        
            Permet de créer tous les layouts qui vont servir pour la 
            QListWidget.
            Crée le self.data_array_dict : 
                Ce dictionnaire de gestion marche sur le principe suivant : 
                - Une clé impaire représente un QLineEdit référence.
                - Une clé paire représente un QLineEdit mot de passe.
        Args : 
            None.
        Return : 
            Une liste composée de tous les layouts horizontaux.
        """
        layout_list = []
        self.data_base = self.get_password_dict_from_json(self.user_data_file)
        self.data_array_dict = {}
        id = 0
        for reference, password in self.data_base.items() : 
            id +=1 
            row = self.create_existing_passwords_row_layout(reference,password)
            self.data_array_dict[id] = row[0]
            id +=1 
            self.data_array_dict[id] = row[1]
            layout = row[2]
            layout_list.append(layout)
        
        return layout_list
    
    def add_to_password_list(self,layout_list,listwidget):
        """
        Desc : 
            Section : Saved
            Méthode d'ajout : 
            Utilisée dans : self.create_saved_section_password_layout()
                        
            Permet d'ajouter à une QListWidget une liste de layout: 
                a) Création d'un QWidget qui sert ensuite à encapsuler le 
                layout.
                b) Création d'un QListWidgetItem qui va permettre de placer
                dans la QListWidget le QWidget.
                c) Set de la size du WidgetItem en fonction de celle du layout
                d) Ajout de WidgetItem dans la QListWidget
                e) Association du QWidget au WidgetItem
                f) Une fois la boucle terminée, ajout du widget mis à jour 
                   dans le layout principal de la section "Saved".
        Args : 
            None.
        Return : 
            None.
        """
        if not isinstance(layout_list,list) : 
            layout_list = [layout_list]
        for layout in layout_list : 
            widget_layout = QWidget()
            widget_layout.setLayout(layout)
            item_list = QListWidgetItem()
            item_list.setSizeHint(widget_layout.sizeHint())
            listwidget.addItem(item_list)
            listwidget.setItemWidget(item_list,widget_layout)
        self.saved_section_password_layout.addWidget(self.saved_section_password_listwidget)

    def create_saved_section_password_layout(self):
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Utilisée dans : self.__init__()
                        
            Crée le Layout principal de la section "Saved", ainsi que la 
            QListWidget principale, puis ajoute les layout grâce à la méthode
            self.add_to_password_list. Pour finir, crée et associe la GroupBox
            de la section au layout principal.
        Args : 
            None.
        Return : 
            None.
        """
        layout_list = self.create_saved_content()
        self.saved_section_password_layout = QVBoxLayout()
        self.saved_section_password_listwidget = QListWidget()
        self.add_to_password_list(layout_list,self.saved_section_password_listwidget)
        self.saved_password_groupbox = self.create_groupbox(
            title = "Saved Passwords", 
            layout_list = [self.saved_section_password_layout])

if __name__ == "__main__" : 
    app = QApplication(sys.argv)
    main_icon = sys.argv[1] if len(sys.argv) > 1 else "icons/logo.ico"
    main_title = "Password Manager"
    main_window = myWindow(main_title,main_icon)
    main_window.show()
    sys.exit(app.exec())

    # SAVED SECTION CONSTRUCTION &&