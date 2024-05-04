# PEP---80-characters-80-characters-80-characters-80-characters-80-characters---
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, \
                              QTabWidget, QLayout, QHBoxLayout, QVBoxLayout, QGroupBox, \
                              QSlider, QCheckBox, QPushButton, QLabel, QLineEdit
                                
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

        # Window construction :

        self.create_central_widget()
        self.create_all_items()
        self.create_essential_properties_layout()
        self.create_optionnal_properties_layout()
        self.create_main_layout()

    def create_central_widget(self) : 
        """
        Desc : 
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
        self.setMinimumSize(460,250)

    # Widgets in Layouts : Definitions :
    
    def create_lenght_slider(self, title = "Default slider", min = 4, max = 50) : 
        """
        Desc : 
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

        return line_edit,line_edit_layout

    def create_push_button(self, title = None, icon = None, 
                           min_height = 40, max_width = 1000) : 
        """
        Desc : 

        Args : 

        Return : 
        
        """
        push_button = QPushButton(title,icon=(QIcon(icon)))
        push_button.setMinimumHeight(min_height)
        push_button.setMaximumWidth(max_width)

        return push_button
        

    def create_label(self, title = "Default") : 
        """
        Desc : 

        Args : 

        Return : 
        
        """
        
        pass
    
    # Create Widgets Application :

    def create_all_items(self) : 
        """
        Desc : 
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

        self.numbers_check_box_list = self.create_check_box("Numbers")
        self.numbers_check_box = self.numbers_check_box_list[0]
        self.numbers_check_box_layout = self.numbers_check_box_list[1]

        self.specials_check_box_list = self.create_check_box("Specials")
        self.specials_check_box = self.specials_check_box_list[0]
        self.specials_check_box_layout = self.specials_check_box_list[1]

        self.mixed_case_check_box_list = self.create_check_box("Mixed Case (Need Letters)")
        self.mixed_case_check_box = self.mixed_case_check_box_list[0]
        self.mixed_case_check_box_layout = self.mixed_case_check_box_list[1]
        self.mixed_case_check_box.setCheckable(False)
        self.mixed_case_check_box.setStyleSheet("color:#bcbcbc")

        self.cuts_check_box_list = self.create_check_box("Cuts")
        self.cuts_check_box= self.cuts_check_box_list[0]
        self.cuts_check_box_layout = self.cuts_check_box_list[1]

        self.lenght_slider_list = self.create_lenght_slider("Length")
        self.lenght_slider = self.lenght_slider_list[0]
        self.lenght_slider_layout = self.lenght_slider_list[1]

        self.include_chars_list = self.create_line_edit("Include")
        self.include_chars = self.include_chars_list[0]
        self.include_chars_layout = self.include_chars_list[1]

        self.exclude_chars_list = self.create_line_edit("Exclude")
        self.exclude_chars = self.exclude_chars_list[0]
        self.exclude_chars_layout = self.exclude_chars_list[1]

        self.create_generate_password_layout()

    # Create Main Containers : Tabs :

    def create_menu_tab(self, tab_dict = {"Default_Title" : []}, direction = "V") : 
        """
        Desc : 
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
    
    def create_main_layout(self) : 
        """
        Desc : 
            Créer un GroupBox contenant un ou plusieurs layout(s).
        Args : 
            title (str) : Le titre du GroupBox.

            layout_list (lst) : Une liste contenant les layouts à ajouter dans 
                                le GroupBox.
        Return : 
            Un objet "groupbox" de type GroupBox.
        
        """
        create_tab_dict = {
                            "Create":[self.essential_groupbox,self.optionnal_groupbox,
                                      self.generate_groupbox],
                            "Saved":[]}
        self.create_tab = self.create_menu_tab(tab_dict=create_tab_dict)
        self.central_layout.addWidget(self.create_tab)

    def create_essential_properties_layout(self):
        """
        Desc : 
            Crée la section de parametre essentiels pour le programme.
            Crée un GroupBox contenant un ou plusieurs layout(s). 
            En vue d'être ajouté plus tard à une tab dans la fonction create_main_layout()
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

    def create_optionnal_properties_layout(self):
        """
        Desc : 
            Crée la section de parametre optionnels pour le programme.
            Crée un GroupBox contenant un ou plusieurs layout(s). 
            En vue d'être ajouté plus tard à une tab dans la fonction create_main_layout()
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
    
    def create_generate_password_layout(self):

        generate_icon = "icons/update.ico"
        self.generate_button_layout = QVBoxLayout()
        self.generate_button = self.create_push_button(title = "Generate Password", 
                                                       icon = generate_icon,max_width=500)
        self.generate_button.setMinimumWidth(250)
        self.generate_button_layout.addWidget(self.generate_button,alignment = Qt.AlignmentFlag.AlignHCenter)
        self.generate_groupbox = QGroupBox()
        self.generate_groupbox.setLayout(self.generate_button_layout)

    def create_build_section_groupbox(self, layout_list = []):

        pass

    def create_copy_save_buttons_layout(self, widget_list = []):
        
        pass

    # Actions / Event / Connection Widgets :

    @Slot()
    def slider_value_changed(self,value) : 
        """
        Desc : 
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

    def check_box_clicked(self):
        """
        Desc : 
            Méthode de connexion : 
            Connecte la méthode d'évenement "make_box_available" au click de 
            la CheckBox "Letters".
        Args : 
            None.
        Return : 
            None.
        
        """
        self.letters_check_box.clicked.connect(self.make_box_available)
    
    @Slot()
    def make_box_available(self,value):
        """
        Desc : 
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
            self.mixed_case_check_box.setStyleSheet("color:#bcbcbc")

        else : 
            self.mixed_case_check_box.setCheckable(True)
            self.mixed_case_check_box.setStyleSheet("color:#000000")

if __name__ == "__main__" : 
    app = QApplication(sys.argv)
    main_icon = sys.argv[1] if len(sys.argv) > 1 else "icons/logo.ico"
    main_title = "Password Generator"
    main_window = myWindow(main_title,main_icon)
    main_window.show()
    sys.exit(app.exec())