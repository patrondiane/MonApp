import random

def print_title(title):
    print("=" * 40)
    print(f"● {title.upper()} ●".center(40))
    print("=" * 40)

print_title("Devine Le Nombre ")

def jeu_utilisateur_devine():
    print("Je pense à un nombre de 1 à 100.")

    secret = random.randint(1, 100)
    essais_max = 7
    essais = 0

    while essais < essais_max:
        proposition = int(input(f"Essai {essais + 1} -> "))
        essais += 1

        if proposition < secret:
            print("❌ Trop petit.\n")
        elif proposition > secret:
            print("❌ Trop grand.\n")
        else:
            print(f"✅ Bravo ! Tu as trouvé en {essais} essais.")
            return
    
    print(f"💥 Tu as perdu ! Le nombre était {secret}.")

# Appel du jeu 
jeu_utilisateur_devine()
