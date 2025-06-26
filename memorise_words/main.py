import flet as ft
import random
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(f"sqlite:///memorise_words/words.db") # Ensure path is correct for where the app runs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, nullable=False, index=True)

class WordStore:
    def __init__(self, db_path="memorise_words/words.db"): # db_path is illustrative, engine is global
        self._create_table()

    def _create_table(self):
        Base.metadata.create_all(bind=engine)

    def add_word(self, new_word_text):
        if not new_word_text:
            return "Input cannot be empty."

        session = SessionLocal()
        try:
            new_word_obj = Word(word=new_word_text)
            session.add(new_word_obj)
            session.commit()
            return f"Added: {new_word_text}"
        except IntegrityError:
            session.rollback()
            return f"'{new_word_text}' already exists."
        finally:
            session.close()

    def get_random_word(self):
        session = SessionLocal()
        try:
            # For SQLite, func.random() or func.rand() depending on SQLAlchemy version and dialect specifics
            # For PostgreSQL use func.random()
            # For MySQL use func.rand()
            # SQLite uses RANDOM()
            random_word_obj = session.query(Word).order_by(func.random()).first()
            return random_word_obj.word if random_word_obj else None
        finally:
            session.close()

    def get_all_words(self):
        session = SessionLocal()
        try:
            all_word_objects = session.query(Word).order_by(Word.word).all()
            return [word_obj.word for word_obj in all_word_objects]
        finally:
            session.close()

    def clear_all_words(self):
        session = SessionLocal()
        try:
            session.query(Word).delete()
            session.commit()
            return "All words cleared."
        except Exception as e:
            session.rollback()
            return f"Error clearing words: {e}"
        finally:
            session.close()

def main(page: ft.Page):
    page.title = "Memorise Words"
    page.vertical_alignment = ft.MainAxisAlignment.START

    word_store = WordStore() # db_path no longer needed as engine is global

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
