**Ceci est une doc pour référencer les process de création de Widget utilisés dans cet exo**

## QTabWidget :

Voici le premier test de création d'onglet avec **QTabWidget** et voici sa procédure : 

1) Création du widget Tab qui va contenir tous les onglets : 

tab = QTabWidget()
for x in range(nombre_donglets_souhaités) : 

2) Création des widgets composant cet onglet : 

button_test_01 = QPushButton("Button 01")
button_test_02 = QPushButton("Button 01")

3) Création du layout qui va accueillir les widgets enfants : 
widget_test_layout = QVBoxLayout()
widget_test_layout.addWidget(button_test_01)
widget_test_layout.addWidget(button_test_02)

4) Création du Widget principal : 
widget_test = QWidget()

5) Ajout d'un onglet à partir du Widget principal :
tab.addTab(widget_test,"Onglet de test")

6) Ajout du layout dans le Widget principal : 
widget_test.setLayout(widget_test_layout)

# Python : 
        """ Voici le premier test de création d'onglet """

        # push_button_1 = QPushButton("Button_01")
        # push_button_2 = QPushButton("Button_02")

        # push_button_3 = QPushButton("Button_03")
        # push_button_4 = QPushButton("Button_04")  
        # test_dict = {
        #             "Onglet 1" : [push_button_1,push_button_2],
        #             "Onglet 2" : [push_button_3,push_button_4]
        # }
        # self.create_tab = self.create_menu_tab(tab_dict = test_dict)
        # self.central_layout.addWidget(self.create_tab)