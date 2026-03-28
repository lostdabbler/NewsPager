import requests, html, curses
from apps.base import BaseApp

class QuizApp(BaseApp):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.name = "Quiz"
        self.score = 0
        self.total = 0
        self.revealed = False
        self.current = {"q": "Loading...", "a": ""}
        self.get_new_q()

    def get_new_q(self):
        try:
            r = requests.get("https://opentdb.com/api.php?amount=1&category=9&type=multiple", timeout=3)
            data = r.json()['results'][0]
            self.current = {"q": html.unescape(data['question']), "a": html.unescape(data['correct_answer'])}
        except:
            self.current = {"q": "API Error. Check Net.", "a": "N/A"}

    def action_a(self): # Correct
        if self.revealed: self.score += 1; self.total += 1; self.revealed = False; self.get_new_q()

    def action_b(self): # Incorrect
        if self.revealed: self.total += 1; self.revealed = False; self.get_new_q()

    def action_c(self): # Reveal
        self.revealed = True

    def draw(self):
        self.stdscr.erase()
        self.stdscr.addstr(0, 0, f"QUIZ [{self.score}/{self.total}]", curses.A_BOLD)
        self.stdscr.addstr(2, 0, self.current['q'][:160]) # Simple truncate for small screen
        
        if self.revealed:
            self.stdscr.addstr(6, 0, "ANS:", curses.A_DIM)
            self.stdscr.addstr(6, 5, self.current['a'], curses.color_pair(1))
            self.stdscr.addstr(8, 0, "A: Correct | B: Wrong")
        else:
            self.stdscr.addstr(8, 0, "Btn C: Reveal")
        self.stdscr.refresh()
