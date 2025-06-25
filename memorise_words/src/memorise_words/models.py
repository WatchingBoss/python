"""Data models for the memorise words application."""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Word:
    """Represents a word to be memorized."""
    
    id: Optional[int] = None
    word: str = ""
    definition: str = ""
    topic: str = "General"  # Topic/category for the word
    difficulty: int = 1  # 1-5 scale
    times_practiced: int = 0
    last_practiced: Optional[datetime] = None
    mastered: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)  # Additional tags
    
    def __post_init__(self):
        """Validate word data after initialization."""
        if not self.word.strip():
            raise ValueError("Word cannot be empty")
        if not self.definition.strip():
            raise ValueError("Definition cannot be empty")
        if not self.topic.strip():
            self.topic = "General"
        if not 1 <= self.difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5")
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the word."""
        if tag.strip() and tag not in self.tags:
            self.tags.append(tag.strip())
    
    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the word."""
        try:
            self.tags.remove(tag)
            return True
        except ValueError:
            return False


@dataclass
class PracticeSession:
    """Represents a practice session."""
    
    id: Optional[int] = None
    word_id: int = 0
    start_time: datetime = None
    end_time: Optional[datetime] = None
    correct_answers: int = 0
    total_attempts: int = 0
    
    def __post_init__(self):
        """Set default start time if not provided."""
        if self.start_time is None:
            self.start_time = datetime.now()
    
    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.total_attempts == 0:
            return 0.0
        return (self.correct_answers / self.total_attempts) * 100
