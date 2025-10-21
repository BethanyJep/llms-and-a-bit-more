"""
YouTube Transcript Processor
Extracts transcripts from YouTube videos and converts them to event transcript format
"""
import re
import json
from typing import Dict, List, Optional
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube


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
        try:
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
                'title': 'YouTube Video',
                'author': 'Unknown',
                'length': 0,
                'views': 0,
                'publish_date': None,
                'description': ''
            }
    
    @staticmethod
    def get_transcript(video_id: str, languages: List[str] = None) -> List[Dict]:
        """
        Get transcript from YouTube video.
        
        Args:
            video_id: YouTube video ID
            languages: List of language codes to try (default: ['en'])
            
        Returns:
            List of transcript segments with text, start time, and duration
        """
        if languages is None:
            languages = ['en']
        
        try:
            # Try to get transcript in specified languages
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to find transcript in requested languages
            for lang in languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    return transcript.fetch()
                except:
                    continue
            
            # If no exact match, try to get any available transcript
            try:
                transcript = transcript_list.find_generated_transcript(languages)
                return transcript.fetch()
            except:
                # Get first available transcript
                available = transcript_list._manually_created_transcripts
                if not available:
                    available = transcript_list._generated_transcripts
                
                if available:
                    first_transcript = list(available.values())[0]
                    return first_transcript.fetch()
                
        except Exception as e:
            raise Exception(f"Could not retrieve transcript: {str(e)}")
    
    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def segment_transcript(
        transcript: List[Dict],
        segment_duration: int = 120,
        min_words: int = 30
    ) -> List[Dict]:
        """
        Segment transcript into logical chunks.
        
        Args:
            transcript: Raw transcript from YouTube
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
            text = entry['text'].strip()
            start = entry['start']
            duration = entry['duration']
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
        
        # Format as event transcript
        event_transcript = {
            'event_name': event_name or metadata['title'],
            'event_date': event_date or metadata['publish_date'] or datetime.now().isoformat(),
            'video_metadata': {
                'youtube_id': video_id,
                'url': url,
                'author': metadata['author'],
                'views': metadata['views'],
                'description': metadata['description'][:500] if metadata['description'] else ''
            },
            'duration_seconds': int(total_duration),
            'duration_formatted': YouTubeProcessor.format_timestamp(total_duration),
            'total_segments': len(segments),
            'total_words': total_words,
            'segments': segments,
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
