# 📚 Inkhaven Post Explorer

A beautiful web interface for exploring and filtering Inkhaven blog posts, with automatic AI-powered tagging using Claude.

## Features

- 🤖 **Automatic AI Tagging**: Uses Claude AI to intelligently categorize posts by topic (30+ granular tags)
- 👥 **Community-Contributed Tags**: Add your own custom tags to any post! Tags are shared across all users
- 🏷️ **Filter by Tag**: Filter posts by AI tags like `ai-safety`, `technical-ml`, `philosophy`, and more
- 🎯 **Filter by Community Tags**: Filter by custom tags added by the community
- ✍️ **Filter by Author**: Browse posts from specific bloggers
- 🔍 **Search**: Quick text search through post titles
- 💾 **Smart Caching**: Tags are cached locally to avoid re-processing
- 🎨 **Beautiful UI**: Modern, responsive design with smooth interactions

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Your Anthropic API Key

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### 3. Tag the Posts

Run the tagger to process posts with Claude:

```bash
python tagger.py
```

This will:
- Load posts from `inkhaven_feed.json`
- Use Claude to tag each post based on title and URL
- Cache results in `tagged_posts.json`
- By default, processes the first 50 posts (edit `max_posts` in the script to change this)

To tag ALL posts, edit `tagger.py` and change the last line to:
```python
tagger.tag_all_posts(max_posts=None)  # Remove the limit
```

### 4. Start the Server

```bash
python server.py
```

### 5. Open the App

Navigate to `http://localhost:8000` in your browser!

## Usage

### Filtering

- **AI Tags**: Click on colored tag badges to filter posts by AI-assigned topics (e.g., "ai-safety", "philosophy")
- **Community Tags**: Click to expand "Community-Contributed Tags" section and filter by custom tags
- **Authors**: Click on author names to see posts from specific bloggers
- **Search**: Type in the search box to filter by title
- **Multiple Filters**: All filters work together - select multiple tags and authors!
- **Clear All**: Click "Clear All Filters" to reset

### Adding Community Tags

Each post card has an input box at the bottom where you can:
1. Type a custom tag (e.g., "must-read", "beginner-friendly", "controversial")
2. Press Enter or click "+ Tag" to add it
3. The tag appears immediately with a purple gradient style
4. Community tags are saved and visible to everyone viewing the app!

### Post Tags

The AI assigns posts to these categories:

- **ai**: Artificial intelligence, ML, AI safety, alignment
- **science**: Biology, physics, chemistry, medicine, research
- **philosophy**: Ethics, metaphysics, epistemology, logic
- **technology**: Software, hardware, programming, tech industry
- **society**: Politics, culture, social issues, economics
- **personal**: Personal essays, life experiences, reflections
- **rationality**: Decision theory, cognitive science, effective thinking
- **math**: Mathematics, statistics, formal reasoning
- **history**: Historical events, analysis, context
- **art**: Literature, music, visual arts, creativity

## Architecture

- **tagger.py**: Python script that uses Claude API to tag posts
- **server.py**: Flask backend serving the tagged posts via API
- **index.html**: Modern single-page web interface
- **tagged_posts.json**: Cached results (generated after first run)

## API Endpoints

- `GET /api/posts` - Get all tagged posts
- `GET /api/tags` - Get all unique tags
- `GET /api/authors` - Get all unique authors

## Notes

- The tagger caches results, so you can safely re-run it - it will only process new posts
- Tags are assigned based on title and URL only (the feed doesn't include full content)
- Each API call to Claude costs a small amount - the default 50 posts is about $0.05
- Processing all ~1000+ posts would cost roughly $1-2

## Customization

To modify the available tags or tagging logic, edit the `tag_post()` method in `tagger.py`.

To change the UI styling, edit the `<style>` section in `index.html`.

---

Built with ❤️ using Claude, Flask, and vanilla JavaScript

