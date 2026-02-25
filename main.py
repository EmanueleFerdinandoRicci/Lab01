from random import randint


class Domanda:
    def __init__(self, testo: str, difficolta: int, r1: str, r2: str, r3: str, r4: str):
        self.testo = testo
        self.difficolta = difficolta
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.rispostaCorretta = r1

    def lista_risposte(self):
        nuova_lista = []
        lista = [self.r1, self.r2, self.r3, self.r4]
        n1 = randint(0, 3)
        nuova_lista.append(lista.pop(n1))
        n2 = randint(0, 2)
        nuova_lista.append(lista.pop(n2))
        n3 = randint(0, 1)
        nuova_lista.append(lista.pop(n3))
        nuova_lista.append(lista[0])
        return nuova_lista

    def lettore(self):
        opzioni = self.lista_risposte()
        print(f"Livello {self.difficolta}) {self.testo}")
        print(f"    1) {opzioni[0]}")
        print(f"    2) {opzioni[1]}")
        print(f"    3) {opzioni[2]}")
        print(f"    4) {opzioni[3]}")
        return opzioni


class Player:
    def __init__(self, nome: str, valore: int):
        self.nome = nome
        self.valore = valore

    def aggiungi_punti(self):
        self.valore += 1


class Game:
    def __init__(self):
        self.arrayDomande = []
        self.arrayPlayer = []

    def leggi_domande(self, nome_file: str):
        with open(nome_file, "r", encoding="utf-8") as file:
            while True:
                testo = file.readline().strip()
                if testo == "":
                    break
                difficolta = int(file.readline().strip())
                r1 = file.readline().strip()
                r2 = file.readline().strip()
                r3 = file.readline().strip()
                r4 = file.readline().strip()

                nuova = Domanda(testo, difficolta, r1, r2, r3, r4)
                self.arrayDomande.append(nuova)
                file.readline()
        return self.arrayDomande

    def lettore_di_livelli(self):
        livello_max = 0
        for domanda in self.arrayDomande:
            if livello_max < domanda.difficolta:
                livello_max = domanda.difficolta
        return livello_max

    def interazione_gioco(self):
        counter = 0
        punteggio = 0
        livello_max = self.lettore_di_livelli()

        while counter <= livello_max:
            array_livello = []
            for domanda in self.arrayDomande:
                if counter == domanda.difficolta:
                    array_livello.append(domanda)

            if len(array_livello) > 0:
                n = randint(0, len(array_livello) - 1)
                domanda_da_porre = array_livello[n]

                opzioni = domanda_da_porre.lettore()
                valore = int(input("Inserisci la risposta: "))

                scelta_utente = opzioni[valore - 1]

                if scelta_utente == domanda_da_porre.rispostaCorretta:
                    punteggio += 1
                    print("Risposta corretta!\n")
                else:
                    indice_corretto = opzioni.index(domanda_da_porre.rispostaCorretta) + 1
                    print(f"Risposta sbagliata! La risposta corretta era: {indice_corretto}\n")

            counter += 1

        print(f"Hai totalizzato {punteggio} punti!")
        nome = input("Inserisci il tuo nickname: ")
        player = Player(nome, punteggio)
        self.arrayPlayer.append(player)

    def stampa(self, nome_file: str):
        classifica = []

        with open(nome_file, "r", encoding="utf-8") as file:
            for linea in file:
                if linea.strip() != "":
                    parti = linea.strip().split()
                    classifica.append((parti[0], int(parti[1])))

        for p in self.arrayPlayer:
            classifica.append((p.nome, p.valore))

        #ordina in modo decrescente
        classifica.sort(key=lambda x: x[1], reverse=True)

        with open(nome_file, "w", encoding="utf-8") as file:
            righe = [f"{nome} {punti}" for nome, punti in classifica]
            file.write("\n".join(righe))


gioco = Game()
gioco.leggi_domande("domande.txt")
gioco.interazione_gioco()
gioco.stampa("punti.txt")