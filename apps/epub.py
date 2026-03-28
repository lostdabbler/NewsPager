import curses
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import textwrap
from apps.base import BaseApp

class EpubApp(BaseApp):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.name = "E-Reader"
        self.book_path = "/home/michael/books/current.epub"
        self.pages = []
        self.current_page = 0
        self.load_book()

    def load_book(self):
        try:
            book = epub.read_epub(self.book_path)
            chapters = []
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                chapters.append(soup.get_text())
            
            # Combine text and wrap it for your small screen
            full_text = "\n\n".join(chapters)
            max_y, max_x = self.stdscr.getmaxyx()
            
            # Wrap text to fit width, then chunk it into "pages" for height
            wrapped = textwrap.wrap(full_text, width=max_x - 4)
            lines_per_page = max_y - 4
            self.pages = [wrapped[i:i + lines_per_page] for i in range(0, len(wrapped), lines_per_page)]
        except:
            self.pages = [["Error: No book found at", self.book_path]]

    def action_a(self): # Button A: Prev Page
        if self.current_page > 0: self.current_page -= 1

    def action_b(self): # Button B: Next Page
        if self.current_page < len(self.pages) - 1: self.current_page += 1

    def draw(self):
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()
        
        # Header with Progress
        progress = f"{self.current_page + 1}/{len(self.pages)}"
        self.stdscr.addstr(0, 0, f" READING ", curses.color_pair(1))
        self.stdscr.addstr(0, max_x - len(progress) - 1, progress, curses.A_DIM)

        # Draw the text block
        if self.pages:
            for i, line in enumerate(self.pages[self.current_page]):
                if i < max_y - 2:
                    self.stdscr.addstr(i + 2, 2, line)

        self.stdscr.refresh()
