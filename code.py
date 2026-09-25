import json
import random
import tkinter as tk
from tkinter import messagebox, ttk


class LatinTrainer:

  def __init__(self, master):
    self.master = master
    self.master.title("LateinTrainer")
    self.master.geometry("560x540")
    self.master.minsize(500, 500)

    # Farbpalette (Clean & Modern)
    self.COLOR_ACCENT = "#EC0016"
    self.COLOR_ACCENT_HOVER = "#C30012"
    self.COLOR_BG = "#F0F3F5"
    self.COLOR_CARD = "#FFFFFF"
    self.COLOR_TEXT = "#282D37"
    self.COLOR_TEXT_MUTED = "#687078"
    self.COLOR_BORDER = "#DCDFE3"
    self.COLOR_SUCCESS = "#2E7D32"
    self.COLOR_ERROR = "#C62828"

    self.master.configure(bg=self.COLOR_BG)

    self.raw_data = {"page": 1, "vokabulary": {}}
    self.latein = {}
    self.deutsch = {}
    self.vocab_meta = {}

    self.active_latein = {}
    self.active_deutsch = {}

    self.current_frame = None

    self._setup_base_ui()
    self.load()
    self.show_menu()

  def _create_button(
      self, parent, text, command, primary=True, width=None, bg_override=None
  ):
    bg_color = (
        bg_override
        if bg_override
        else (self.COLOR_ACCENT if primary else self.COLOR_CARD)
    )
    hover_color = (
        self.COLOR_ACCENT_HOVER
        if primary and not bg_override
        else ("#E4E7EA" if not bg_override else bg_color)
    )
    fg_color = "#FFFFFF" if primary or bg_override else self.COLOR_TEXT

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold" if primary else "normal"),
        bg=bg_color,
        fg=fg_color,
        activebackground=hover_color,
        activeforeground=fg_color,
        bd=1 if not primary and not bg_override else 0,
        relief="solid" if not primary and not bg_override else "flat",
        highlightthickness=0,
        cursor="hand2",
        padx=15,
        pady=8,
    )

    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

    if not primary and not bg_override:
      btn.configure(highlightbackground=self.COLOR_BORDER)

    if width:
      btn.configure(width=width)
    return btn

  def _setup_base_ui(self):
    self.header = tk.Frame(self.master, bg=self.COLOR_ACCENT, height=55)
    self.header.pack(fill="x", side="top")
    self.header.pack_propagate(False)

    self.btn_back = tk.Button(
        self.header,
        text="← Zurück",
        command=self.show_menu,
        font=("Segoe UI", 9, "bold"),
        bg=self.COLOR_ACCENT_HOVER,
        fg="#FFFFFF",
        activebackground=self.COLOR_ACCENT,
        activeforeground="#FFFFFF",
        bd=0,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=4,
    )

    self.title_label = tk.Label(
        self.header,
        text="LateinTrainer",
        font=("Segoe UI", 14, "bold"),
        bg=self.COLOR_ACCENT,
        fg="#FFFFFF",
        anchor="w",
    )
    self.title_label.pack(side="left", padx=20, pady=12)

    self.card_container = tk.Frame(
        self.master,
        bg=self.COLOR_CARD,
        bd=1,
        relief="solid",
        highlightbackground=self.COLOR_BORDER,
    )
    self.card_container.pack(fill="both", expand=True, padx=20, pady=20)

  def _clear_content(self, show_back=True):
    if self.current_frame is not None:
      self.current_frame.destroy()

    if show_back:
      self.btn_back.pack(side="right", padx=15, pady=12)
    else:
      self.btn_back.pack_forget()

    self.current_frame = tk.Frame(self.card_container, bg=self.COLOR_CARD)
    self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

  def load(self):
    try:
      with open("adeo.json", mode="r", encoding="utf-8") as f:
        self.raw_data = json.load(f)
        vokab_dict = self.raw_data.get("vokabulary", {})

        self.latein = {}
        self.deutsch = {}
        self.vocab_meta = {}

        for lat_word, info in vokab_dict.items():
          meanings = info.get("meaning", [])
          if isinstance(meanings, str):
            meanings = [meanings]

          self.vocab_meta[lat_word] = {
              "blue": info.get("blue", False),
              "page": str(info.get("page", "")),
          }

          self.latein[lat_word] = meanings

          for m in meanings:
            m_clean = m.strip()
            if m_clean not in self.deutsch:
              self.deutsch[m_clean] = []
            if lat_word not in self.deutsch[m_clean]:
              self.deutsch[m_clean].append(lat_word)

    except FileNotFoundError:
      self.raw_data = {"page": 1, "vokabulary": {}}
      self.latein = {}
      self.deutsch = {}
      self.vocab_meta = {}

  # --- ANSICHT 1: Hauptmenü ---
  def show_menu(self):
    self._clear_content(show_back=False)

    tk.Label(
        self.current_frame,
        text="Übersicht",
        font=("Segoe UI", 13, "bold"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
    ).pack(anchor="w", pady=(0, 2))

    tk.Label(
        self.current_frame,
        text="Bitte wähle eine Option aus:",
        font=("Segoe UI", 9),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT_MUTED,
    ).pack(anchor="w", pady=(0, 20))

    btn_frame = tk.Frame(self.current_frame, bg=self.COLOR_CARD)
    btn_frame.pack(fill="x", pady=10)

    self._create_button(
        btn_frame,
        text="Abfrage starten",
        command=self.show_quiz_settings,
        primary=True,
    ).pack(fill="x", pady=6)

    self._create_button(
        btn_frame,
        text="Vokabel hinzufügen",
        command=self.show_add_vocab,
        primary=False,
    ).pack(fill="x", pady=6)

    self._create_button(
        btn_frame,
        text="Wörterbuch / Listen",
        command=self.show_list_selection,
        primary=False,
    ).pack(fill="x", pady=6)

    total_vok = len(self.latein)
    tk.Label(
        self.current_frame,
        text=f"Status: {total_vok} Vokabeln geladen",
        font=("Segoe UI", 8),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT_MUTED,
    ).pack(side="bottom", anchor="w")

  # --- ANSICHT 2: Vokabel hinzufügen ---
  def show_add_vocab(self):
    self._clear_content(show_back=True)

    tk.Label(
        self.current_frame,
        text="Neue Vokabel hinzufügen",
        font=("Segoe UI", 12, "bold"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
    ).pack(anchor="w", pady=(0, 10))

    def create_field(parent, label_text):
      tk.Label(
          parent,
          text=label_text,
          font=("Segoe UI", 9, "bold"),
          bg=self.COLOR_CARD,
          fg=self.COLOR_TEXT,
      ).pack(anchor="w", pady=(6, 2))
      entry = tk.Entry(
          parent,
          font=("Segoe UI", 10),
          bd=1,
          relief="solid",
          highlightthickness=1,
          highlightbackground=self.COLOR_BORDER,
      )
      entry.pack(fill="x", pady=(0, 4))
      return entry

    self.lat_entry = create_field(self.current_frame, "Lateinisches Wort:")
    self.deu_entry = create_field(
        self.current_frame, "Bedeutungen im Deutschen (kommagetrennt):"
    )
    self.stamm_entry = create_field(
        self.current_frame, "Stammformen (kommagetrennt):"
    )
    self.page_entry = create_field(self.current_frame, "Seite (z.B. 12):")

    self.blue_var = tk.BooleanVar()
    chk = tk.Checkbutton(
        self.current_frame,
        text="Als blau markieren",
        variable=self.blue_var,
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
        activebackground=self.COLOR_CARD,
        font=("Segoe UI", 9),
    )
    chk.pack(anchor="w", pady=5)

    self._create_button(
        self.current_frame,
        text="Speichern",
        command=self.save_vocab,
        primary=True,
    ).pack(fill="x", pady=10)

    self.msg_label = tk.Label(
        self.current_frame,
        text="",
        font=("Segoe UI", 9),
        bg=self.COLOR_CARD,
    )
    self.msg_label.pack(anchor="w")

  def save_vocab(self):
    latinum = self.lat_entry.get().strip()
    germanicum = [
        m.strip() for m in self.deu_entry.get().split(",") if m.strip()
    ]
    stammformen = [
        s.strip() for s in self.stamm_entry.get().split(",") if s.strip()
    ]
    page_val = self.page_entry.get().strip()
    is_blue = self.blue_var.get()

    if not latinum or not germanicum:
      self.msg_label.config(
          text="Bitte Latein und mindestens eine Übersetzung angeben.",
          fg=self.COLOR_ERROR,
      )
      return

    self.raw_data["vokabulary"][latinum] = {
        "meaning": germanicum,
        "stammformen": stammformen,
        "blue": is_blue,
        "page": page_val,
    }

    with open("adeo.json", mode="w", encoding="utf-8") as f:
      json.dump(self.raw_data, f, indent=4, ensure_ascii=False)

    self.load()
    self.lat_entry.delete(0, "end")
    self.deu_entry.delete(0, "end")
    self.stamm_entry.delete(0, "end")
    self.blue_var.set(False)

    self.msg_label.config(
        text="Vokabel erfolgreich gespeichert!", fg=self.COLOR_SUCCESS
    )

  # --- ANSICHT 3: Sprachrichtung wählen ---
  def show_list_selection(self):
    self._clear_content(show_back=True)

    tk.Label(
        self.current_frame,
        text="Wörterbuch / Listen",
        font=("Segoe UI", 12, "bold"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        self.current_frame,
        text="Wähle die gewünschte Sortierung:",
        font=("Segoe UI", 9),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT_MUTED,
    ).pack(anchor="w", pady=(0, 20))

    self._create_button(
        self.current_frame,
        text="Deutsch → Latein",
        command=lambda: self.show_vocab_table("Deutsch → Latein", self.deutsch),
        primary=False,
    ).pack(fill="x", pady=6)

    self._create_button(
        self.current_frame,
        text="Latein → Deutsch",
        command=lambda: self.show_vocab_table("Latein → Deutsch", self.latein),
        primary=True,
    ).pack(fill="x", pady=6)

  # --- ANSICHT 4: Tabellenansicht ---
  def show_vocab_table(self, title, dictionary):
    self._clear_content(show_back=True)

    tk.Label(
        self.current_frame,
        text=f"{title} ({len(dictionary)} Einträge)",
        font=("Segoe UI", 12, "bold"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
    ).pack(anchor="w", pady=(0, 10))

    tree_frame = tk.Frame(self.current_frame, bg=self.COLOR_CARD)
    tree_frame.pack(fill="both", expand=True)

    columns = ("key", "val")
    tree = ttk.Treeview(
        tree_frame, columns=columns, show="headings", selectmode="browse"
    )

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold"),
        background=self.COLOR_BG,
        foreground=self.COLOR_TEXT,
    )
    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=24,
        background=self.COLOR_CARD,
        fieldbackground=self.COLOR_CARD,
    )

    tree.heading("key", text="Wort")
    tree.heading("val", text="Übersetzung")
    tree.column("key", width=160, anchor="w")
    tree.column("val", width=260, anchor="w")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    for key in sorted(dictionary.keys()):
      val = dictionary[key]
      val_str = ", ".join(val) if isinstance(val, list) else str(val)
      tree.insert("", "end", values=(key, val_str))

  # --- ANSICHT 5: Quiz-Einstellungen (Filter) ---
  def show_quiz_settings(self):
    self._clear_content(show_back=True)

    tk.Label(
        self.current_frame,
        text="Abfrage-Einstellungen",
        font=("Segoe UI", 12, "bold"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
    ).pack(anchor="w", pady=(0, 10))

    tk.Label(
        self.current_frame,
        text="Bitte wähle aus, welche Vokabeln abgefragt werden sollen.",
        font=("Segoe UI", 9),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT_MUTED,
        wraplength=450,
        justify="left",
    ).pack(anchor="w", pady=(0, 20))

    self.quiz_blue_var = tk.BooleanVar()
    tk.Checkbutton(
        self.current_frame,
        text="Nur blaue Vokabeln abfragen",
        variable=self.quiz_blue_var,
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
        activebackground=self.COLOR_CARD,
        font=("Segoe UI", 10, "bold"),
    ).pack(anchor="w", pady=(0, 15))

    tk.Label(
        self.current_frame,
        text="Nur Vokabeln von folgenden Seiten (kommagetrennt):",
        font=("Segoe UI", 9, "bold"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
    ).pack(anchor="w", pady=(0, 5))

    self.quiz_page_entry = tk.Entry(
        self.current_frame,
        font=("Segoe UI", 10),
        bd=1,
        relief="solid",
        highlightthickness=1,
        highlightbackground=self.COLOR_BORDER,
    )
    self.quiz_page_entry.pack(fill="x", pady=(0, 20))
    tk.Label(
        self.current_frame,
        text="Hinweis: Leer lassen, um alle Seiten abzufragen.",
        font=("Segoe UI", 8, "italic"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT_MUTED,
    ).pack(anchor="w", pady=(0, 20))

    self._create_button(
        self.current_frame,
        text="Abfrage starten",
        command=self.start_quiz,
        primary=True,
    ).pack(fill="x", pady=6)

  # --- ANSICHT 6: Abfrage (Interaktiv im Fenster) ---
  def start_quiz(self):
    if not self.latein or not self.deutsch:
      messagebox.showerror("Fehler", "Es sind keine Vokabeln vorhanden.")
      return

    must_be_blue = self.quiz_blue_var.get()
    allowed_pages = [
        p.strip() for p in self.quiz_page_entry.get().split(",") if p.strip()
    ]

    self.active_latein = {}
    self.active_deutsch = {}

    for word, meta in self.vocab_meta.items():
      if must_be_blue and not meta["blue"]:
        continue
      if allowed_pages and meta["page"] not in allowed_pages:
        continue

      self.active_latein[word] = self.latein[word]
      for d_word in self.latein[word]:
        if d_word not in self.active_deutsch:
          self.active_deutsch[d_word] = []
        self.active_deutsch[d_word].append(word)

    if not self.active_latein:
      messagebox.showwarning(
          "Hinweis", "Für diese Kriterien gibt es keine Vokabeln."
      )
      return

    try:
      with open("punkte.json", mode="r", encoding="utf-8") as f:
        self.coins = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, EOFError):
      self.coins = 0

    self.next_quiz_question()

  def next_quiz_question(self):
    self._clear_content(show_back=True)

    dir_choice = random.choice([1, 2])
    if dir_choice == 1:
      frage_dict = self.active_deutsch
      self.antwort_sprache = "Latein"
    else:
      frage_dict = self.active_latein
      self.antwort_sprache = "Deutsch"

    self.to_ask = random.choice(list(frage_dict.keys()))
    self.erwartete = frage_dict[self.to_ask]
    if isinstance(self.erwartete, str):
      self.erwartete = [self.erwartete]

    is_konjunktiv = (
        random.choice([True, False])
        and self.to_ask.endswith("re")
        and self.antwort_sprache == "Deutsch"
    )

    header_frame = tk.Frame(self.current_frame, bg=self.COLOR_CARD)
    header_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        header_frame,
        text="Vokabelabfrage",
        font=("Segoe UI", 12, "bold"),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
    ).pack(side="left")

    self.coins_label = tk.Label(
        header_frame,
        text=f"Punkte: {self.coins}",
        font=("Segoe UI", 10, "bold"),
        bg=self.COLOR_BG,
        fg=self.COLOR_TEXT,
        padx=8,
        pady=2,
    )
    self.coins_label.pack(side="right")

    if is_konjunktiv:
      self.person = random.choice([
          "1. Person Singular",
          "2. Person Singular",
          "3. Person Singular",
          "1. Person Plural",
          "2. Person Plural",
          "3. Person Plural",
      ])
      endings = {
          "1. Person Singular": "m",
          "2. Person Singular": "s",
          "3. Person Singular": "t",
          "1. Person Plural": "mus",
          "2. Person Plural": "tis",
          "3. Person Plural": "nt",
      }
      self.korrekte_antwort = f"{self.to_ask}{endings[self.person]}"
      self.is_konjunktiv_mode = True

      frage_text = f"Was ist die {self.person} Konjunktiv von '{self.to_ask}'?"
    else:
      self.is_konjunktiv_mode = False
      frage_text = f"Was heißt '{self.to_ask}' auf {self.antwort_sprache}?"

    tk.Label(
        self.current_frame,
        text=frage_text,
        font=("Segoe UI", 11),
        bg=self.COLOR_CARD,
        fg=self.COLOR_TEXT,
        wraplength=450,
        justify="left",
    ).pack(anchor="w", pady=(0, 15))

    self.quiz_entry = tk.Entry(
        self.current_frame,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid",
        highlightthickness=1,
        highlightbackground=self.COLOR_BORDER,
    )
    self.quiz_entry.pack(fill="x", pady=(0, 10))
    self.quiz_entry.focus()
    self.quiz_entry.bind("<Return>", lambda e: self.check_quiz_answer())

    self.btn_submit = self._create_button(
        self.current_frame,
        text="Antworten",
        command=self.check_quiz_answer,
        primary=True,
    )
    self.btn_submit.pack(fill="x", pady=5)

    self.quiz_feedback = tk.Label(
        self.current_frame,
        text="",
        font=("Segoe UI", 9, "bold"),
        bg=self.COLOR_CARD,
        justify="left",
    )
    self.quiz_feedback.pack(anchor="w", pady=10)

  def check_quiz_answer(self):
    user_input = self.quiz_entry.get().strip()
    if not user_input:
      return

    def strip_articles(text):
      text = text.lower().strip()
      for art in ["der ", "die ", "das "]:
        if text.startswith(art):
          text = text[len(art) :]
      return text

    if self.is_konjunktiv_mode:
      user_clean = strip_articles(user_input)
      ans_clean = strip_articles(self.korrekte_antwort)
      is_correct = user_clean == ans_clean
      loesung_str = self.korrekte_antwort
    else:
      user_clean = strip_articles(user_input)
      erwartete_clean = [strip_articles(a) for a in self.erwartete]
      is_correct = user_clean in erwartete_clean
      loesung_str = ", ".join(self.erwartete)

    if is_correct:
      self.coins += 1
      self.quiz_feedback.config(
          text=f"Richtig! Lösung: {loesung_str}", fg=self.COLOR_SUCCESS
      )
    else:
      self.coins -= 1
      self.quiz_feedback.config(
          text=f"Falsch! Richtige Lösung: {loesung_str}", fg=self.COLOR_ERROR
      )

    with open("punkte.json", mode="w", encoding="utf-8") as f:
      json.dump(self.coins, f)

    self.coins_label.config(text=f"Punkte: {self.coins}")
    self.btn_submit.config(state="disabled")

    self._create_button(
        self.current_frame,
        text="Nächste Vokabel →",
        command=self.next_quiz_question,
        primary=True,
    ).pack(fill="x", pady=5)


if __name__ == "__main__":
  root = tk.Tk()
  app = LatinTrainer(root)
  root.mainloop()
