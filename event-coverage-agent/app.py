"""
Flask Web Application for Event Coverage Agent
Provides a user-friendly UI to demo the agent's capabilities
"""
from flask import Flask, render_template, request, jsonify, send_file
import asyncio
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from server import (
    process_event_transcript,
    extract_press_quotes,
    generate_social_media_posts,
    create_press_release,
    generate_newsletter_recap,
    run_full_coverage_cycle
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Store generated content in memory (in production, use a database)
generated_content = {
    'transcript': None,
    'quotes': None,
    'twitter': None,
    'linkedin': None,
    'instagram': None,
    'press_release': None,
    'newsletter': None,
    'last_updated': None
}


@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')


@app.route('/api/process-transcript', methods=['POST'])
def process_transcript():
    """Process event transcript and prepare for content generation."""
    try:
        data = request.json
        event_file = data.get('event_file', 'mock_transcript.json')
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(process_event_transcript(event_file))
        loop.close()
        
        # Store result
        generated_content['transcript'] = json.loads(result)
        generated_content['last_updated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': json.loads(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-quotes', methods=['POST'])
def generate_quotes():
    """Generate press-ready quotes."""
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(extract_press_quotes())
        loop.close()
        
        # Store result
        generated_content['quotes'] = json.loads(result)
        generated_content['last_updated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': json.loads(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-social/<platform>', methods=['POST'])
def generate_social(platform):
    """Generate social media posts for specified platform."""
    try:
        if platform not in ['twitter', 'linkedin', 'instagram']:
            return jsonify({
                'success': False,
                'error': 'Invalid platform'
            }), 400
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_social_media_posts(platform))
        loop.close()
        
        # Store result
        generated_content[platform] = json.loads(result)
        generated_content['last_updated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': json.loads(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-press-release', methods=['POST'])
def generate_press_release():
    """Generate press release."""
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(create_press_release())
        loop.close()
        
        # Store result
        generated_content['press_release'] = json.loads(result)
        generated_content['last_updated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': json.loads(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-newsletter', methods=['POST'])
def generate_newsletter():
    """Generate newsletter recap."""
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_newsletter_recap())
        loop.close()
        
        # Store result
        generated_content['newsletter'] = json.loads(result)
        generated_content['last_updated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': json.loads(result)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-all', methods=['POST'])
def generate_all():
    """Generate all content types at once."""
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_full_coverage_cycle())
        loop.close()
        
        result_data = json.loads(result)
        
        # Store all results
        if result_data.get('status') == 'success':
            outputs = result_data.get('outputs', {})
            generated_content['transcript'] = outputs.get('transcript_analysis')
            generated_content['quotes'] = outputs.get('press_quotes')
            generated_content['twitter'] = outputs.get('social_media', {}).get('twitter')
            generated_content['linkedin'] = outputs.get('social_media', {}).get('linkedin')
            generated_content['press_release'] = outputs.get('press_release')
            generated_content['newsletter'] = outputs.get('newsletter')
            generated_content['last_updated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': result_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/<content_type>', methods=['GET'])
def export_content(content_type):
    """Export generated content as downloadable file."""
    try:
        if content_type not in generated_content or not generated_content[content_type]:
            return jsonify({
                'success': False,
                'error': 'Content not generated yet'
            }), 400
        
        # Create export file
        export_data = generated_content[content_type]
        
        # Format based on content type
        if content_type == 'press_release':
            content = export_data.get('press_release', '')
            filename = 'press_release.txt'
        elif content_type == 'newsletter':
            content = export_data.get('newsletter', '')
            filename = 'newsletter.txt'
        elif content_type in ['twitter', 'linkedin', 'instagram']:
            posts = export_data.get('posts', [])
            content = '\n\n---\n\n'.join([p.get('content', str(p)) for p in posts])
            filename = f'{content_type}_posts.txt'
        elif content_type == 'quotes':
            quotes = export_data.get('quotes', [])
            content = '\n\n'.join([q.get('formatted', str(q)) for q in quotes])
            filename = 'press_quotes.txt'
        else:
            content = json.dumps(export_data, indent=2)
            filename = f'{content_type}.json'
        
        # Save to temp file
        temp_file = Path(f'/tmp/{filename}')
        with open(temp_file, 'w') as f:
            f.write(content)
        
        return send_file(
            temp_file,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current generation status."""
    status = {
        'transcript_processed': generated_content['transcript'] is not None,
        'quotes_generated': generated_content['quotes'] is not None,
        'twitter_generated': generated_content['twitter'] is not None,
        'linkedin_generated': generated_content['linkedin'] is not None,
        'instagram_generated': generated_content['instagram'] is not None,
        'press_release_generated': generated_content['press_release'] is not None,
        'newsletter_generated': generated_content['newsletter'] is not None,
        'last_updated': generated_content['last_updated']
    }
    
    return jsonify(status)


@app.route('/api/clear', methods=['POST'])
def clear_content():
    """Clear all generated content."""
    global generated_content
    generated_content = {
        'transcript': None,
        'quotes': None,
        'twitter': None,
        'linkedin': None,
        'instagram': None,
        'press_release': None,
        'newsletter': None,
        'last_updated': None
    }
    
    return jsonify({'success': True})


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Create static directory if it doesn't exist
    static_dir = Path(__file__).parent / 'static'
    static_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("🎤 Event Coverage Agent - Web UI")
    print("=" * 60)
    print("\n🚀 Starting Flask server...")
    print("📍 Open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
