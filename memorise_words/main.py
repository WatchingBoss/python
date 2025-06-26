import flet as ft
import sqlite3
import random

class WordStore:
    def __init__(self, db_name="words.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL UNIQUE
                )
            """)
            conn.commit()

    def add_word(self, word):
        if not word:
            return "Input cannot be empty."
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
                conn.commit()
            return f"Added: {word}"
        except sqlite3.IntegrityError:
            return f"'{word}' already exists."

    def get_random_word(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM words ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else None

    def get_all_words(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word FROM words ORDER BY word")
            return [row[0] for row in cursor.fetchall()]

    def clear_all_words(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM words")
            conn.commit()
        return "All words cleared."

def main(page: ft.Page):
    page.title = "Memorise Words"
    page.vertical_alignment = ft.MainAxisAlignment.START

    word_store = WordStore("memorise_words/words.db")

    output_text = ft.Text(value="Welcome! Add or find words.", size=16)
    new_word_input = ft.TextField(label="Enter new word", width=300)

    def update_output(message: str):
        output_text.value = message
        page.update()

    def add_word_click(e):
        word = new_word_input.value.strip()
        message = word_store.add_word(word)
        update_output(message)
        new_word_input.value = ""
        page.update()

    def random_word_click(e):
        word = word_store.get_random_word()
        if word:
            update_output(f"Random word: {word}")
        else:
            update_output("No words in the dictionary yet.")

    def all_words_click(e):
        words = word_store.get_all_words()
        if words:
            output_text.value = "All words:\n" + "\n".join(f"- {w}" for w in words)
        else:
            output_text.value = "No words in the dictionary yet."
        page.update()

    def clear_list_click(e):
        message = word_store.clear_all_words()
        update_output(message)

    add_button = ft.ElevatedButton(text="Add new word", on_click=add_word_click)
    random_button = ft.ElevatedButton(text="Random word", on_click=random_word_click)
    all_button = ft.ElevatedButton(text="All words", on_click=all_words_click)
    clear_button = ft.ElevatedButton(text="Clean the list", on_click=clear_list_click)

    page.add(
        ft.Column(
            [
                output_text,
                ft.Row([new_word_input, add_button]),
                ft.Row([random_button, all_button, clear_button]),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
