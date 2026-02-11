"""
YouTube Transcript Processor
Extracts transcripts from YouTube videos and converts them to event transcript format
"""
import re
import json
from typing import Dict, List, Optional
from datetime import datetime

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    raise ImportError("Please install youtube-transcript-api: pip install youtube-transcript-api")

try:
    from pytube import YouTube
except ImportError:
    YouTube = None  # Make pytube optional


class YouTubeProcessor:
    """Process YouTube videos to extract transcripts."""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats.
        
        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        - https://www.youtube.com/v/VIDEO_ID
        """
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
            r'(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def get_video_metadata(video_id: str) -> Dict:
        """Get video metadata using pytube."""
        if YouTube is None:
            # Fallback if pytube is not available
            return {
                'title': f'YouTube Video {video_id}',
                'author': 'Unknown',
                'length': 0,
                'views': 0,
                'publish_date': None,
                'description': ''
            }
        
        try:
            import ssl
            import certifi
            # Try to handle SSL certificate issues
            ssl._create_default_https_context = ssl._create_unverified_context
            
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            return {
                'title': yt.title,
                'author': yt.author,
                'length': yt.length,
                'views': yt.views,
                'publish_date': yt.publish_date.isoformat() if yt.publish_date else None,
                'description': yt.description
            }
        except Exception as e:
            print(f"Warning: Could not fetch metadata: {e}")
            return {
                'title': f'YouTube Video {video_id}',
                'author': 'Unknown',
                'length': 0,
                'views': 0,
                'publish_date': None,
                'description': ''
            }
    
    @staticmethod
    def get_transcript(video_id: str, languages: List[str] = None) -> List[Dict]:
        """
        Get transcript from YouTube video using youtube-transcript-api.
        
        Args:
            video_id: YouTube video ID
            languages: List of language codes to try (default: ['en'])
            
        Returns:
            List of transcript segments with text, start time, and duration
        """
        if languages is None:
            languages = ['en']
        
        try:
            # Create API instance and get transcript list
            api = YouTubeTranscriptApi()
            
            # Try to get transcript in specified languages
            transcript_list = api.list(video_id)
            
            # transcript_list is a list of available transcripts
            # Each transcript has language_code and is_generated properties
            selected_transcript = None
            
            # First, try to find manually created transcript in preferred languages
            for transcript in transcript_list:
                if hasattr(transcript, 'language_code') and transcript.language_code in languages:
                    if hasattr(transcript, 'is_generated') and not transcript.is_generated:
                        selected_transcript = transcript
                        break
            
            # If no manual transcript found, try auto-generated in preferred languages
            if not selected_transcript:
                for transcript in transcript_list:
                    if hasattr(transcript, 'language_code') and transcript.language_code in languages:
                        selected_transcript = transcript
                        break
            
            # If still nothing, just use the first available
            if not selected_transcript and transcript_list:
                selected_transcript = transcript_list[0]
            
            if not selected_transcript:
                raise Exception("No transcripts available for this video")
            
            # Fetch the actual transcript content
            transcript_data = selected_transcript.fetch()
            return transcript_data
            
        except AttributeError:
            # Fallback: Try the simpler direct method
            try:
                # Some versions might have a simpler API
                transcript_data = YouTubeTranscriptApi.fetch(video_id, languages=languages)
                return transcript_data
            except:
                pass
            
            # Another fallback
            try:
                transcript_data = YouTubeTranscriptApi.fetch(video_id)
                return transcript_data
            except:
                pass
                
        except Exception as e:
            error_msg = str(e)
            if "Subtitles are disabled" in error_msg or "No transcript" in error_msg or "Could not retrieve" in error_msg:
                raise Exception(
                    f"No transcript available for this video (ID: {video_id}). "
                    f"The video may have disabled captions or no captions have been created. "
                    f"Please try a different video with captions enabled."
                )
            else:
                raise Exception(f"Could not retrieve transcript: {error_msg}")
    
    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def segment_transcript(
        transcript: List,
        segment_duration: int = 120,
        min_words: int = 30
    ) -> List[Dict]:
        """
        Segment transcript into logical chunks.
        
        Args:
            transcript: Raw transcript from YouTube (list of objects or dicts)
            segment_duration: Target duration for each segment in seconds
            min_words: Minimum words per segment
            
        Returns:
            List of formatted transcript segments
        """
        segments = []
        current_segment = {
            'text': [],
            'start': 0,
            'end': 0,
            'word_count': 0
        }
        
        for entry in transcript:
            # Handle both dict and object formats
            if isinstance(entry, dict):
                text = entry.get('text', '').strip()
                start = entry.get('start', 0)
                duration = entry.get('duration', 0)
            else:
                # Handle object with attributes
                text = getattr(entry, 'text', '').strip()
                start = getattr(entry, 'start', 0)
                duration = getattr(entry, 'duration', 0)
            
            end = start + duration
            
            # Initialize first segment
            if current_segment['start'] == 0:
                current_segment['start'] = start
            
            # Add text to current segment
            current_segment['text'].append(text)
            current_segment['end'] = end
            current_segment['word_count'] += len(text.split())
            
            # Check if we should create a new segment
            segment_length = current_segment['end'] - current_segment['start']
            
            if (segment_length >= segment_duration and 
                current_segment['word_count'] >= min_words):
                
                # Save current segment
                segments.append({
                    'timestamp': YouTubeProcessor.format_timestamp(current_segment['start']),
                    'speaker': 'Speaker',  # We don't have speaker info from YouTube
                    'text': ' '.join(current_segment['text']),
                    'start_seconds': current_segment['start'],
                    'end_seconds': current_segment['end'],
                    'word_count': current_segment['word_count']
                })
                
                # Start new segment
                current_segment = {
                    'text': [],
                    'start': end,
                    'end': end,
                    'word_count': 0
                }
        
        # Add final segment if it has content
        if current_segment['text']:
            segments.append({
                'timestamp': YouTubeProcessor.format_timestamp(current_segment['start']),
                'speaker': 'Speaker',
                'text': ' '.join(current_segment['text']),
                'start_seconds': current_segment['start'],
                'end_seconds': current_segment['end'],
                'word_count': current_segment['word_count']
            })
        
        return segments
    
    @staticmethod
    def process_youtube_url(
        url: str,
        event_name: Optional[str] = None,
        event_date: Optional[str] = None,
        segment_duration: int = 120
    ) -> Dict:
        """
        Process a YouTube URL and convert to event transcript format.
        
        Args:
            url: YouTube video URL
            event_name: Optional event name (uses video title if not provided)
            event_date: Optional event date (uses publish date if not provided)
            segment_duration: Target duration for segments in seconds
            
        Returns:
            Dictionary in event transcript format compatible with the agent
        """
        # Extract video ID
        video_id = YouTubeProcessor.extract_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
        
        # Get metadata
        metadata = YouTubeProcessor.get_video_metadata(video_id)
        
        # Get transcript
        raw_transcript = YouTubeProcessor.get_transcript(video_id)
        
        # Segment transcript
        segments = YouTubeProcessor.segment_transcript(
            raw_transcript,
            segment_duration=segment_duration
        )
        
        # Calculate total statistics
        total_words = sum(seg['word_count'] for seg in segments)
        total_duration = segments[-1]['end_seconds'] if segments else 0
        
        # Format segments to match expected structure (add category and importance)
        formatted_segments = []
        for seg in segments:
            formatted_segments.append({
                'timestamp': seg['timestamp'],
                'speaker': seg['speaker'],
                'text': seg['text'],
                'category': 'general',  # Could be enhanced with AI categorization
                'importance': 'medium'  # Could be enhanced with AI analysis
            })
        
        # Format as event transcript matching the expected structure
        event_transcript = {
            'event_metadata': {
                'event_name': event_name or metadata['title'],
                'date': event_date or metadata['publish_date'] or datetime.now().isoformat().split('T')[0],
                'duration_minutes': int(total_duration / 60),
                'speakers': [
                    {
                        'name': metadata.get('author', 'Speaker'),
                        'role': 'Presenter',
                        'speaking_time': f"00:00-{YouTubeProcessor.format_timestamp(total_duration)}"
                    }
                ],
                'source': 'youtube',
                'video_metadata': {
                    'youtube_id': video_id,
                    'url': url,
                    'author': metadata['author'],
                    'views': metadata.get('views', 0),
                    'description': metadata['description'][:500] if metadata['description'] else ''
                }
            },
            'transcript_segments': formatted_segments,
            'statistics': {
                'total_segments': len(segments),
                'total_words': total_words,
                'duration_seconds': int(total_duration),
                'duration_formatted': YouTubeProcessor.format_timestamp(total_duration)
            },
            'processed_at': datetime.now().isoformat()
        }
        
        return event_transcript


def process_youtube_link(url: str) -> str:
    """
    Main function to process YouTube link and return formatted transcript.
    This is the entry point used by the Flask app.
    
    Args:
        url: YouTube video URL
        
    Returns:
        JSON string of the event transcript
    """
    processor = YouTubeProcessor()
    transcript = processor.process_youtube_url(url)
    return json.dumps(transcript, indent=2)


# Example usage
if __name__ == '__main__':
    # Test with a sample URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        result = process_youtube_link(test_url)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
