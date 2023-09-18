"""
Fichier de génération de questionnaires depuis des fichiers json.
"""
import json

NUMERO_QUESTION = 1


class Question:
    """
    Classe qui permet de générer une question depuis un fichier JSON
    """

    def __init__(self, titre: str, choix: list, bonne_reponse: str):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data: dict) -> object:
        """
        Fonction qui permet de lire un fichier json et d'en extraire le titre, le choix de réponse et la bonne réponse.

        :returns: un objet Question avec ses données
        """
        choix = [i[0] for i in data["choix"]]
        bonne_reponse = [i[0] for i in data["choix"] if i[1]]
        # prendre en compte le cas d'aucune réponse et de plus d'une réponse.
        if len(bonne_reponse) != 1:
            return None
        q = Question(data["titre"], choix, bonne_reponse[0])
        return q

    def poser(self, numero_question : int, nb_question_total : int) -> bool:
        """
        Fonction pour démarrer le questionnaire.
        Elle retourne true ou false à l'utilisateur en fonction de sa réponse.

        :return: boolean
        """

        print("Questionnaire ")
        print("QUESTION n° " + str(numero_question + 1) + "/" + str(nb_question_total))
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i + 1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_utilisateur_numerique(1, len(self.choix))

        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")

        print()
        return resultat_response_correcte

    def demander_reponse_utilisateur_numerique(min: int, max: int) -> int:
        """
        Fonction pour récupérer la réponse numérique de l'utilisateur.

        :param min: int, le numéro de la réponse la plus basse
        :param max: int, le numéro de la réponse la plus haute
        :return: le choix numérique de l'utilisateur
        """
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_utilisateur_numerique(min, max)


class Questionnaire:

    def __init__(self, titre: str, categorie: str, difficulte: str, questions : list):
        self.questions = questions
        self.titre = titre
        self.categorie = categorie
        self.difficulte = difficulte

    def from_json_data(data):
        questionnaire_data_question = data["questions"]
        qs = [Question.from_json_data(i) for i in questionnaire_data_question]

        return Questionnaire(data["titre"], data["categorie"], data["difficulte"], qs)

    def lancer(self) -> int:
        """
        Fonction pour comptabiliser le nombre de bonne réponse au questionnaire généré
        :return: int, le score de l'utilisateur
        """

        score = 0
        print("_______________________")
        print("Questionnaire : " + self.titre)
        print("Catégorie : " + self.categorie)
        print("Difficulté : " + self.difficulte)
        print("Nombre de questions : " + str(len(self.questions)))
        print("_______________________")
        for index in range(len(self.questions)):
            question = self.questions[index]
            if question.poser(index, len(self.questions)):
                score += 1

        print("Votre score final est de :", score, "sur", len(self.questions))
        return score


# q1 = Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris")
# q1.poser()

# data = (("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris", "Quelle est la capitale de la France ?")
# q = Question.FromData(data)
# print(q.__dict__)


# --------------charger fichier json
filename = "animaux_leschats_confirme.json"  # test avec un fichier
file = open(filename, "r")
data_json = file.read()
file.close()
questionnaire = json.loads(data_json)

Questionnaire.from_json_data(questionnaire).lancer()

print()
