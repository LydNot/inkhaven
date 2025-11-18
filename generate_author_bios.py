import json
import os
from anthropic import Anthropic
import time
from collections import defaultdict

def generate_author_bios():
    """Generate AI bios for each author based on their posts"""
    
    # Load tagged posts
    with open('tagged_posts.json', 'r') as f:
        tagged_posts = json.load(f)
    
    # Group posts by author
    author_posts = defaultdict(list)
    for post_data in tagged_posts.values():
        author = post_data.get('author', '')
        if author:
            author_posts[author].append({
                'title': post_data.get('title', ''),
                'tags': post_data.get('tags', [])
            })
    
    # Load or create author bios cache
    bios_file = 'author_bios.json'
    if os.path.exists(bios_file):
        with open(bios_file, 'r') as f:
            author_bios = json.load(f)
    else:
        author_bios = {}
    
    # Initialize Anthropic client
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    print(f"Generating bios for {len(author_posts)} authors...")
    
    for i, (author, posts) in enumerate(sorted(author_posts.items()), 1):
        # Skip if already generated
        if author in author_bios:
            print(f"[{i}/{len(author_posts)}] Skipping (cached): {author}")
            continue
        
        print(f"[{i}/{len(author_posts)}] Generating bio for: {author}")
        
        # Prepare post information
        titles = [p['title'] for p in posts[:10]]  # Use up to 10 recent posts
        all_tags = []
        for p in posts:
            all_tags.extend(p['tags'])
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Generate bio
        prompt = f"""Based on these blog post titles and topics, write a brief (2-3 sentence) description of what {author} writes about. Be specific and engaging.

Recent post titles:
{chr(10).join(f'- {t}' for t in titles)}

Most common topics: {', '.join(f'{tag} ({count})' for tag, count in top_tags)}

Write a concise, engaging bio that captures their main themes and style. Start directly with what they write about (don't say "This author writes about..."). Keep it under 60 words."""

        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            bio = message.content[0].text.strip()
            author_bios[author] = bio
            
            # Save after each generation
            with open(bios_file, 'w') as f:
                json.dump(author_bios, f, indent=2)
            
            print(f"  ✓ Generated: {bio[:60]}...")
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            author_bios[author] = f"Writer exploring various topics including {', '.join(t[0] for t in top_tags[:3])}."
            with open(bios_file, 'w') as f:
                json.dump(author_bios, f, indent=2)
    
    print(f"\n✅ Done! Generated bios for {len(author_bios)} authors.")
    return author_bios

if __name__ == "__main__":
    generate_author_bios()


