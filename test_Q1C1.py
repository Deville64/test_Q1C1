import csv
import os
import unicodedata

# Fonction pour afficher le menu d'accueil
def display_menu():
    print("Menu d'accueil:")
    print("1. Afficher les immeubles")
    print("2. Rechercher")

# Fonction pour fusionner les fichiers CSV dans un dossier
def merge_csv_files(path):
    csv_data = []
    unique_data = []

    try:
        # Parcours tous les fichiers dans le chemin pour tout mettre dans une liste
        for file_name in os.listdir(path):
            if file_name.endswith('.csv'):
                with open(os.path.join(path, file_name), 'r', encoding='utf-8') as csv_file:
                    reader = csv.DictReader(csv_file)
                    csv_data.extend(reader)
            
            else:
                print(f"{file_name} ignoré car ce n'est pas un fichier CSV.")
        
        # Suppression des doublons des données fusionnées
        for element in csv_data:
            if element not in unique_data:
                unique_data.append(element)

        return unique_data

    except FileNotFoundError:
        print(f"Le chemin '{path}' n'existe pas.")
        return 

# Fonction pour afficher la liste des immeubles
def display_buildings():
    csv_data = merge_csv_files('data')
    # Tri des données fusionnées par numéro d'immeuble puis par nom de propriétaire
    sorted_data = sorted(csv_data, key=lambda x: (int(x['building_id']), x['lastname']))

    #Affichage
    print("\nListe des immeubles:\n")
    print("{:<10} {:<10} {:<25} {:<25} {:<20} {:<55} {:<20}".format("Immeuble", "Lot", "Nom", "Prénom", "Data d'achat", "Adresse", "Email"))
    print("-" * 175)

    for row in sorted_data:
        print("{:<10} {:<10} {:<25} {:<25} {:<20} {:<55} {:<20}".format(row['building_id'], row['property'], row['lastname'], row['firstname'], row['owner_acquisition_date'], row['street1'] + ", " + row['city'] + " " + row['zip'], row['email']))
    
    print("\n")

# Fonction pour faire une recherche dans les fichiers CSV
def search(column, value):
    csv_data = merge_csv_files('data')
    # Tri des données fusionnées par numéro d'immeuble puis par nom de propriétaire
    sorted_data = sorted(csv_data, key=lambda x: (int(x['building_id']), x['lastname']))

    # Normalisation et suppression des accents pour la valeur entrée par l'utilisateur
    value_normalized = unicodedata.normalize('NFD', value).encode('ascii', 'ignore').decode('utf-8').lower()

    #Affichage
    print("\n{:<10} {:<10} {:<25} {:<25} {:<20} {:<55} {:<20}".format("Immeuble", "Lot", "Nom", "Prénom", "Data d'achat", "Adresse", "Email"))
    print("-" * 150)

    for row in sorted_data:
        # Normalisation et suppression des accents pour la valeur de la colonne spécifiée
        column_value_normalized = unicodedata.normalize('NFD', row[column]).encode('ascii', 'ignore').decode('utf-8').lower()

        if column_value_normalized == value_normalized:
            print("{:<10} {:<10} {:<25} {:<25} {:<20} {:<55} {:<20}".format(row['building_id'], row['property'], row['lastname'], row['firstname'], row['owner_acquisition_date'], row['street1'] + ", " + row['city'] + " " + row['zip'], row['email']))

    print("\n")


# Fonction de traduction pour faire la recherche des colonnes en francais ou bien en anglais
def translate_input(user_input):
        translation_map  = {
        'lot': 'property',
        'immeuble': 'building_id',
        'achat': 'owner_acquisition_date',
        'rue': 'street1',
        'ville': 'city',
        'codepostal': 'zip',
        'nom': 'lastname',
        'prenom': 'firstname',
        'email': 'email'
        }
        user_input_lower = user_input.lower()

        for key, value in translation_map.items():
            if user_input_lower == key.lower():
                return value, translation_map 
            
        return user_input_lower, translation_map

# Fonction principale
def main():
    while True:
        display_menu()
        choice = input("Veuillez saisir votre choix (1 ou 2): ")

        if choice == '1':
            display_buildings()

        elif choice == '2':
            print("\nColonne possible: immeuble, lot, nom, prenom, achat, rue, ville, codepostal, email")
            column_input = input("Veuillez saisir le nom de la colonne à rechercher : ")
            column, translation_map  = translate_input(column_input)

            if column not in translation_map.values():
                print(f"La colonne '{column}' n'existe pas dans les données.\n")
                continue
            
            value_input = input("Veuillez saisir la valeur à rechercher : ")
            search(column, value_input)

        else:
            print("Choix invalide. Veuillez saisir 1 ou 2.\n")

if __name__ == "__main__":
    main()
