# PEP---80-characters-80-characters-80-characters-80-characters-80-characters---

import random
import string
import warnings

class Password: 

    def __init__(self, 
                 length = 4, 
                 include_letters = True, 
                 include_numbers = True, 
                 include_special_chars = True, 
                 include_mixed_case = True, 
                 include_cuts = False, 
                 exclude_chars = "", 
                 include_chars = "" 
                 ) :
        
        self.length = length
        self.include_letters = include_letters
        self.include_numbers = include_numbers
        self.include_special_chars = include_special_chars
        self.include_mixed_case = include_mixed_case
        self.include_cuts = include_cuts
        self.exclude_chars = self.__get_sorted_chars_string(exclude_chars)
        self.include_chars = self.__get_sorted_chars_string(include_chars)

        self.__validate_user_datas()
        self.__get_password_chars_library()

    # Methods : User Data Manipulation :

    def __get_sorted_list_from_string(self, chars_string) : 
        """ 
        Convertit une chaine de caractères en liste triée.

        Args : 
            chars_string(str) : La chaine de caractères à convertir.

        Returns : 
            Une liste triée des caractères de la chaine.
        """

        sorted_list = sorted( [char for char in chars_string] )
        set(sorted_list)
        return sorted_list

    def __get_sorted_chars_string(self, chars_string) : 
        """ 
        Trie une chaine de caractères.

        Args : 
            chars_string(str) : La chaine de caractères à trier.

        Returns : 
            Une chaine de caractères triée.
        """
        sorted_chars_list = self.__get_sorted_list_from_string(chars_string)
        sorted_chars_string = ""

        for char in sorted_chars_list : 
            sorted_chars_string += str(char)

        return sorted_chars_string

    # Methods : User Data Validation :

    def __validate_user_datas(self) : 

        self.__validate_essential_parameters()
        self.__validate_optional_parameters_requirements()
        self.__get_initial_chars_library()
        self.__clean_special_chars()
        self.__validate_exclude_all_chars()
        self.__validate_conflicts_include_exclude()

    def __validate_essential_parameters(self) : 
        """ 
        Permet de valider qu'au moins un paramètre essentiel "Lettre", "Number" ou 
        "Spécial" est actif.

        Args : 
            Self.

        Returns : 
            None.
        """
        essentials_parameters = [
                                 self.include_letters, 
                                 self.include_numbers, 
                                 self.include_special_chars
                                 ]
    
        if not any(essentials_parameters) : 
            raise Exception("Le mot de passe doit contenir au moins des lettres, "
                            " des chiffres, ou des caractères spéciaux !")

    def __validate_optional_parameters_requirements(self) : 
        """ 
        Permet de valider que si les paramètres "Mixed Case" et/ou "cuts" sont actifs, 
        le paramètre essentiel "Lettre" l'est aussi.

        Args : 
            Self.

        Returns : 
            None.
        """
        if self.include_mixed_case or self.include_cuts : 
            if not self.include_letters : 
                raise ValueError("Mixed Case et cuts ne marchent qu'avec, au minimum, "
                                 "des lettres !")

    def __get_initial_chars_library(self) : 

        """ 
        Permet de valider que si les paramètres "Mixed Case" et/ou "cuts" sont actifs, 
        le paramètre essentiel "Lettre" l'est aussi.

        Args : 
            Self.

        Returns : 
            None.
        """

        self.all_letters = ""
        self.all_numbers = ""
        self.all_specials = ""
        
        if self.include_letters : 
            self.all_letters = string.ascii_lowercase

        if self.include_numbers : 
            self.all_numbers = string.digits

        if self.include_special_chars : 
            self.all_specials = string.punctuation

        if self.include_letters and self.include_mixed_case : 
            self.all_letters = string.ascii_letters

        self.all_chars = self.all_letters + self.all_numbers + self.all_specials
        self.all_chars = self.__get_sorted_chars_string(self.all_chars)

    def __clean_special_chars(self) : 
        """ 
        Exclu les caractères spéciaux trop complexes de la librairie finale.
        Si "Cuts" est actif, il retire également les symboles "_" et "-" qui servent de
        séparateurs.

        Args : 
            Self.

        Returns : 
            None.
        """
        complex_special_strings = "\"'()*, -./:;[\\]^_`{|}"
        if not self.include_cuts : 
            complex_special_strings = complex_special_strings.replace("_", "").replace("-", "")
        for char in self.all_chars : 
            if char in complex_special_strings : 
                self.all_chars = self.all_chars.replace(char, "")
        
        print("All chars are >>>", self.all_chars)

    def __validate_exclude_all_chars(self):
        """ 
        Permet de valider que le paramètre "Exclude" n'exclut pas toute la chaine de 
        caractères générées par les paramètres essentiels.

        Args : 
            Self.

        Returns : 
            None.
        """
        if self.all_chars == self.exclude_chars :
            raise ValueError("La section \"Exclude\" comporte tous les caractères "
                             "sélectionnés !")
        
    def __validate_conflicts_include_exclude(self):
        """ 
        Permet de valider les conflits entre les paramètres "Include" et "Exclude":
            - 1) Raise une Execption s'ils sont exactement similaires.
            - 2) Exclu automatiquement les caractères similaires entre les deux
              chaines de caractères.

        Args : 
            Self.

        Returns : 
            None.
        """
        if self.include_chars and self.exclude_chars : 
            
            """ 1) : Raise une Execption s'ils sont exactement similaires. """

            if self.include_chars == self.exclude_chars :
                raise ValueError("Les listes d'inclusion et d'exclusion sont similaires")
            
            """ 2) : Exclu automatiquement les caractères similaires entre les deux
              chaines de caractères """

            include_chars_list = self.__get_sorted_list_from_string(self.include_chars)
            exclude_chars_list = self.__get_sorted_list_from_string(self.exclude_chars)
            
            # Need to find longest list to correctly compare in the next for loop.
            if not len(include_chars_list) == len(exclude_chars_list) : 

                longest_list = include_chars_list \
                            if len(include_chars_list) > len(exclude_chars_list)\
                            else exclude_chars_list
                
                shortest_list = include_chars_list \
                            if len(include_chars_list) < len(exclude_chars_list)\
                            else exclude_chars_list
            else : 
                longest_list = include_chars_list
                shortest_list = exclude_chars_list

            # Create a list to exclude similar elements.
            exclude_from_password = []

            for char in longest_list : 
                if char in shortest_list : 
                    if char not in exclude_from_password :
                        exclude_from_password.append(char)
            
            # Modify self.include_chars to remove similar elements.
            for char in exclude_from_password : 
                self.include_chars = self.include_chars.replace(char, "") 
                self.exclude_chars = self.exclude_chars.replace(char, "") 

            # Warn the user about auto exclusion.
            warnings.warn(f"Characters {exclude_from_password} are automatically "
                          f"excluded from password. \nAre only included "
                          f"\"{self.include_chars}\" characters.", stacklevel=2)
            
    # Methods : Character Library Generation : 

    def __get_password_chars_library(self) : 
        """ 
        Permet créer une librarie de caractères servant pour la création du mot de
        passe.

        Args : 
            Self.

        Returns : 
            None.
        """
        self.password_chars_library = self.all_chars + self.include_chars

        for char in self.exclude_chars : 
            self.password_chars_library = self.password_chars_library.replace(char, "")

        self.password_chars_library = list(self.password_chars_library)
        self.__separate_chars_category()

    def __separate_chars_category(self):
        """ 
        1) Permet créer différentes catégories de libraries en fonction de leurs
        caractéristiques. 
        2) Permet également de créer une liste contenant les informations sur le 
        nombre de parametres différents dans le mot de passe "chars_type_available".


        Args : 
            Self.

        Returns : 
            None.
        """

        """ 1) Permet créer différentes catégories de libraries en fonction de leurs
        caractéristiques. """

        self.password_letter_chars = [
                                    char for char in self.all_chars if 
                                    char in string.ascii_letters
                                    ]
        self.password_number_chars = [
                                    char for char in self.all_chars if 
                                    char in string.digits
                                    ] 
        self.password_special_chars = [
                                    char for char in self.all_chars if 
                                    char in string.punctuation
                                    ]
        
        self.password_category_list = []

        for list in [
                     self.password_letter_chars, 
                     self.password_chars_library, 
                     self.password_special_chars
                     ] :
            
            if list : 
                self.password_category_list.append(list)

        """ 2) Permet également de créer une liste contenant les informations sur le 
        nombre de parametres différents dans le mot de passe "chars_type_available". """

        self.chars_type_available = [ x + 1 for x in range(len(self.password_category_list)) ]
        self.chars_type_available_length = len(self.chars_type_available)

    def __apply_cuts(self, password, separator="-") : 
        """ 
        Permet à partir d'un mot de passe déjà créé de générer un autre mot de passe mais
        séquencé et coupé par un séparateur unique.
        Ne fonctionne qu'avec un nombre minimum de caractères (8 par défaut).
        Les séparateurs sont placés de manière redondante et calculée aléatoirement
        selon la longueur initiale du mot de passe et un diviseur arbitraire.

        Une fois cette redondance calculée en terme d'index dans la liste de caractères
        composant le mot de passe, cette dernière est modifiée puis transformée en variable
        de type string qui surcharge le paramètre "password". Cette variable est ensuite 
        retournée à la sortie de la fonction.
        
        Args : 
            password(str) : La chaine de caractères à séquencer.
            separator(str) : Le caractère séparateur.

        Returns : 
            Une chaine de caractère string représentant le mot de passe final .
            
        """

        password_list = list(password)

        if self.length >= 8 :
            if self.include_cuts : 
                min_cut_percentage = int(self.length/4)
                max_cut_percentage = int(self.length/2)
                random_cut_percentage = random.randint(min_cut_percentage, 
                                                            max_cut_percentage)
        else : 
            warnings.warn("Cuts ignored, only available with minimum lenght of 8 characters", 
                          stacklevel=2)

        idx_replace_position_list = list(range(self.length))
        idx_replace_position_list = idx_replace_position_list[0::random_cut_percentage] 
                                    # pour prendre en compte le premier caractère.
        idx_replace_position_list.remove(0) # pour ne pas modifier le premier caractère

        for idx, value in enumerate(password_list) : 
            if idx in idx_replace_position_list : 
                password_list[idx-1] = separator

        password = ""

        for char in password_list : 
            password+=char
        
        return password

    def generate(self) : 

        """ 
        Génère un premier tour de séquence chiffrée pour créer plus tard le mot de passe. 
        Un chiffre random est généré dans l'espace de nombre entre 1 et le nombre de parametres 
        selectionnés par l'utilisateur. 
        Il est ensuite ajouté à la séquence chiffrée qui permettra de composer le mot de passe.
        Un second tour de sécurité est lancé si un des parametres n'a pas été généré durant 
        le premier tour.
        Si "Cuts" est actif, on lance la fonction qui lui est associé.

        Args : 
            Self.

        Returns : 
            None.
        """

        self.password = ""
        self.final_number_sequence = []

        # Generate first round of securated number sequence :
        for idx in range(self.length) :
            random_number = random.randrange(1, self.chars_type_available_length + 1)
            # Sans + 1, la génération skip toujours le dernier paramètre
            self.final_number_sequence.append(random_number)

        self.final_number_sequence_length = len(self.final_number_sequence) - 1

        # Generate second round of securated number sequence if not all chars type available
        # in final number sequence :
        for num in self.chars_type_available : 
            final_number_sequence_set = sorted(self.final_number_sequence)
            final_number_sequence_set = list(set(final_number_sequence_set))

            if num not in self.final_number_sequence : 
                random_place_in_list = random.randint(1, self.final_number_sequence_length)
                self.final_number_sequence.pop(random_place_in_list)
                self.final_number_sequence.insert(random_place_in_list, num)
                # Update final number sequence set
                final_number_sequence_set = sorted(self.final_number_sequence)
                final_number_sequence_set = list(set(final_number_sequence_set))

        # Generate full securated password :
        values_dict = {
                        1:self.password_letter_chars, 
                        2:self.password_number_chars, 
                        3:self.password_special_chars
                        }

        for idx in self.final_number_sequence :
            for key, character_type in values_dict.items() :
                if idx == key : 
                    pick_char = random.choice(character_type if character_type else "")
                    self.password += pick_char

        # Generate cuts securated password :
        if self.include_cuts : 
            self.password = self.__apply_cuts(password = self.password)

        print("Generated password is :", self.password)

if __name__ == "__main__" : 

    password = Password(length = 20, 
                        include_letters = True, 
                        include_numbers = True, 
                        include_special_chars = False, 
                        exclude_chars = "", 
                        include_chars = "", 
                        include_mixed_case = True, 
                        include_cuts = True)

    password.generate()
