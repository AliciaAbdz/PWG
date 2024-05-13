**Ceci est une doc pour référencer les process de création de Widget utilisés dans cet exo**

# QTabWidget :

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

## Python : 
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

# Add Icon to QLineEdit : 

Voici comment ajouter une icone dans un QLineEdit :

## Python : 

        self.password_line_edit.addAction(QIcon(self.password_line_edit_icon),self.password_line_edit.ActionPosition.LeadingPosition)

# Find children of a any QObject(inherited by QWidget) : 

On peut trouver les widgets (et pas layouts) enfants d'un widget en utilisant la méthode "findChildren" qui prend en argument le type d'enfants qu'on cherche:

## Python : 
child_button = QPushButton("Button")
main_layout = QHBoxLayout()
parent_widget = QWidget()

main_layout.addWidget(child_button)
parent_widget.setLayout(main_layout)

child_list = parent_widget.findChildren(QPushButton)

""" /!\ Attention, ici l'appel de la méthode "findChildren" donnera comme résultat le child_button et non le main_layout ! """


# Add layout to QListWidget : 

On ne peut pas ajouter directement une liste de QLayout (VBox ou HBox par exemple) à un QListWidget. 
Il faut l'encapsuler dans un QWidget, et l'utiliser de paire avec un QListWidgetItem() pour pouvoir l'intégrer tranquillement dans le QListWidget ;
Voici la marche à suivre : 

Pour une liste de layout "layout_list" : 

## Python : 

main_layout = QVBoxLayout()

layout_list = [Hlayout1,Hlayout2,Hlayout3]
listwidget = QListWidget()

for layout in layout_list : 
        widget_layout = QWidget()
        item_list = QListWidgetItem()

        widget_layout.setLayout(layout)
        item_list.setSizeHint(widget_layout.sizeHint())

        listwidget.addItem(item_list)
        listwidget.setItemWidget(item_list,widget_layout)

main_layout.addWidget(listwidget)