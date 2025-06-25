"""Storage module for persisting word data."""

import json
import sqlite3
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Optional, Dict, Set
from datetime import datetime

from .models import Word, PracticeSession


class WordStorage:
    """Base class for word storage implementations."""
    
    def add_word(self, word: Word) -> int:
        """Add a word and return its ID."""
        raise NotImplementedError
    
    def get_word(self, word_id: int) -> Optional[Word]:
        """Get a word by ID."""
        raise NotImplementedError
    
    def get_all_words(self) -> List[Word]:
        """Get all words."""
        raise NotImplementedError
    
    def update_word(self, word: Word) -> bool:
        """Update a word."""
        raise NotImplementedError
    
    def delete_word(self, word_id: int) -> bool:
        """Delete a word."""
        raise NotImplementedError


class JSONStorage(WordStorage):
    """JSON file-based storage implementation."""
    
    def __init__(self, filepath: Path = None):
        """Initialize JSON storage."""
        self.filepath = filepath or Path("words.json")
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the JSON file exists."""
        if not self.filepath.exists():
            self.filepath.write_text("[]")
    
    def _load_words(self) -> List[dict]:
        """Load words from JSON file."""
        with open(self.filepath, 'r') as f:
            return json.load(f)
    
    def _save_words(self, words: List[dict]):
        """Save words to JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(words, f, indent=2, default=str)
    
    def add_word(self, word: Word) -> int:
        """Add a word and return its ID."""
        words = self._load_words()
        word_id = max([w.get('id', 0) for w in words], default=0) + 1
        word.id = word_id
        
        word_dict = {
            'id': word.id,
            'word': word.word,
            'definition': word.definition,
            'topic': word.topic,
            'difficulty': word.difficulty,
            'times_practiced': word.times_practiced,
            'last_practiced': word.last_practiced.isoformat() if word.last_practiced else None,
            'mastered': word.mastered,
            'created_at': word.created_at.isoformat(),
            'tags': word.tags
        }
        
        words.append(word_dict)
        self._save_words(words)
        return word_id
    
    def get_word(self, word_id: int) -> Optional[Word]:
        """Get a word by ID."""
        words = self._load_words()
        for word_dict in words:
            if word_dict['id'] == word_id:
                return self._dict_to_word(word_dict)
        return None
    
    def get_all_words(self) -> List[Word]:
        """Get all words."""
        words = self._load_words()
        return [self._dict_to_word(word_dict) for word_dict in words]
    
    def update_word(self, word: Word) -> bool:
        """Update a word."""
        words = self._load_words()
        for i, word_dict in enumerate(words):
            if word_dict['id'] == word.id:
                words[i] = {
                    'id': word.id,
                    'word': word.word,
                    'definition': word.definition,
                    'topic': word.topic,
                    'difficulty': word.difficulty,
                    'times_practiced': word.times_practiced,
                    'last_practiced': word.last_practiced.isoformat() if word.last_practiced else None,
                    'mastered': word.mastered,
                    'created_at': word.created_at.isoformat(),
                    'tags': word.tags
                }
                self._save_words(words)
                return True
        return False
    
    def delete_word(self, word_id: int) -> bool:
        """Delete a word."""
        words = self._load_words()
        original_length = len(words)
        words = [w for w in words if w['id'] != word_id]
        if len(words) < original_length:
            self._save_words(words)
            return True
        return False
    
    def _dict_to_word(self, word_dict: dict) -> Word:
        """Convert dictionary to Word object."""
        last_practiced = None
        if word_dict.get('last_practiced'):
            last_practiced = datetime.fromisoformat(word_dict['last_practiced'])
            
        created_at = datetime.now()  # Default
        if word_dict.get('created_at'):
            created_at = datetime.fromisoformat(word_dict['created_at'])
        
        return Word(
            id=word_dict['id'],
            word=word_dict['word'],
            definition=word_dict['definition'],
            topic=word_dict.get('topic', 'General'),
            difficulty=word_dict['difficulty'],
            times_practiced=word_dict['times_practiced'],
            last_practiced=last_practiced,
            mastered=word_dict['mastered'],
            created_at=created_at,
            tags=word_dict.get('tags', [])
        )
    
    def get_all_topics(self) -> List[str]:
        """Get all unique topics."""
        words = self._load_words()
        topics = set()
        for word_dict in words:
            topic = word_dict.get('topic', 'General')
            if topic:
                topics.add(topic)
        return sorted(list(topics))
    
    def get_words_by_topic(self, topic: str) -> List[Word]:
        """Get all words in a specific topic."""
        words = self._load_words()
        topic_words = []
        for word_dict in words:
            if word_dict.get('topic', 'General') == topic:
                topic_words.append(self._dict_to_word(word_dict))
        return topic_words
    
    def clear_all_words(self) -> bool:
        """Clear all words."""
        try:
            self._save_words([])
            return True
        except Exception:
            return False
    
    def clear_topic(self, topic: str) -> bool:
        """Clear all words in a specific topic."""
        try:
            words = self._load_words()
            words = [w for w in words if w.get('topic', 'General') != topic]
            self._save_words(words)
            return True
        except Exception:
            return False
    
    def get_statistics(self) -> Dict[str, any]:
        """Get word statistics."""
        words = self._load_words()
        total_words = len(words)
        mastered_words = sum(1 for w in words if w.get('mastered', False))
        topics = set(w.get('topic', 'General') for w in words)
        
        return {
            'total_words': total_words,
            'mastered_words': mastered_words,
            'unmastered_words': total_words - mastered_words,
            'topics_count': len(topics),
            'topics': sorted(list(topics))
        }
    
    # Async methods for better performance
    async def add_word_async(self, word: Word) -> int:
        """Add a word asynchronously."""
        return await asyncio.to_thread(self.add_word, word)
    
    async def get_all_words_async(self) -> List[Word]:
        """Get all words asynchronously."""
        return await asyncio.to_thread(self.get_all_words)
    
    async def update_word_async(self, word: Word) -> bool:
        """Update a word asynchronously."""
        return await asyncio.to_thread(self.update_word, word)
    
    async def delete_word_async(self, word_id: int) -> bool:
        """Delete a word asynchronously."""
        return await asyncio.to_thread(self.delete_word, word_id)
