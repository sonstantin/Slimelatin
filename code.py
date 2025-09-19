import tkinter as tk
import json
import random
from tkinter import messagebox, simpledialog

class LatinTrainer:
    def __init__(self, master):
        self.master = master
        self.master.title("Latein lernen, Juhu!")

        buttonframe = tk.Frame(self.master)
        buttonframe.pack(expand=True)

        neue_Vokabel_hinzufuegen = tk.Button(buttonframe, text="Vokabel hinzufügen", command=self.add_it)
        neue_Vokabel_hinzufuegen.grid(column=0, row=0, pady=5, padx=5)

        abfrage = tk.Button(buttonframe, text="Abfrage starten", command=self.Abfrage)
        abfrage.grid(column=1, row=0, pady=5, padx=5)

        liste = tk.Button(buttonframe, text="Listen", command=self.lists)
        liste.grid(column=2, row=0, pady=5, padx=5)

        self.latein = {}
        self.deutsch = {}
        self.load()

    def add_it(self):
        add = tk.Toplevel(self.master)
        add.title("Vokabel hinzufügen")

        ue1 = tk.Label(add, text="Wort im Lateinischen:")
        ue1.pack()
        self.lat = tk.Entry(add, width=50)
        self.lat.pack()

        ue2 = tk.Label(add, text="Wort im Deutschen:")
        ue2.pack()
        self.deu = tk.Entry(add, width=50)
        self.deu.pack()

        save = tk.Button(add, text="Speichern", command=self.save)
        save.pack()

    def save(self):
        latinum = self.lat.get().strip()
        germanicum = self.deu.get().strip()
        self.lat.delete(0, "end")
        self.deu.delete(0, "end")

        if not latinum:
            messagebox.showerror("Fehler", "Gib im ersten Textfeld etwas ein!")
            return
        if not germanicum:
            messagebox.showerror("Fehler", "Gib im zweiten Textfeld etwas ein!")
            return

        # Latein -> Deutsch
        if latinum in self.latein:
            if germanicum not in self.latein[latinum]:
                self.latein[latinum].append(germanicum)
        else:
            self.latein[latinum] = [germanicum]

        # Deutsch -> Latein
        if germanicum in self.deutsch:
            if latinum not in self.deutsch[germanicum]:
                self.deutsch[germanicum].append(latinum)
        else:
            self.deutsch[germanicum] = [latinum]

        with open("latin.json", mode="w", encoding="utf-8") as f:
            json.dump([self.latein, self.deutsch], f, indent=4, ensure_ascii=False)
        

        messagebox.showinfo("Gespeichert", "Vokabel erfolgreich gespeichert!")

    def lists(self):
        lists = tk.Toplevel(self.master)
        d = tk.Button(lists, text="Deutsch -> Latein", command=self.listD)
        d.pack()
        l = tk.Button(lists, text="Latein -> Deutsch", command=self.listL)
        l.pack()
    def load(self):
        try:
            with open("latin.json", mode="r", encoding="utf-8") as f:
                self.latein = json.load(f)
                self.deutsch = self.latein[1]
                self.latein = self.latein[0]
        except FileNotFoundError:
            self.latein = {}
            self.deutsch = {}
            messagebox.showwarning("Datei nicht gefunden", """Keine gespeicherten Vokabeln gefunden.
Der Speicherstand wurde zurückgesetzt.""")
    def listD(self):
        list = tk.Toplevel(self.master)
        Vrow = 0
        Vcolumn = 0
        var = 0
        for vocab in sorted(self.deutsch):
            b = tk.Label(list, text=f"{vocab} -> {self.deutsch[vocab]}")
            b.grid(row=Vrow, column=Vcolumn)
            var += 1
            list.title(f"Anzahl der Vokabeln: {var}")
            if Vrow > 34:
                Vrow = 0
                Vcolumn += 1
            else:
                Vrow += 1
    def listL(self):
        list = tk.Toplevel(self.master)
        Vrow = 0
        Vcolumn = 0
        var = 0

        for vocab in sorted(self.latein):
            b = tk.Label(list, text=f"{vocab} -> {self.latein[vocab]}")
            b.grid(row=Vrow, column=Vcolumn)
            var += 1
            list.title(f"Anzahl der Vokabeln: {var}")
            if Vrow > 34:
                Vrow = 0
                Vcolumn += 1
            else:
                Vrow += 1
    def Abfrage(self):
        try:
            try:
                with open("punkte.json", mode="r", encoding="utf-8") as f:
                    coins = json.load(f)
            except EOFError:
                coins = 0
        except FileNotFoundError:
            coins = 0

        if not self.latein or not self.deutsch:
            messagebox.showerror("Fehler", "Es sind keine Vokabeln vorhanden!")
            return

        while True:
            dir = random.choice([1, 2])  # 1 = Deutsch->Latein, 2 = Latein->Deutsch
            if dir == 1:
                frage_dict = self.deutsch
                frage_sprache = "Deutsch"
                antwort_sprache = "Latein"
            else:
                frage_dict = self.latein
                frage_sprache = "Latein"
                antwort_sprache = "Deutsch"

            toAsk = random.choice(list(frage_dict.keys()))
            erwartete_antworten = frage_dict[toAsk]

            if isinstance(erwartete_antworten, str):
                erwartete_antworten = [erwartete_antworten]
            isKonjunktiv = random.choice([True, False])
            if isKonjunktiv == True and toAsk.endswith("re") and frage_sprache == "Latein":
                person = random.choice(["1. Person Singular", "2. Person Singular", "3. Person Singular", "1. Person Plural", "2. Person Plural", "3. Person Plural"])
                print(person)

                antwort = simpledialog.askstring("Vokabelabfrage - Konjunktiv", f"""Was ist die {person} Konjunktiv von '{toAsk}'?
                                                 Wenn du abbrechen willst, dann lass das Feld
                                                 leer und drücke 'OK'!""")

                endings = {
                    "1. Person Singular": "m",
                    "2. Person Singular": "s",
                    "3. Person Singular": "t",
                    "1. Person Plural": "mus",
                    "2. Person Plural": "tis",
                    "3. Person Plural": "nt"
                }
                print(endings[f"{person}"])
                if antwort is None:
                    with open("punkte.json", mode="w", encoding="utf-8") as f:
                        json.dump(coins, f)
                    break  # Benutzer hat abgebrochen
                
                elif antwort == f'{toAsk}{endings[f"{person}"]}':
                    coins += 1
                    messagebox.showinfo("Richtig", f'''Du hast jetzt {coins} Punkte. Alle 
                                        richtigen Antworten sind:
                                        {toAsk}{endings[f"{person}"]}''')
                elif antwort == "":
                    with open("punkte.json", mode="w", encoding="utf-8") as f:
                        json.dump(coins, f)
                    break  # Benutzer hat abgebrochen
                else:
                    coins -= 1
                    messagebox.showwarning("Falsch", f'Die richtige Antwort wäre {toAsk}{endings[f"{person}"]} gewesen! Du hast jetzt {coins} Punkte!')
            if isKonjunktiv == False:
                erwartete_antworten = [a.strip().lower() for a in erwartete_antworten]
                
                antwort = simpledialog.askstring("Vokabelabfrage",
                    f"""Was heißt '{toAsk}' auf {antwort_sprache}?
                    Wenn du abbrechen willst, dann lass das Feld
                    leer und drücke auf 'OK'!""")


                if antwort is None:
                    with open("punkte.json", mode="w", encoding="utf-8") as f:
                        json.dump(coins, f)
                    break  # Benutzer hat abgebrochen
                elif antwort is "":
                    
                    with open("punkte.json", mode="w", encoding="utf-8") as f:
                        json.dump(coins, f)
                    break

                elif antwort.strip().lower() in erwartete_antworten:
                    coins += 1
                    messagebox.showinfo("Richtig", f"""Du hast jetzt {coins} Punkte. Alle 
                                        richtigen Antworten sind:
                                        {erwartete_antworten}""")
                else:
                    coins -= 1

                    messagebox.showwarning("Falsch", f"Die richtige Antwort wäre {erwartete_antworten} gewesen! Du hast jetzt {coins} Punkte!")

            with open("punkte.json", mode="w", encoding="utf-8") as f:
                json.dump(coins, f)


    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LatinTrainer(root)
    app.run()
