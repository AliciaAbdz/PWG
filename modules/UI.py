# PEP---80-characters-80-characters-80-characters-80-characters-80-characters---
import sys
import tkinter
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, \
                              QTabWidget, QHBoxLayout, QVBoxLayout, QGroupBox, \
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
        contenant les méthodes "check_box_clicked" & "set_box_available".
    Args : 
        qline_edit (QLineEdit) : Le widget QLineEdit dont on veut masquer
        ou montrer les caractères.
    Return : 
        None.
    
    """
    def __init__(self, qline_edit) :
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
        self.GENERATE_SECTION_LINE_EDIT_MAXH = 40
        self.SAVED_SECTION_LINE_EDIT_MAXH = 30
        self.SAVED_SECTION_BUTTON_MINS = 30
        self.WINDOW_MINH = 500
        self.WINDOW_MINW = 450

        # Saved section disposition :
        self.PASSWORD_IDX = 0
        self.REFERENCE_IDX = 1

        # Icon variables :
        self.NOT_AVAILABLE_COLOR = "#646464"
        self.AVAILABLE_COLOR = "#000000"

        self.WARNING_WINDOW_ICON = "icons/warning-icon.ico"
        self.SAVE_NOT_AVAILABLE_ICON = "icons/save_not_available.ico"     
        self.SAVE_ICON = "icons/SAVE_ICON.ico"     
        self.COPY_NOT_AVAILABLE_ICON = "icons/copy_not_available.ico"     
        self.COPY_ICON = "icons/copy.ico"    
        self.HIDE_ICON = "icons/eyeclosedlogo.ico"
        self.SHOW_ICON = "icons/eyeopenlogo.ico"
        self.GENERATE_ICON = "icons/update.ico"
        self.MODIFY_ICON = "icons/modify.ico"
        self.TRASH_ICON = "icons/trash.ico"

        self.psswd_icon = self.HIDE_ICON

        # Data variables : 
        self.user_data_file = "data/password_data/password_data.json"

        # Window construction :
        self.create_central_widget()

        self.generate_section_all_items()
        self.generate_section_essential_properties_layout()
        self.generate_section_optionnal_properties_layout()
        self.generate_section_create_password_layout()
        self.generate_section_copy_save_buttons_layout()

        self.saved_section_main_layout()

        self.tabs_main_layout()

    # Message boxes :

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
        error_box.setWindowIcon(QIcon(self.WARNING_WINDOW_ICON))
        error_box.setText(message)
        error_box.exec()

    def create_confirm_box(self, 
                           message = "Voulez-vous confirmer?", 
                           conf = "Confirm", 
                           canc = "Cancel") : 
        """
        Desc : 
            Ouvre une fenêtre de confirmation contenant un message et deux
            boutons à l'attention de l'utilisateur.
        Args : 
            conf (str) : Le texte du bouton de confirmation .
            canc (str) : Le texte du bouton d'annulation .
        Return : 
            Une variable de type boolean sur le choix de l'utilisateur.
        """
        confirmed = False
        confirm_box = QMessageBox(text = message)
        confirm_box.setWindowTitle("Confirm Window")
        confirm_box.setWindowIcon(QIcon(self.WARNING_WINDOW_ICON))
        confirm_box.addButton(conf, QMessageBox.ButtonRole.YesRole)
        confirm_box.addButton(canc, QMessageBox.ButtonRole.NoRole)
        confirm_box.exec()
        output_user = confirm_box.clickedButton().text()
        if output_user == conf :
            confirmed = True
        return confirmed
    
    # Misc methods :

    def get_widget_list(self, q_widget_list) :
        """
        Desc : 
            Permet de récupérer une liste des widgets présent dans une QListWidget.
        Args : 
            q_widget_list (QListWidget) : La QListWidget dont il faut extraire les données.
        Return : 
            list_contents (list) : Une variable de type list contenant des éléments
                                   de type QWidget.
        """
        if not isinstance(q_widget_list, QListWidget) :
            raise TypeError("This method needs QListWidget class.")
        list_contents = []
        list_range = q_widget_list.count()
        for idx in range(list_range):
            item_widget = q_widget_list.item(idx)
            widget = q_widget_list.itemWidget(item_widget)
            list_contents.append(widget)
        return list_contents
    
    def get_data_list_widget(self, child = "R") :
        """
        Desc : 
            Section : Saved
            Méthode de gestion : 
            Utilisée dans  : self.save_password()
                             self.modify_button_clicked()
                             self.delete_button_clicked()
            Récupère la liste des références (par défaut) ou des passwords, 
            à partir de la liste principale actuelle. 
            A utiliser lors d'évènements utilisants des méthodes visant à 
            modifier la liste.
        Args : 
            child(str) : "R" pour référence, "P" pour password
        Return : 
            new_data_list_widget (list) : Une liste de datas de type string.
        """
        new_data_list_widget = []
        data_list = self.get_widget_list(self.saved_section_psswd_listwidget)
        for widget in data_list : 
            children = widget.findChildren(QLineEdit)
            if child == "R" : 
                child = children[self.REFERENCE_IDX].text()
            elif child == "P" : 
                child = children[self.PASSWORD_IDX].text()
            else : 
                raise ValueError("Only 'R' and 'P' string flags are supported "
                                 "for child arg.")
            new_data_list_widget.append(child)
        return new_data_list_widget

    # Main window methods :
        
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
        # central_widget.setStyleSheet("background : #fffed2")
        self.setCentralWidget(central_widget)
        self.central_layout = QHBoxLayout(central_widget)
        self.setMinimumSize(self.WINDOW_MINH, self.WINDOW_MINW)

    # Main widgets methods :
    
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
            Une liste contenant le widget "slider" et son QHBoxLayout associé.
        """
        slider_layout = QHBoxLayout()

        title_label = QLabel(title)
        slider = QSlider(orientation = Qt.Horizontal, 
                         maximum = max, 
                         minimum = min)
        slider_mid_value = int(max/2)
        slider.setValue(slider_mid_value)

        self.value_label = QLabel(str(slider_mid_value))
        value_label_layout = QHBoxLayout()
        value_label_layout.addWidget(self.value_label)

        slider_layout.addWidget(title_label)
        slider_layout.addWidget(slider)
        slider_layout.addLayout(value_label_layout)

        slider.valueChanged.connect(self.slider_value_changed)

        return slider, slider_layout

    def create_check_box(self, title = "Default check box") : 
        """
        Desc : 
            Section : Generate
            Créer un layout composé horizontalement de : 
                - Une CheckBox et son titre.
        Args : 
            title (str) : Le titre de la CheckBox.
            
        Return : 
            Une liste contenant le widget "check_box" et son QHBoxLayout associé.
        """
        check_box_layout = QHBoxLayout()
        check_box = QCheckBox(title)
        check_box_layout.addWidget(check_box)

        return check_box, check_box_layout

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
            Une liste contenant le widget "check_box" et son QHBoxLayout associé.
        """

        line_edit_layout = QHBoxLayout()
        label = QLabel(title)
        line_edit = QLineEdit()
        line_edit_layout.addWidget(label)
        line_edit_layout.addWidget(line_edit)

        if read_only == True : 
            line_edit.setReadOnly()

        return line_edit, line_edit_layout

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
        push_button = QPushButton(title, icon = (QIcon(icon)))

        push_button.setMinimumHeight(min_height)
        push_button.setMaximumHeight(max_height)
        push_button.setMinimumWidth(min_width)
        push_button.setMaximumWidth(max_width)

        return push_button
        
    # # Generate Section Construction :

    def generate_section_all_items(self) : 
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

        self.mixed_case_check_box_list = self.create_check_box("Mixed Case "
                                                               "(Need Letters)")
        self.mixed_case_check_box = self.mixed_case_check_box_list[0]
        self.mixed_case_check_box_layout = self.mixed_case_check_box_list[1]
        self.mixed_case_check_box.setChecked(True)

        self.cuts_check_box_list = self.create_check_box("Cuts")
        self.cuts_check_box = self.cuts_check_box_list[0]
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

        self.generate_button = self.create_push_button(title = "Generate Password", 
                                                       icon = self.GENERATE_ICON, max_width = 500)
        
        self.view_psswd = self.create_push_button(title = "", icon = self.psswd_icon)

        self.copy_psswd_button = self.create_push_button(title = "Copy", 
                                                            icon = self.COPY_NOT_AVAILABLE_ICON)    
        self.copy_psswd_button.setStyleSheet(f"color : {self.NOT_AVAILABLE_COLOR}")

        self.save_psswd_button = self.create_push_button(title = "Save", 
                                                            icon = self.SAVE_NOT_AVAILABLE_ICON)
        self.save_psswd_button.setStyleSheet(f"color : {self.NOT_AVAILABLE_COLOR}")

    # Create Containers : GroupBox and Layouts :

    def create_groupbox(self, title = "Default Groupbox", layout_list = []):
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
    
    def generate_section_essential_properties_layout(self):
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

    def generate_section_optionnal_properties_layout(self):
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
        layout_lists_list = [[self.mixed_case_check_box_layout, self.cuts_check_box_layout], 
                             [self.include_chars_layout, self.exclude_chars_layout]
                             ]
        for layout_list in layout_lists_list : 
            optionnal_sub_layout = QHBoxLayout()
            for layout in layout_list: 
                optionnal_sub_layout.addLayout(layout)
            self.optionnal_layout.addLayout(optionnal_sub_layout)
            self.optionnal_groupbox = self.create_groupbox(title = "Optionnal Settings", 
                                                       layout_list = [self.optionnal_layout])

    def password_display_action(self) : 
        """
        Desc : 
            Section : Generate
            Méthode de création et d'action : 
            Crée un mot de passe à partir de la classe Password importée du module 
            principal "main".
            Set ensuite le mot de passe dans le line edit adéquat.
        Args : 
            None.
        Return : 
            None.
        """
        self.psswd_display = PasswordDisplay(self.psswd_line_edit)
        self.psswd_display.hide()
        self.view_psswd.clicked.connect(self.show_hide_password)

    def generate_section_create_password_layout(self):
        """
        Desc : 
            Section : Generate
            Méthode de création : 
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
        self.generate_button.setMinimumWidth(250)
        self.generate_layout = QVBoxLayout()
        self.generate_layout.addWidget(self.generate_button, alignment = Qt.AlignmentFlag.AlignHCenter)

        # 1) Création du line edit contenant le mot de passe (sans passer par la
        #    méthode disponible car pas besoin de label associé au line_edit)
        # 2) Connection au Slot rendant available ou non les boutons save et copy
        #    en fonction du contenu du line edit

        self.psswd_line_edit = QLineEdit()
        self.psswd_line_edit.setMinimumHeight(self.GENERATE_SECTION_LINE_EDIT_MAXH)
        self.psswd_line_edit.setClearButtonEnabled(True)
        self.psswd_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.psswd_line_edit.textChanged.connect(self.change_save_button_icon)
        
        # Edit du bouton show/view qui permettra de voir ou non le mot de passe :
        # Définition de l'action du bouton : 
        
        self.password_display_action()

        # Création du layout qui accueillera le line edit mais aussi le bouton view/show
        # Ajout du layout line edit au layout principal de generate password et création 
        # du groupbox qui accueillera ce dernier.

        self.psswd_line_edit_layout = QHBoxLayout()
        self.psswd_line_edit_layout.addWidget(self.psswd_line_edit)
        self.psswd_line_edit_layout.addWidget(self.view_psswd)

        self.generate_layout.addLayout(self.psswd_line_edit_layout)

        self.generate_groupbox = self.create_groupbox(title = "Generate Password", 
                                                       layout_list = [self.generate_layout])

    def generate_section_copy_save_buttons_layout(self):
        """
        Desc : 
            Section : Generate
            Méthode de création : 
            Crée la section de copy et save à partir des boutons existants et le layout 
            auquel ces derniers sont associés.
            Ce layout est contenu dans un groupbox.
            
        Args : 
            None.
        Return : 
            None.
        
        """
        # Edit des boutons copy et save et création de leur layout et groupbox: 

        self.copy_psswd_button.setMinimumWidth(150)
        self.copy_button_clicked()
        self.save_psswd_button.setMinimumWidth(150)
        self.save_button_clicked()

        self.validate_buttons_layout = QHBoxLayout()
        self.validate_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.validate_buttons_layout.addWidget(self.copy_psswd_button)
        self.validate_buttons_layout.addWidget(self.save_psswd_button)

        self.validate_buttons_groupbox = self.create_groupbox(title = "", 
                                                              layout_list = [self.validate_buttons_layout])

    # Signals / Actions / Connection Widgets :

    def check_box_clicked(self):
        """
        Desc : 
            Section : Generate
            Méthode de connexion : 
            Connecte la méthode d'évenement "set_box_available" au click de 
            la CheckBox "Letters".
        Args : 
            None.
        Return : 
            None.
        """
        self.letters_check_box.clicked.connect(self.set_box_available)

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
        self.generate_button.clicked.connect(self.create_password)

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
        self.copy_psswd_button.clicked.connect(self.copy_password)

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
        self.save_psswd_button.clicked.connect(self.save_password)

    def add_password_to_json_file(self) : 
        """
        Desc : 
            Section : Generate
            Méthode d'ajout et de sauvegarde : 
            Met à jour le dictionnaire avec les nouvelles entrées et modifie
            entièrement le password_data.json en mettant à jour le fichier.
        Args : 
            None.
        Return : 
            None.
        """
        self.new_ref_to_save_text = self.new_ref_to_save.text()
        self.new_psswd_to_save_text = self.new_psswd_to_save.text()

        self.data_base[self.new_ref_to_save_text] = self.new_psswd_to_save_text
        
        json_dict = json.dumps(self.data_base, indent = 4)
        with open(self.user_data_file, "w") as outfile:
            outfile.write(json_dict)
    
    # Events / Actions :

    @Slot()
    def slider_value_changed(self, value) : 
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
        self.value_label.setText(str(value))

    @Slot()
    def set_box_available(self, value):
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
            self.mixed_case_check_box.setStyleSheet(f"color:{self.NOT_AVAILABLE_COLOR}")

        else : 
            self.mixed_case_check_box.setCheckable(True)
            self.mixed_case_check_box.setStyleSheet(f"color:{self.AVAILABLE_COLOR}")

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
        psswd_display_current_state = str(self.psswd_line_edit.echoMode())
        if psswd_display_current_state == "EchoMode.Password" : 
            self.psswd_display.show()
            self.psswd_icon = self.SHOW_ICON
        else : 
            self.psswd_display.hide()
            self.psswd_icon = self.HIDE_ICON

        self.view_psswd.setIcon(QIcon(self.psswd_icon))

    @Slot()
    def create_password(self) : 
        """
        Desc : 
            Section : Generate
            Méthode d'évènement et de création : 
            Crée un mot de passe à partir de la classe Password.
            Set ensuite le mot de passe dans le line edit adéquat.
        Args : 
            None.
        Return : 
            None.
        """

        self.psswd = main.Password(length = self.lenght_slider.value(), 
                                      include_letters = self.letters_check_box.isChecked(), 
                                      include_numbers = self.numbers_check_box.isChecked(), 
                                      include_special_chars = self.specials_check_box.isChecked(), 
                                      include_mixed_case = self.mixed_case_check_box.isChecked(), 
                                      include_cuts = self.cuts_check_box.isChecked(), 
                                      include_chars = self.include_chars.text(), 
                                      exclude_chars = self.exclude_chars.text()
                                      )
        
        self.psswd = self.psswd.generate()
        self.psswd_line_edit.setText(self.psswd)
        self.psswd_output = self.psswd_line_edit.text()

    @Slot()
    def copy_password(self) : 
        """
            Section : Generate
        Desc : 
            Méthode d'évènement : 
            Permet de copier le mot de passe généré dans le presse-papier à 
            l'aide de tkinter.
        Args : 
            None.
        Return : 
            None.
        """
        self.psswd_output = self.psswd_line_edit.text()

        if self.psswd_output != "" : 
            copy_to_clipboard = tkinter.Tk() # Create Tk object
            copy_to_clipboard.withdraw() # To disable window generated by Tk
            copy_to_clipboard.clipboard_clear()
            copy_to_clipboard.clipboard_append(self.psswd_output)
            copy_to_clipboard.update() # Value stays in the clipboard after window 
                                    # is closed
            copy_to_clipboard.destroy() 

    @Slot()
    def save_password(self):
        """
        Desc : 
            Section : Generate
            Méthode d'évènement et de sauvegarde : 
            Permet d'ajouter à la liste de l'interface les nouvelles entrées :
            - Mot de passe
            - Reference de mot de passe
            Récupère le mot de passe créé, puis ouvre un QDialog pour récupérer
            la référence auprès de l'utilisateur.
            A partir de ces données, on crée le nouveau layout horizontal, 
            Puis on l'ajoute à la QListWidget, 
            Si rien n'est entré dans le QDialog, un QMessageBox s'ouvre pour
            informer l'utilisateur que rien n'a été sauvegardé.
        Args : 
            value (int) : La valeur retournée par le slider.
        Return : 
            None.
        
        """
        # Update list to check validate names : 
        self.data_list_widget = self.get_data_list_widget()
        self.psswd_output = self.psswd_line_edit.text()

        if self.psswd_output : 

            # QInput Dialog to get reference input :
            ref_dialog = QInputDialog()
            ref_dialog.setWindowTitle("Reference Name")
            ref_dialog.setWindowIcon(QIcon(self.main_icon))
            ref_dialog.setLabelText("Password ref name : ")
            ref_dialog.exec()
            self.ref_output = ref_dialog.textValue()

            if self.ref_output : 

                new_row = self.create_existing_passwords_row_layout(ref = self.ref_output, 
                                                                psswd = self.psswd_output)
                self.new_psswd_to_save = new_row[self.PASSWORD_IDX]
                self.new_ref_to_save = new_row[self.REFERENCE_IDX]
                layout = new_row[2]
                self.add_to_password_list(layout, self.saved_section_psswd_listwidget)
                if self.double_name_check :
                    self.add_password_to_json_file()

            else : 
                self.create_warning_box("Saving aborted.")

    @Slot()
    def change_save_button_icon(self, value) : 
        """
        Desc : 
            Section : Generate
            Méthode d'évènement : 
            Utilisée dans : self.generate_section_create_password_layout()

            Change l'icone et la couleur des boutons "Save" et "Copy" en 
            fonction du contenu rempli ou vide du Generate QLineEdit.
        Args : 
            value (str) : La valeur retournée par le QLineEdit.
        Return : 
            None.
        
        """
        if value :
            self.copy_psswd_button.setIcon(QIcon(self.COPY_ICON))
            self.copy_psswd_button.setStyleSheet(f"color:{self.AVAILABLE_COLOR}")
            self.save_psswd_button.setIcon(QIcon(self.SAVE_ICON))
            self.save_psswd_button.setStyleSheet(f"color:{self.AVAILABLE_COLOR}")
        else : 
            self.save_psswd_button.setIcon(QIcon(self.SAVE_NOT_AVAILABLE_ICON))
            self.save_psswd_button.setStyleSheet(f"color : {self.NOT_AVAILABLE_COLOR}")
            self.copy_psswd_button.setIcon(QIcon(self.COPY_NOT_AVAILABLE_ICON))
            self.copy_psswd_button.setStyleSheet(f"color : {self.NOT_AVAILABLE_COLOR}")

    # # Saved Section Construction :

    def create_saved_contents_line_edit(self, 
                                       contents = "DefaultPassword", 
                                       hidden = True, 
                                       read_only = True) : 
        """
        Desc : 
            Section : Saved.
            Méthode de création : 
            Crée un QLine Edit avec un contenu. 
        Args : 
            password_file_url (str) : url du fichier .json contenant les données.
            hidden (bool) : set if password is hidden by default or not.
            read_only (bool) : set Qline Edit read only.

        Return : 
            Un dictionnaire avec comme clé la référence et comme valeur
            le mot de passe associé.
        """
        contents = str(contents)
        saved_contents = QLineEdit(contents)
        saved_contents.setMaximumHeight(self.SAVED_SECTION_LINE_EDIT_MAXH)
        if hidden :
            saved_contents.setEchoMode(QLineEdit.Password)
        if read_only :
            saved_contents.setStyleSheet(f"color:{self.NOT_AVAILABLE_COLOR}")
            saved_contents.setReadOnly(True)
        return saved_contents

    def create_modify_password_button(self):
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            a) Crée le QPushButton qui permet d'éditer les mots de passe pour 
            chaque layout qui se trouve dans la QListWidget de la section 
            "Saved" du programme.
            b) Set une variable de statut "sender_button_contents", 
            qui permettra de savoir le current state du bouton et qui sera
            modifié à chaque click du button.
            c) Set une variable "current_edit_button" permettant de savoir si 
            la session d'édition du mot de passe ou de sa référence est bien 
            fermée (édition d'une ligne à la fois maximum acceptée). A chaque
            passage de la fonction de sauvegarde, cete variable est remise
            à zéro. Elle est checkée à chaque passage de la fonction d'édition.
            Si le bouton cliqué enregistré.

        Args : 
            None.
        Return : 
            Un widget de type QPushButton.
        """

        modify_button = self.create_push_button(title = "", 
                                                icon = self.MODIFY_ICON, 
                                                min_height = self.SAVED_SECTION_BUTTON_MINS, 
                                                min_width = self.SAVED_SECTION_BUTTON_MINS)
        self.sender_button_contents = None
        self.current_edit_button = None

        return modify_button

    def create_delete_password_from_list_button(self):
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
                                                icon = self.TRASH_ICON, 
                                                min_height = self.SAVED_SECTION_BUTTON_MINS, 
                                                min_width = self.SAVED_SECTION_BUTTON_MINS)
        return delete_button

    def create_existing_passwords_row_layout(self, ref, psswd):
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Utilisée dans : self.save_password()
            Utilisée dans : self.create_saved_contents()
            
            Permet de créer le layout complet d'une ligne de QListWidget de
            la section "Saved" : 
                a) Création des deux lineEdit remplis et customisés dans la 
                méthode de création "create_saved_contents_line_edit".
                Ils sont initalisés en not available (méthode en readOnly par 
                défaut).
                b) Création des deux boutons Edit et Delete, et association
                de leur méthode d'evenement respectives
                c) Création du layout horizontal et accueil de tous les 
                widgets.
        Args : 
            ref (str) : Le contenu string déjà présent dans le 
                              dictionnaire self.data_base, ou bien issu de la 
                              fenetre input remplie par l'utilisateur lors de
                              la sauvegarde.
            psswd (str) :  Le contenu string déjà présent dans le 
                              dictionnaire self.data_base, ou bien issu de la 
                              QlineEdit remplie par l'outil lors de la 
                              génération du mot de passe ou de bien directement
                              rempli par l'utilisateur.
        Return : 
            Une liste composée des deux QLineEdit et du layout horizontal.
        """
        psswd_line_edit = self.create_saved_contents_line_edit(contents = psswd)

        ref_line_edit = self.create_saved_contents_line_edit(contents = ref, 
                                                                  hidden = False)

        button_line_edit = self.create_modify_password_button()
        button_line_edit.clicked.connect(self.modify_button_clicked)
        button_line_delete = self.create_delete_password_from_list_button()
        button_line_delete.clicked.connect(self.delete_button_clicked)

        existing_psswds_layout = QHBoxLayout()
        existing_psswds_layout.addWidget(psswd_line_edit)
        existing_psswds_layout.addWidget(ref_line_edit)
        existing_psswds_layout.addWidget(button_line_edit)
        existing_psswds_layout.addWidget(button_line_delete)

        return psswd_line_edit, ref_line_edit, existing_psswds_layout

    def create_saved_contents(self) : 
        """
        Desc : 
            Section : Saved
            Méthode de création : 
            Utilisée dans : self.saved_section_main_layout()
                        
            Permet de créer tous les layouts qui vont servir pour la 
            QListWidget.

        Args : 
            None.
        Return : 
            Une liste composée de tous les layouts horizontaux.
        """
        layout_list = []
        self.data_base = self.get_password_dict_from_json(self.user_data_file)
        for ref, psswd in self.data_base.items() : 
            row = self.create_existing_passwords_row_layout(ref, psswd)
            layout = row[2]
            layout_list.append(layout)
        
        return layout_list
    
    def saved_section_main_layout(self):
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
        layout_list = self.create_saved_contents()
        self.saved_section_psswd_layout = QVBoxLayout()
        self.data_list_widget = []
        self.saved_section_psswd_listwidget = QListWidget()
        self.add_to_password_list(layout_list, self.saved_section_psswd_listwidget)
        self.saved_psswd_groupbox = self.create_groupbox(
            title = "Saved Passwords", 
            layout_list = [self.saved_section_psswd_layout])

    # Data Management Methods :

    def get_password_dict_from_json(self, psswd_file_url): 
        """
        Desc : 
            Section : Saved
            Méthode d'acquisition : 
            Utilisée dans : self.create_saved_contents()
            
            Permet de récupérer les mots de passe présents dans le fichier
            json.
        Args : 
            psswd_file_url (str) : url du fichier .json contenant les 
                                      données.
        Return : 
            Un dictionnaire avec comme clé la référence et comme valeur
            le mot de passe associé.
        """
        psswd_file = open(psswd_file_url)
        psswd_data = json.load(psswd_file)
        return psswd_data

    def save_password_dict_to_json(self, psswd_file_url): 
        """
        Desc : 
            Section : Saved
            Méthode de sauvegarde : 
            Utilisée dans : self.save_line_edit_changes()

            Permet d'update le fichier json avec le nouveau dictionnaire 
            de stockage "self.data_base", recréé des widgets de la liste 
            trouvés grâce aux items de la liste associés 
            (# Found QWidget in QListWidget).
        Args : 
            psswd_file_url (str) : url du fichier .json contenant les 
                                      données.
        Return : 
            None.
        
        """
        self.data_base = {}
        list_contents = self.get_widget_list(self.saved_section_psswd_listwidget)
        for widget in list_contents : 
            line_edit_children_list = widget.findChildren(QLineEdit)
            psswd = line_edit_children_list[self.PASSWORD_IDX].text()
            ref = line_edit_children_list[self.REFERENCE_IDX].text()
            self.data_base[ref] = psswd

        json_dict = json.dumps(self.data_base, indent = 4)
        with open(psswd_file_url, "w") as outfile:
            outfile.write(json_dict)

    def remove_password_from_json_dict(self) : 
        """
        Desc : 
            Section : Saved
            Méthode de suppression et de sauvegarde : 
            Utilisée dans : self.delete_button_clicked()

            Met à jour les dictionnaires avec les nouvelles entrées et modifie
            entièrement le password_data.json en mettant à jour le fichier.
        Args : 
            None.
        Return : 
            None.
        """
        if self.delete_confirm :
            self.data_base.pop(self.ref_to_delete)
            
            json_dict = json.dumps(self.data_base, indent = 4)
            with open(self.user_data_file, "w") as outfile:
                outfile.write(json_dict)

    # Security :

    def validate_double_reference_names(self, widget):
        """
        Desc : 
            Section : Saved
            Méthode de vérification : 
            Utilisée dans : self.save_line_edit_changes()
                            add_to_password_list()
                        
            Permet de checker les doublons de nom de référence d'un widget 
            contenant deux QLineEdit.
        Args : 
            widget(QWidget) : Le layout horizontal contenant 2
                              QLineEdit.
        Return : 
            unique_name_checked (bool) : Un booléen qui informe du statut
                                         du check.
        """
        unique_name_checked = True
        widget_children = widget.findChildren(QLineEdit)
        ref = widget_children[1].text()
        if ref in self.data_list_widget :
            self.create_warning_box(f"\"{ref}\" already exists as reference.\n"
                                    "Please enter a unique name.")
            unique_name_checked = False
        return unique_name_checked

    # Events / Actions :

    def add_to_password_list(self, layout_list, listwidget):
        """
        Desc : 
            Section : Saved
            Méthode d'ajout : 
            Utilisée dans : self.saved_section_main_layout()
                        
            Permet d'ajouter à une QListWidget une liste de layout: 
                a) Création d'un QWidget qui sert ensuite à encapsuler le 
                layout.
                b) Création d'un QListWidgetItem qui va permettre de placer
                dans la QListWidget le QWidget.
                c) Set de la size du WidgetItem en fonction de celle du layout
                d) Check des doublons dans la liste
                e) Ajout de WidgetItem dans la QListWidget
                f) Association du QWidget au WidgetItem
                g) Une fois la boucle terminée, ajout du widget mis à jour 
                   dans le layout principal de la section "Saved".
        Args : 
            None.
        Return : 
            None.
        """
        if not isinstance(layout_list, list) : 
            layout_list = [layout_list]
        for layout in layout_list : 
            widget_layout = QWidget()
            widget_layout.setLayout(layout)
            children = widget_layout.findChildren(QLineEdit)
            ref = [x.text() for x in children][1]
            item_list = QListWidgetItem()
            item_list.setSizeHint(widget_layout.sizeHint())
            # Check unique reference name 
            self.double_name_check = self.validate_double_reference_names(widget_layout)
            if not self.double_name_check :
                return
            self.data_list_widget.append(ref)
            listwidget.addItem(item_list)
            listwidget.setItemWidget(item_list, widget_layout)
        # print("data list is", self.data_list_widget)

        self.saved_section_psswd_layout.addWidget(self.saved_section_psswd_listwidget)

    def remove_password_from_list(self, row_int) : 
        """
        Desc : 
            Section : Saved
            Méthode d'action : 
            Utilisée dans  : self.delete_button_clicked()

            Ouvre une fenêtre de confirmation lors de la suppression de
            la colonne. 
            Supprime la colonne dont le numéro a été initialisé lors du
            passage de la fonction self.delete_button_clicked()  : 
                
        Args : 
            row_int (int) : Numéro de ligne de la QListWidget, 
                            initialisé lors du passage de la fonction 
                            self.delete_button_clicked().
        Return : 
            None.
        """
        self.delete_confirm = self.create_confirm_box("Delete this password?")
        if self.delete_confirm : 
            self.saved_section_psswd_listwidget.takeItem(row_int)
        else : 
            return
            # self.create_warning_box("Delete aborted.")  

    def make_line_edit_editable(self, widget_list) : 
        """
        Desc : 
            Section : Saved
            Méthode d'action : 
            Utilisée dans  : self.modify_button_clicked()
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
                widget.setStyleSheet(f"color:{self.AVAILABLE_COLOR}")
                widget.setReadOnly(False)
                widget.setEchoMode(QLineEdit.Normal)

    def save_line_edit_changes(self, widget_list) : 
        """
        Desc : 
            Section : Saved
            Méthode d'action : 
            Utilisée dans  : self.modify_button_clicked()
            1) Modifie le display et le statut des QLine Edit quand le 
            bouton au statut "Save" est cliqué : 
                a) Set les QlineEdit en readOnly
                b) Change la couleur du texte pour indiquer le non-available
                c) Change l'echoMode de celui identifié comme le password 
                pour cacher le texte.
            2) Effectue les vérifications d'usage et sauvegarde les changements :
                a) Vérifie s'il y a des changements dans les line_edits.
                b) Vérifie les doublons.
                c) Ouvre une fenetre de confirmation.
                d) Passe la méthode qui permet d'update le fichier json.
        Args : 
            widget_list (list) : liste des QlineEdit du parent du button cliqué.
        Return : 
            None.
        """
        self.current_edit_button = None

        for widget in widget_list :
            widget.setReadOnly(True)
            widget.setStyleSheet(f"color:{self.NOT_AVAILABLE_COLOR}")

        current_psswd = widget_list[self.PASSWORD_IDX]
        current_ref = widget_list[self.REFERENCE_IDX]
        current_psswd.setEchoMode(QLineEdit.Password)

        if current_psswd.text() != self.init_psswd \
        or current_ref.text() != self.init_ref:
            widget_parent = current_psswd.parentWidget()
            # Check unique reference name 
            self.double_name_check = self.validate_double_reference_names(widget_parent)
            if self.double_name_check :
                confirmed = self.create_confirm_box("Save modifications?")
                if confirmed :
                    self.save_password_dict_to_json(self.user_data_file)
                else : 
                    current_psswd.setText(self.init_psswd)
                    current_ref.setText(self.init_ref)
            else : 
                current_psswd.setText(self.init_psswd)
                current_ref.setText(self.init_ref)
        else : 
            return
        
    # Signals / Actions / Connection Widgets :

    @Slot()
    def modify_button_clicked(self) : 
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

        if self.sender_button_contents == None : 
            self.sender_button_contents = "Edit"

        if self.current_edit_button == None : 
            self.current_edit_button = sender_button
        else: 
            # Check line edition mode closed : 
            if self.current_edit_button != sender_button : 
                print("Previous edit section not closed")
                self.create_warning_box("Please save present edition.")
                return 
            else : 
                pass
        
        button_parent = sender_button.parentWidget() # Trouve le parent du 
                                                     # bouton émeteur, ici  
                                                     # c'est un Qwidget
        line_edit_list = button_parent.findChildren(QLineEdit)

        if self.sender_button_contents == "Edit" :
            # Update list to check validate names : 
            self.data_list_widget = self.get_data_list_widget()
            # Get init password and reference and make line editable
            self.init_sender_button = self.sender()
            self.init_psswd = line_edit_list[self.PASSWORD_IDX].text()
            self.init_ref = line_edit_list[self.REFERENCE_IDX].text()
            sender_button.setIcon(QIcon(self.SAVE_ICON))
            self.make_line_edit_editable(line_edit_list)
            # Change sender button status
            self.sender_button_contents = "Save"

        elif self.sender_button_contents == "Save" : 
            sender_button.setIcon(QIcon(self.MODIFY_ICON))
            self.save_line_edit_changes(line_edit_list)
            self.sender_button_contents = "Edit"

    @Slot()
    def delete_button_clicked(self) : 
        """
        Desc : 
            Section : Saved
            Méthode d'évènement : 
            Permet de retrouver la ligne correspondante au bouton cliqué
            ainsi que la référence du mot de passe correspondant, afin de 
            pouvoir lancer les méthodes d'actions permettant de supprimer
            la ligne visée.
        Args : 
            None.
        Return : 
            None.
        """
        sender_button = self.sender()
        # Check line edition mode closed : 
        if self.current_edit_button != None : 
            self.create_warning_box("Please save present edition.")
            return
        button_parent = sender_button.parentWidget()
        list_range = self.saved_section_psswd_listwidget.count()
        for idx in range(list_range) : 
            widget_item = self.saved_section_psswd_listwidget.item(idx)
            widget = self.saved_section_psswd_listwidget.itemWidget(widget_item)
            if button_parent == widget :
                widget_children = widget.findChildren(QLineEdit)
                self.psswd_to_delete = widget_children[self.PASSWORD_IDX].text()
                self.ref_to_delete = widget_children[self.REFERENCE_IDX].text()
                row_to_delete = self.saved_section_psswd_listwidget.row(widget_item)
                self.remove_password_from_list(row_to_delete)
                self.remove_password_from_json_dict()
                # Update list to check validate names : 
                self.data_list_widget = self.get_data_list_widget()

    # Create Main Containers > Tabs :

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
        for title, list_items in tab_dict.items() : 
            main_widget = QWidget()
            tab.addTab(main_widget, title)
            if direction == "V" : 
                main_layout = QVBoxLayout()
            elif direction == "H" : 
                main_layout = QHBoxLayout()
            else : 
                raise ValueError("ERROR : La direction ne peut être que \"V\""
                                 " ou \"H\"")
            
            if list_items : 
                for item in list_items : 
                    if isinstance(item, QWidget) or isinstance(item, QGroupBox) : 
                        main_layout.addWidget(item)
                    if isinstance(item, QVBoxLayout) or isinstance(item, QHBoxLayout) : 
                        main_layout.addLayout(item)
            
            main_widget.setLayout(main_layout)
        
        return tab

    def tabs_main_layout(self) : 
        """
        Desc : 
            Section : MainWindow
            - Fonction principale pour créer les onglets à partir du dictionnaire de tabs, 
            composé du nom de la tab et d'une liste de GroupBox.
            - Intègre ensuite ces tabs au widget central.
        Args : 
            None.

        Return : 
            None.
        """
        all_tabs_dict = {
                        "Generate":[self.essential_groupbox, 
                                        self.optionnal_groupbox, 
                                        self.generate_groupbox, 
                                        self.validate_buttons_groupbox
                                        ], 
                        "Saved":[self.saved_psswd_groupbox
                                    ]}
        self.all_tabs = self.create_menu_tab(tab_dict = all_tabs_dict)
        self.central_layout.addWidget(self.all_tabs)

# SUITE - 
#       - TRIER LES METHODES DE LA SECTION SAVED POUR QU'ELLES SOIENT 
#         COHERENTES AVEC LES METHODES DE LA SECTION GENERATE.
#       - FAIRE UN CHECK PEP 8

# EXTRA - AJOUTER LE MOT DE PASSE DE LA SESSION WINDOWS POUR ACCEDER AUX
#         INFORMATIONS SENSIBLES (Mot de passe cachés)

def create_main_window() : 
    app = QApplication(sys.argv)
    main_icon = sys.argv[1] if len(sys.argv) > 1 else "icons/logo.ico"
    main_title = "Password Manager"
    main_window = myWindow(main_title, main_icon)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__" : 
    import main
    create_main_window()
else : 
    import modules.main as main
