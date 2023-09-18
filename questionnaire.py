"""
Fichier de génération de questionnaires depuis des fichiers json.
"""
import json
import sys


class Question:
    """
    Classe Question : Elle permet de dérouler le contenu d'une question depuis un fichier JSON
    """

    def __init__(self, titre: str, choix: list, bonne_reponse: str):
        """
        Constructeur de la classe Question

        :param titre: str, le titre d'une question
        :param choix: list, une liste de réponse possible à la question
        :param bonne_reponse: str, la réponse valide à la question
        """
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data: dict) -> object:
        """
        Fonction qui permet de lire un fichier json et d'en extraire le titre, le choix de réponse et la bonne réponse.

        :param: data, un dictionnaire contenant toutes les données d'une question

        :returns: un objet Question avec ses données triées
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
    """
    Classe Questionnaire pour gérer un questionnaire depuis un fichier json
    """

    def __init__(self, titre: str, categorie: str, difficulte: str, questions: list):
        """
        Constructeur de la classe
        :param titre: str, le titre général du questionnaire
        :param categorie: str, le nom de la catégorie auquel appartient le questionnaire
        :param difficulte: str, le niveau de difficulté du questionnaire
        :param questions: list, la liste des questions
        """
        self.questions = questions
        self.titre = titre
        self.categorie = categorie
        self.difficulte = difficulte

    def from_json_data(data: dict) -> object:
        """
        Fonction qui trie les données issus du fichier json.

        :param data: dict, les données brute du questionnaire désérialisé
        :return: un objet trié avec les données pour lancer un questionnaire
        """
        questionnaire_data_question = data["questions"]
        qs = [Question.from_json_data(i) for i in questionnaire_data_question if Question.from_json_data(i)]

        return Questionnaire(data["titre"], data["categorie"], data["difficulte"], qs)

    def lancer(self) -> int:
        """
        Fonction pour comptabiliser le nombre de bonne réponse au questionnaire généré.

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

    def start(file_data: str):

        filename = open(file_data, "r")
        data_json = filename.read()
        filename.close()
        questionnaire = json.loads(data_json)

        return Questionnaire.from_json_data(questionnaire).lancer()


# programme principal
if len(sys.argv) == 2 and ".json" in (sys.argv[1]):
    Questionnaire.start(sys.argv[1])
else:
    print("Erreur, veuillez indiquer un seul fichier 'json' en paramètre de votre commande")
    sys.exit()

print()
