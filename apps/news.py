# ~/pi_dashboard/apps/news.py
import re
import curses
import feedparser
import textwrap
import threading
import time
from apps.base import BaseApp
import config

class NewsApp(BaseApp):
    def __init__(self, stdscr):
        self.articles = []
        self.current_feed_index = 0
        self.current_article_index = 0
        self.is_loading = False
        super().__init__(stdscr) # This starts the background thread
        self.name = "News Reader"

    def update_data(self):
        """ This runs in the background thread from BaseApp """
        self.is_loading = True
        try:
            feed_url = config.RSS_FEEDS[self.current_feed_index]
            # Fetching news... the UI won't freeze here!
            feed = feedparser.parse(feed_url)
            self.articles = feed.entries
        except Exception:
            self.articles = []
        self.is_loading = False

    def get_update_interval(self):
        return 600 # Auto-refresh news every 10 minutes

    def action_a(self): # Next Article
        if self.articles and self.current_article_index < len(self.articles) - 1:
            self.current_article_index += 1
            # No need to refresh_news, just redraw local data
            self.draw()

    def action_b(self): # Prev Article
        if self.articles and self.current_article_index > 0:
            self.current_article_index -= 1
            self.draw()

    def action_c(self): # Next Feed
        self.current_feed_index = (self.current_feed_index + 1) % len(config.RSS_FEEDS)
        self.current_article_index = 0
        # Trigger a background update immediately
        threading.Thread(target=self.update_data, daemon=True).start()

    def draw(self):
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()
        
        feed_url = config.RSS_FEEDS[self.current_feed_index]
        source_name = feed_url.split('/')[2].replace('www.', '').upper()

        # Header
        self.stdscr.addstr(0, 0, f" {source_name} ", curses.A_BOLD | curses.color_pair(1))
        
        if self.is_loading and not self.articles:
            self.stdscr.addstr(2, 0, "Fetching updates...", curses.A_DIM)
            self.stdscr.refresh()
            return

        if not self.articles:
            self.stdscr.addstr(2, 0, "No articles found.")
            self.stdscr.refresh()
            return

        # Rest of your original logic for rendering the article
        self.stdscr.addstr(0, max_x - 10, f"{self.current_article_index + 1}/{len(self.articles)}")
        
        article = self.articles[self.current_article_index]
        raw_summary = article.get('summary', 'No summary.')
        clean_summary = re.sub('<[^<]+?>', '', raw_summary)
        
        title = article.get('title', 'No Title')
        wrapped_title = textwrap.wrap(title, width=max_x - 2)
        
        line_offset = 2
        for line in wrapped_title:
            if line_offset < max_y:
                self.stdscr.addstr(line_offset, 0, line, curses.A_UNDERLINE)
                line_offset += 1
        
        line_offset += 1 
        wrapped_summary = textwrap.wrap(clean_summary, width=max_x - 2)
        for line in wrapped_summary:
            if line_offset < max_y - 1: 
                self.stdscr.addstr(line_offset, 0, line)
                line_offset += 1

        self.stdscr.refresh()
