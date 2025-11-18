import json
import os
from typing import List, Dict, Optional
from anthropic import Anthropic
import time

class PostTagger:
    def __init__(self, cache_file="tagged_posts.json"):
        self.cache_file = cache_file
        self.tagged_posts = self._load_cache()
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
    def _load_cache(self) -> Dict:
        """Load previously tagged posts from cache"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """Save tagged posts to cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.tagged_posts, f, indent=2)
    
    def tag_post(self, post: Dict) -> List[str]:
        """Use Claude to tag a post based on its title and URL"""
        post_id = post['id']
        
        # Check cache first
        if post_id in self.tagged_posts:
            return self.tagged_posts[post_id]['tags']
        
        title = post.get('title', '')
        url = post.get('url', '')
        author = post.get('author', {}).get('name', '')
        
        prompt = f"""You are a tagging system. Based on the blog post title and URL below, return ONLY a comma-separated list of 1-4 relevant tags. Do not explain or justify your choices.

Available tags: ai-safety, technical-ml, mathematics, statistics, biology, physics, chemistry, philosophy, moral-philosophy, technology, programming, politics, economics, society, personal, life-advice, rationality, epistemology, history, art, literature, music, psychology, neuroscience, religion, education, science-fiction, games, humor, travel

Title: {title}
URL: {url}
Author: {author}

Response format (example): technical-ml, mathematics"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=150,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the response - extract just the tags
            response_text = message.content[0].text.strip()
            
            # If response has multiple lines, try to find the line with tags
            lines = response_text.split('\n')
            tags_str = lines[0]  # Usually the tags are in the first line
            
            # Clean up the response and extract only valid tags
            valid_tags = {
                'ai-safety', 'technical-ml', 'mathematics', 'statistics', 'biology',
                'physics', 'chemistry', 'philosophy', 'moral-philosophy', 'technology',
                'programming', 'politics', 'economics', 'society', 'personal',
                'life-advice', 'rationality', 'epistemology', 'history', 'art',
                'literature', 'music', 'psychology', 'neuroscience', 'religion',
                'education', 'science-fiction', 'games', 'humor', 'travel'
            }
            
            # Split by comma and filter for valid tags only
            raw_tags = [tag.strip().lower() for tag in tags_str.split(',')]
            tags = [tag for tag in raw_tags if tag in valid_tags]
            
            # If no valid tags found, default to 'personal'
            if not tags:
                tags = ['personal']
            
            # Cache the result
            self.tagged_posts[post_id] = {
                'title': title,
                'url': url,
                'author': author,
                'date_modified': post.get('date_modified', ''),
                'tags': tags
            }
            self._save_cache()
            
            return tags
            
        except Exception as e:
            print(f"Error tagging post {title}: {e}")
            return ['uncategorized']
    
    def tag_all_posts(self, feed_file="inkhaven_feed.json", max_posts: Optional[int] = None):
        """Tag all posts in the feed"""
        with open(feed_file, 'r') as f:
            feed = json.load(f)
        
        posts = feed.get('items', [])
        if max_posts:
            posts = posts[:max_posts]
        
        total = len(posts)
        print(f"Processing {total} posts...")
        
        for i, post in enumerate(posts, 1):
            post_id = post['id']
            if post_id in self.tagged_posts:
                print(f"[{i}/{total}] Skipping (cached): {post.get('title', 'Untitled')}")
            else:
                print(f"[{i}/{total}] Tagging: {post.get('title', 'Untitled')}")
                self.tag_post(post)
                time.sleep(0.5)  # Rate limiting
        
        print(f"\nDone! Tagged {len(self.tagged_posts)} posts total.")
        return self.tagged_posts
    
    def get_all_tags(self) -> List[str]:
        """Get unique list of all tags used"""
        all_tags = set()
        for post_data in self.tagged_posts.values():
            all_tags.update(post_data.get('tags', []))
        return sorted(list(all_tags))
    
    def get_all_authors(self) -> List[str]:
        """Get unique list of all authors"""
        authors = set()
        for post_data in self.tagged_posts.values():
            author = post_data.get('author', '')
            if author:
                authors.add(author)
        return sorted(list(authors))

if __name__ == "__main__":
    tagger = PostTagger()
    # Tag ALL posts (869 total)
    tagger.tag_all_posts(max_posts=None)

