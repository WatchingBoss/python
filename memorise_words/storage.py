import json
from pathlib import Path
from typing import List, Dict
from .models import Word, Topic

class Storage:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.topics_file = self.data_dir / "topics.json"
        
    def save_topic(self, topic: Topic) -> None:
        """Save a topic to the JSON file"""
        topics = self.load_topics()
        topics[topic.name] = topic
        
        # Convert topics to dictionary format for JSON serialization
        topics_dict = {}
        for name, topic_obj in topics.items():
            topics_dict[name] = topic_obj.model_dump()
        
        with open(self.topics_file, 'w') as f:
            json.dump(topics_dict, f, indent=2, default=str)
        
    def load_topics(self) -> Dict[str, Topic]:
        """Load all topics from the JSON file"""
        if not self.topics_file.exists():
            return {}
        
        try:
            with open(self.topics_file, 'r') as f:
                topics_dict = json.load(f)
            
            # Convert dictionary back to Topic objects
            topics = {}
            for name, topic_data in topics_dict.items():
                # Convert word dictionaries back to Word objects
                words = [Word(**word_data) for word_data in topic_data.get('words', [])]
                topics[name] = Topic(name=name, words=words)
            
            return topics
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading topics: {e}")
            return {}
    
    def save_word_to_topic(self, word: Word, topic_name: str) -> None:
        """Add a word to a specific topic"""
        topics = self.load_topics()
        
        if topic_name not in topics:
            topics[topic_name] = Topic(name=topic_name, words=[])
        
        # Check if word already exists in topic
        existing_words = [w.text for w in topics[topic_name].words]
        if word.text not in existing_words:
            topics[topic_name].words.append(word)
            self.save_topic(topics[topic_name])
    
    def get_topic(self, topic_name: str) -> Optional[Topic]:
        """Get a specific topic by name"""
        topics = self.load_topics()
        return topics.get(topic_name)
    
    def delete_topic(self, topic_name: str) -> bool:
        """Delete a topic"""
        topics = self.load_topics()
        if topic_name in topics:
            del topics[topic_name]
            
            # Save updated topics
            topics_dict = {}
            for name, topic_obj in topics.items():
                topics_dict[name] = topic_obj.model_dump()
            
            with open(self.topics_file, 'w') as f:
                json.dump(topics_dict, f, indent=2, default=str)
            return True
        return False
