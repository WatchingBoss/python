"""Main application module for the memorise words app."""

import flet as ft
import asyncio
import random
from datetime import datetime
from typing import List, Optional, Dict, Any
from .models import Word, PracticeSession
from .storage import JSONStorage


class WordMemorizeApp:
    """Main word memorization application."""
    
    def __init__(self):
        """Initialize the application."""
        self.storage = JSONStorage()
        self.current_words: List[Word] = []
        self.current_practice_word: Optional[Word] = None
        self.practice_mode = False
        
        # UI components
        self.word_input: Optional[ft.TextField] = None
        self.definition_input: Optional[ft.TextField] = None
        self.difficulty_dropdown: Optional[ft.Dropdown] = None
        self.words_list: Optional[ft.ListView] = None
        self.practice_word_text: Optional[ft.Text] = None
        self.practice_input: Optional[ft.TextField] = None
        self.practice_result: Optional[ft.Text] = None
        self.page: Optional[ft.Page] = None
        
    def main(self, page: ft.Page):
        """Main entry point for the Flet app."""
        self.page = page
        page.title = "Word Memorization"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.window_width = 800
        page.window_height = 600
        page.window_resizable = True
        
        # Load existing words
        self.refresh_words()
        
        # Create UI components
        self.create_ui_components()
        
        # Create main layout
        page.add(
            ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=ft.Text(
                            "Word Memorization App",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.PRIMARY
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=20)
                    ),
                    
                    # Tab container
                    ft.Tabs(
                        selected_index=0,
                        tabs=[
                            ft.Tab(
                                text="Add Words",
                                content=self.create_add_word_tab()
                            ),
                            ft.Tab(
                                text="Word List",
                                content=self.create_word_list_tab()
                            ),
                            ft.Tab(
                                text="Practice",
                                content=self.create_practice_tab()
                            )
                        ]
                    )
                ]),
                padding=20
            )
        )
        
    def create_ui_components(self):
        """Create and initialize UI components."""
        # Add word components
        self.word_input = ft.TextField(
            label="New word",
            width=300,
            autofocus=True
        )
        
        self.definition_input = ft.TextField(
            label="Definition",
            width=400,
            multiline=True,
            max_lines=3
        )
        
        self.difficulty_dropdown = ft.Dropdown(
            label="Difficulty (1-5)",
            width=150,
            value="1",
            options=[
                ft.dropdown.Option("1", "1 - Easy"),
                ft.dropdown.Option("2", "2 - Moderate"),
                ft.dropdown.Option("3", "3 - Normal"),
                ft.dropdown.Option("4", "4 - Hard"),
                ft.dropdown.Option("5", "5 - Very Hard")
            ]
        )
        
        # Word list
        self.words_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.all(10)
        )
        
        # Practice components
        self.practice_word_text = ft.Text(
            "",
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        self.practice_input = ft.TextField(
            label="Your definition",
            width=400,
            multiline=True,
            max_lines=3
        )
        
        self.practice_result = ft.Text(
            "",
            text_align=ft.TextAlign.CENTER
        )
        
    def create_add_word_tab(self) -> ft.Container:
        """Create the add word tab content."""
        return ft.Container(
            content=ft.Column([
                ft.Text("Add a new word to your collection", size=16),
                ft.Divider(),
                
                # Input form
                ft.Row([
                    self.word_input,
                    self.difficulty_dropdown
                ]),
                
                ft.Row([
                    self.definition_input
                ]),
                
                # Action buttons
                ft.Row([
                    ft.ElevatedButton(
                        "Add Word",
                        on_click=self.add_word,
                        icon=ft.icons.ADD
                    ),
                    ft.OutlinedButton(
                        "Clear",
                        on_click=self.clear_form
                    )
                ], alignment=ft.MainAxisAlignment.START),
                
                ft.Divider(),
                ft.Text(f"Total words: {len(self.current_words)}", size=14)
            ]),
            padding=20
        )
        
    def create_word_list_tab(self) -> ft.Container:
        """Create the word list tab content."""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Your Word Collection", size=16),
                    ft.IconButton(
                        ft.icons.REFRESH,
                        tooltip="Refresh list",
                        on_click=lambda _: self.refresh_words_list()
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                
                # Filter options
                ft.Row([
                    ft.Text("Filter:"),
                    ft.Dropdown(
                        value="all",
                        width=150,
                        options=[
                            ft.dropdown.Option("all", "All words"),
                            ft.dropdown.Option("unmastered", "Not mastered"),
                            ft.dropdown.Option("mastered", "Mastered")
                        ],
                        on_change=self.filter_words
                    )
                ]),
                
                # Words list
                ft.Container(
                    content=self.words_list,
                    height=400,
                    border=ft.border.all(1, ft.colors.OUTLINE)
                )
            ]),
            padding=20
        )
        
    def create_practice_tab(self) -> ft.Container:
        """Create the practice tab content."""
        return ft.Container(
            content=ft.Column([
                ft.Text("Practice Mode", size=16),
                ft.Divider(),
                
                # Practice controls
                ft.Row([
                    ft.ElevatedButton(
                        "Start Practice",
                        on_click=self.start_practice,
                        icon=ft.icons.PLAY_ARROW
                    ),
                    ft.OutlinedButton(
                        "Random Word",
                        on_click=self.get_random_word,
                        icon=ft.icons.SHUFFLE
                    )
                ]),
                
                ft.Divider(),
                
                # Practice area
                ft.Container(
                    content=ft.Column([
                        ft.Text("Word:", size=14),
                        self.practice_word_text,
                        ft.Container(height=20),
                        self.practice_input,
                        ft.Container(height=10),
                        ft.Row([
                            ft.ElevatedButton(
                                "Check Answer",
                                on_click=self.check_answer,
                                icon=ft.icons.CHECK
                            ),
                            ft.OutlinedButton(
                                "Show Answer",
                                on_click=self.show_answer,
                                icon=ft.icons.VISIBILITY
                            ),
                            ft.OutlinedButton(
                                "Next Word",
                                on_click=self.get_random_word,
                                icon=ft.icons.SKIP_NEXT
                            )
                        ]),
                        ft.Container(height=20),
                        self.practice_result
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    border=ft.border.all(1, ft.colors.OUTLINE)
                )
            ]),
            padding=20
        )
        
    def add_word(self, e):
        """Add a new word to the collection."""
        try:
            word_text = self.word_input.value.strip()
            definition_text = self.definition_input.value.strip()
            
            if not word_text or not definition_text:
                self.show_snackbar("Please fill in both word and definition", error=True)
                return
                
            difficulty = int(self.difficulty_dropdown.value)
            
            # Create new word
            new_word = Word(
                word=word_text,
                definition=definition_text,
                difficulty=difficulty
            )
            
            # Add to storage
            word_id = self.storage.add_word(new_word)
            new_word.id = word_id
            
            # Refresh UI
            self.refresh_words()
            self.clear_form(None)
            self.refresh_words_list()
            
            self.show_snackbar(f"Added word: {word_text}")
            
        except ValueError as ve:
            self.show_snackbar(f"Error: {str(ve)}", error=True)
        except Exception as ex:
            self.show_snackbar(f"Unexpected error: {str(ex)}", error=True)
            
    def clear_form(self, e):
        """Clear the add word form."""
        self.word_input.value = ""
        self.definition_input.value = ""
        self.difficulty_dropdown.value = "1"
        self.page.update()
        
    def refresh_words(self):
        """Refresh the words list from storage."""
        self.current_words = self.storage.get_all_words()
        
    def refresh_words_list(self):
        """Refresh the words list view."""
        self.refresh_words()
        self.words_list.controls.clear()
        
        for word in self.current_words:
            # Create word card
            word_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                word.word,
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Row([
                                ft.Text(f"Difficulty: {word.difficulty}"),
                                ft.Icon(
                                    ft.icons.CHECK_CIRCLE if word.mastered else ft.icons.RADIO_BUTTON_UNCHECKED,
                                    color=ft.colors.GREEN if word.mastered else ft.colors.GREY
                                )
                            ])
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Text(
                            word.definition,
                            size=14,
                            color=ft.colors.ON_SURFACE_VARIANT
                        ),
                        
                        ft.Row([
                            ft.Text(f"Practiced: {word.times_practiced} times"),
                            ft.Row([
                                ft.IconButton(
                                    ft.icons.EDIT,
                                    tooltip="Edit word",
                                    on_click=lambda e, w=word: self.edit_word(w)
                                ),
                                ft.IconButton(
                                    ft.icons.DELETE,
                                    tooltip="Delete word",
                                    on_click=lambda e, w=word: self.delete_word(w)
                                )
                            ])
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    padding=15
                )
            )
            
            self.words_list.controls.append(word_card)
            
        self.page.update()
        
    def filter_words(self, e):
        """Filter words based on selection."""
        filter_value = e.control.value
        
        if filter_value == "all":
            filtered_words = self.current_words
        elif filter_value == "mastered":
            filtered_words = [w for w in self.current_words if w.mastered]
        else:  # unmastered
            filtered_words = [w for w in self.current_words if not w.mastered]
            
        # Update the display
        self.words_list.controls.clear()
        
        for word in filtered_words:
            word_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                word.word,
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(f"Difficulty: {word.difficulty}")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(word.definition, size=14)
                    ]),
                    padding=15
                )
            )
            self.words_list.controls.append(word_card)
            
        self.page.update()
        
    def edit_word(self, word: Word):
        """Edit a word (placeholder for future implementation)."""
        self.show_snackbar(f"Edit functionality for '{word.word}' coming soon!")
        
    def delete_word(self, word: Word):
        """Delete a word from the collection."""
        if self.storage.delete_word(word.id):
            self.refresh_words()
            self.refresh_words_list()
            self.show_snackbar(f"Deleted word: {word.word}")
        else:
            self.show_snackbar("Failed to delete word", error=True)
            
    def start_practice(self, e):
        """Start practice mode."""
        if not self.current_words:
            self.show_snackbar("No words to practice! Add some words first.", error=True)
            return
            
        self.practice_mode = True
        self.get_random_word(None)
        self.show_snackbar("Practice mode started!")
        
    def get_random_word(self, e):
        """Get a random word for practice."""
        if not self.current_words:
            self.practice_word_text.value = "No words available"
            self.page.update()
            return
            
        import random
        # Prefer unmastered words
        unmastered = [w for w in self.current_words if not w.mastered]
        if unmastered:
            self.current_practice_word = random.choice(unmastered)
        else:
            self.current_practice_word = random.choice(self.current_words)
            
        self.practice_word_text.value = self.current_practice_word.word
        self.practice_input.value = ""
        self.practice_result.value = ""
        self.page.update()
        
    def check_answer(self, e):
        """Check the user's answer."""
        if not self.current_practice_word:
            self.show_snackbar("No word selected for practice", error=True)
            return
            
        user_answer = self.practice_input.value.strip().lower()
        correct_answer = self.current_practice_word.definition.lower()
        
        # Simple similarity check
        if user_answer in correct_answer or correct_answer in user_answer:
            self.practice_result.value = "✓ Good job!"
            self.practice_result.color = ft.colors.GREEN
            
            # Update word statistics
            self.current_practice_word.times_practiced += 1
            self.current_practice_word.last_practiced = datetime.now()
            
            # Consider mastered if practiced enough times
            if self.current_practice_word.times_practiced >= 5:
                self.current_practice_word.mastered = True
                
            self.storage.update_word(self.current_practice_word)
        else:
            self.practice_result.value = "✗ Try again or check the answer"
            self.practice_result.color = ft.colors.RED
            
        self.page.update()
        
    def show_answer(self, e):
        """Show the correct answer."""
        if not self.current_practice_word:
            self.show_snackbar("No word selected for practice", error=True)
            return
            
        self.practice_result.value = f"Answer: {self.current_practice_word.definition}"
        self.practice_result.color = ft.colors.BLUE
        self.page.update()
        
    def show_snackbar(self, message: str, error: bool = False):
        """Show a snackbar message."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.colors.ERROR if error else ft.colors.PRIMARY
        )
        self.page.snack_bar.open = True
        self.page.update()


def main():
    """Main entry point for the application."""
    ft.app(target=WordMemorizeApp().main)


if __name__ == "__main__":
    main()
