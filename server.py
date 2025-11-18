from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def load_tagged_posts():
    """Load tagged posts from cache"""
    if os.path.exists('tagged_posts.json'):
        with open('tagged_posts.json', 'r') as f:
            return json.load(f)
    return {}

def load_community_tags():
    """Load community-contributed tags"""
    if os.path.exists('community_tags.json'):
        with open('community_tags.json', 'r') as f:
            return json.load(f)
    return {}

def save_community_tags(tags):
    """Save community-contributed tags"""
    with open('community_tags.json', 'w') as f:
        json.dump(tags, f, indent=2)

@app.route('/api/posts')
def get_posts():
    """Get all tagged posts with community tags merged"""
    tagged_posts = load_tagged_posts()
    community_tags = load_community_tags()
    
    # Convert dict to list for easier frontend handling
    posts_list = []
    for post_id, post_data in tagged_posts.items():
        post_dict = {
            'id': post_id,
            **post_data,
            'community_tags': community_tags.get(post_id, [])
        }
        posts_list.append(post_dict)
    
    # Sort by date (newest first)
    posts_list.sort(key=lambda x: x.get('date_modified', ''), reverse=True)
    return jsonify(posts_list)

@app.route('/api/tags')
def get_tags():
    """Get all unique AI tags"""
    tagged_posts = load_tagged_posts()
    all_tags = set()
    for post_data in tagged_posts.values():
        all_tags.update(post_data.get('tags', []))
    return jsonify(sorted(list(all_tags)))

@app.route('/api/community-tags')
def get_community_tags():
    """Get all unique community tags"""
    community_tags = load_community_tags()
    all_tags = set()
    for tags_list in community_tags.values():
        all_tags.update(tags_list)
    return jsonify(sorted(list(all_tags)))

@app.route('/api/community-tags/<path:post_id>', methods=['POST'])
def add_community_tag(post_id):
    """Add a community tag to a post"""
    data = request.json
    new_tag = data.get('tag', '').strip().lower()
    
    if not new_tag:
        return jsonify({'error': 'Tag cannot be empty'}), 400
    
    # Load existing community tags
    community_tags = load_community_tags()
    
    # Add tag to post (avoid duplicates)
    if post_id not in community_tags:
        community_tags[post_id] = []
    
    if new_tag not in community_tags[post_id]:
        community_tags[post_id].append(new_tag)
        save_community_tags(community_tags)
        return jsonify({'success': True, 'tag': new_tag})
    
    return jsonify({'success': False, 'message': 'Tag already exists'})

@app.route('/api/authors')
def get_authors():
    """Get all unique authors"""
    tagged_posts = load_tagged_posts()
    authors = set()
    for post_data in tagged_posts.values():
        author = post_data.get('author', '')
        if author:
            authors.add(author)
    return jsonify(sorted(list(authors)))

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    print("\n🚀 Starting Inkhaven Post Explorer...")
    print(f"📊 Running on port {port}\n")
    app.run(debug=False, host='0.0.0.0', port=port)

