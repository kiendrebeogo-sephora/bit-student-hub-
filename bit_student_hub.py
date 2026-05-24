# ============================================================
#   BIT STUDENT HUB — PRG1406 Group Assignment 1
#   Domaine : Portail étudiant centralisé (BIT)
#   Auteur  : KIENDREBEOGO Sephora Léocadie
# ============================================================

# ============================================================
# PART 2 & 3 — CLASSES + INHERITANCE + MAGIC METHODS
# ============================================================

class User:
    """Classe parent : utilisateur du portail BIT"""

    total_users = 0  # attribut de classe (pour @classmethod)

    def __init__(self, nom: str, prenom: str, email: str, is_admin: bool):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.is_admin = is_admin  # bool
        User.total_users += 1

    # MAGIC METHOD 1 — ce qui s'affiche quand on fait print(objet)
    def __str__(self) -> str:
        role = "Admin" if self.is_admin else "Étudiant"
        return f"[{role}] {self.prenom} {self.nom} — {self.email}"

    # MAGIC METHOD 2 — pour comparer deux users avec ==
    def __eq__(self, other) -> bool:
        return self.email == other.email

    # PART 4 — DECORATOR @classmethod
    @classmethod
    def get_total_users(cls) -> int:
        """Retourne le nombre total d'utilisateurs créés"""
        return cls.total_users

    # PART 4 — DECORATOR @staticmethod
    @staticmethod
    def valider_email(email: str) -> bool:
        """Vérifie qu'un email contient @ et un point"""
        return "@" in email and "." in email


class Student(User):
    """Classe enfant : étudiant avec notes et paiements"""

    def __init__(self, nom: str, prenom: str, email: str,
                 filiere: str, niveau: int, frais_total: float):
        # Appel du constructeur parent
        super().__init__(nom, prenom, email, is_admin=False)

        # Attributs propres à Student (pas dans User)
        self.filiere = filiere          # str
        self.niveau = niveau            # int
        self.frais_total = frais_total  # float
        self.frais_payes = 0.0          # float
        self.notes = {}                 # dict {matiere: note}
        self.annonces_lues = []         # list

    # MAGIC METHOD 3 — len(etudiant) retourne le nb de matières
    def __len__(self) -> int:
        return len(self.notes)

    # PART 4 — DECORATOR @property (calcul automatique de la moyenne)
    @property
    def moyenne(self) -> float:
        """Calcule la moyenne automatiquement"""
        if not self.notes:
            return 0.0
        return sum(self.notes.values()) / len(self.notes)

    @property
    def solde_restant(self) -> float:
        """Retourne le montant restant à payer"""
        return self.frais_total - self.frais_payes

    @property
    def est_a_jour(self) -> bool:
        """True si tous les frais sont payés"""
        return self.frais_payes >= self.frais_total

    def ajouter_note(self, matiere: str, note: float):
        self.notes[matiere] = note

    def effectuer_paiement(self, montant: float) -> bool:
        if montant < 0:
            print("   Montant invalide : ne peut pas être négatif.")
            return False
        if self.frais_payes + montant > self.frais_total:
            print(f"   Montant trop élevé. Reste à payer : {self.solde_restant:,.0f} FCFA")
            return False
        self.frais_payes += montant
        return True

    def afficher_bulletin(self):
        print(f"\n{'='*45}")
        print(f"  BULLETIN — {self.prenom} {self.nom}")
        print(f"  Filière : {self.filiere} | Niveau : L{self.niveau}")
        print(f"{'='*45}")
        if not self.notes:
            print("  Aucune note enregistrée.")
        else:
            for matiere, note in self.notes.items():
                mention = "✓" if note >= 10 else "✗"
                print(f"  {mention} {matiere:<25} {note:.2f}/20")
            print(f"{'─'*45}")
            print(f"  Moyenne générale : {self.moyenne:.2f}/20")
            print(f"  Nombre de matières : {len(self)}")
        print(f"{'='*45}")

    def afficher_paiement(self):
        statut = "✓ À JOUR" if self.est_a_jour else "✗ EN ATTENTE"
        print(f"\n{'='*45}")
        print(f"  PAIEMENT — {self.prenom} {self.nom}")
        print(f"{'='*45}")
        print(f"  Frais totaux   : {self.frais_total:,.0f} FCFA")
        print(f"  Montant payé   : {self.frais_payes:,.0f} FCFA")
        print(f"  Reste à payer  : {self.solde_restant:,.0f} FCFA")
        print(f"  Statut         : {statut}")
        print(f"{'='*45}")


# ============================================================
# PART 1 — FONCTIONS UTILITAIRES (input + validation)
# ============================================================

def saisir_str(message: str) -> str:
    """Input string non vide"""
    while True:
        valeur = input(message).strip()
        if valeur:
            return valeur
        print("   Ce champ ne peut pas être vide. Réessaie.")

def saisir_int(message: str, min_val: int = None, max_val: int = None) -> int:
    """Input entier avec validation"""
    while True:
        try:
            valeur = int(input(message))
            if min_val is not None and valeur < min_val:
                print(f"   Valeur minimum : {min_val}")
                continue
            if max_val is not None and valeur > max_val:
                print(f"   Valeur maximum : {max_val}")
                continue
            return valeur
        except ValueError:
            print("   Saisis un nombre entier valide.")

def saisir_float(message: str, min_val: float = 0) -> float:
    """Input float avec validation"""
    while True:
        try:
            valeur = float(input(message))
            if valeur < min_val:
                print(f"   Valeur minimum : {min_val}")
                continue
            return valeur
        except ValueError:
            print("   Saisis un nombre valide (ex: 1500.50).")

def saisir_bool(message: str) -> bool:
    """Input booléen (yes/no)"""
    while True:
        valeur = input(message).strip().lower()
        if valeur in ("yes", "oui", "o", "y"):
            return True
        elif valeur in ("no", "non", "n"):
            return False
        print("   Réponds par 'yes' ou 'no'.")

def saisir_email(message: str) -> str:
    """Input email avec validation"""
    while True:
        email = input(message).strip()
        if User.valider_email(email):
            return email
        print("   Email invalide. Ex: nom@bit.edu")

def saisir_note(message: str) -> float:
    """Input note entre 0 et 20"""
    while True:
        note = saisir_float(message, min_val=0)
        if note > 20:
            print("   La note ne peut pas dépasser 20.")
        else:
            return note


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():
    print("\n" + "="*50)
    print("    BIT STUDENT HUB — Portail Étudiant BIT")
    print("="*50)

    etudiants = []
    annonces = [
        "Les examens du semestre 2 commencent le 10 juin 2026.",
        " Dépôt des dossiers de bourse : avant le 30 mai 2026.",
        " Réunion pédagogique : vendredi 28 mai à 10h00."
    ]

    # --- Saisie du nombre d'étudiants ---
    print("\n--- Inscription des étudiants ---")
    nb = saisir_int("Combien d'étudiants voulez-vous inscrire ? (1-5) : ", 1, 5)

    for i in range(nb):
        print(f"\n  ── Étudiant {i+1}/{nb} ──")

        nom      = saisir_str("  Nom de famille : ")
        prenom   = saisir_str("  Prénom : ")
        email    = saisir_email("  Email (@bit.edu) : ")
        filiere  = saisir_str("  Filière (ex: Informatique) : ")
        niveau   = saisir_int("  Niveau (1, 2 ou 3) : ", 1, 3)
        frais    = saisir_float("  Frais de scolarité (FCFA) : ", 0)

        etudiant = Student(nom, prenom, email, filiere, niveau, frais)

        # --- Notes (arithmetic expressions) ---
        print(f"\n  Saisie des notes pour {prenom} :")
        matieres = ["Programmation", "Réseaux", "Bases de données"]
        for matiere in matieres:
            note = saisir_note(f"  Note en {matiere} (/20) : ")
            etudiant.ajouter_note(matiere, note)

        # --- Paiement ---
        deja_paye = saisir_float(f"  Montant déjà payé par {prenom} (FCFA) : ", 0)
        etudiant.effectuer_paiement(deja_paye)

        etudiants.append(etudiant)
        print(f"  ✓ {etudiant} enregistré avec succès.")

    # --- Affichage des annonces ---
    print("\n" + "="*50)
    print("   ANNONCES DU PORTAIL BIT")
    print("="*50)
    for annonce in annonces:
        print(f"  {annonce}")

    # --- Bulletins et paiements ---
    print("\n" + "="*50)
    print("   RÉCAPITULATIF DES ÉTUDIANTS")
    print("="*50)

    for etudiant in etudiants:
        etudiant.afficher_bulletin()
        etudiant.afficher_paiement()

    # --- Statistiques globales (arithmetic expressions) ---
    if etudiants:
        moyennes = [e.moyenne for e in etudiants]
        moy_generale = sum(moyennes) / len(moyennes)
        moy_max      = max(moyennes)
        moy_min      = min(moyennes)
        nb_a_jour    = sum(1 for e in etudiants if e.est_a_jour)
        total_collecte = sum(e.frais_payes for e in etudiants)

        print("\n" + "="*50)
        print("   STATISTIQUES GLOBALES — BIT Student Hub")
        print("="*50)
        print(f"  Nombre total d'utilisateurs  : {User.get_total_users()}")
        print(f"  Étudiants inscrits           : {len(etudiants)}")
        print(f"  Moyenne générale (promo)     : {moy_generale:.2f}/20")
        print(f"  Meilleure moyenne            : {moy_max:.2f}/20")
        print(f"  Moyenne la plus basse        : {moy_min:.2f}/20")
        print(f"  Étudiants à jour (paiement)  : {nb_a_jour}/{len(etudiants)}")
        print(f"  Total collecté               : {total_collecte:,.0f} FCFA")

        # Vérification égalité entre deux étudiants (magic __eq__)
        if len(etudiants) >= 2:
            meme = etudiants[0] == etudiants[1]
            print(f"\n  Étudiant 1 == Étudiant 2 ?   : {meme}")

    print("\n" + "="*50)
    print("  ✅ Session terminée — BIT Student Hub")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
