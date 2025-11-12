class PaletteCouleurs:
    def __init__(self, couleurs):
        if isinstance(couleurs, list) or isinstance(couleurs, tuple):
            if all(isinstance(c, tuple) and len(c) == 3 for c in couleurs):
                self.couleurs = couleurs
            else:
                raise ValueError("Chaque couleur doit être un tuple de 3 entiers (R, G, B).")
        elif isinstance(couleurs, tuple) and len(couleurs) == 3:
            self.couleurs = [couleurs]
        else:
            raise ValueError("L'argument doit être une liste de tuples ou un seul tuple de 3 entiers (R, G, B).")
        
        self.taille = len(self.couleurs)

    def get_couleur(self, valeur):
        index = valeur % self.taille
        return self.couleurs[index]
    
    def debug(self):
        print("Palette de couleurs:")
        for i, couleur in enumerate(self.couleurs):
            print(f"  Couleur {i}: {couleur}")
    

    
if __name__ == "__main__":
    palette1 = PaletteCouleurs([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    palette1.debug()
    print(palette1.get_couleur(62000))
    
    palette2 = PaletteCouleurs([(128, 128, 128)])
    palette2.debug()
