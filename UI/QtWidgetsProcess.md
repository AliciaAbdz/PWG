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

# Found QWidget in QListWidget :

On peut trouver le QWidget correspondant au bouton cliqué en passant par deux méthodes successives de la classe QListWidget :
QListWidget.item(int) 
QListWidget.itemWidget(QListWidgetItem)

Elles s'utilisent comme suit dans le contexte suivant :
On utilise une QListWidget "list_widget_item" contenant des layouts encapsulés dans des QWidget comme plus haut, et associés à des QWidgetItem.

## Python : 

list_lenght = list_widget_item.count()
list_content_widget = []
for idx in range(list_lenght) :
        widget_item = list_widget_item.item(idx)
        widget = list_widget_item.itemWidget(widget_item)
        list_content_widget.append(widget)

On obtient une liste de tous les items présents dans la QListWidget. On peut alors utiliser la méthode .findChildren pour retrouver les composants spécifiques qui nous intéresse. 
On peut aussi l'utiliser pour trouver quel QWidgetItem correspond par exemple au bouton cliqué (pour dans le cas où on aurait besoin d'un bouton qui permet supprimer sa ligne de liste)