import whisper
import yt_dlp
import os
import json
from datetime import timedelta

class PodcastTranscriber:
    def __init__(self, youtube_url):
        self.youtube_url = youtube_url
        self.model = whisper.load_model("base")  # Use "small", "medium", or "large" for better accuracy
        
    def download_audio(self, output_path="audio"):
        """Download audio from YouTube video"""
        os.makedirs(output_path, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        }
        
        print("Downloading audio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.youtube_url, download=True)
            video_title = info.get('title', 'podcast')
            audio_file = f"{output_path}/{video_title}.mp3"
        
        print(f"Audio downloaded: {audio_file}")
        return audio_file
    
    def transcribe_with_timestamps(self, audio_path):
        """Transcribe audio with word-level timestamps"""
        print("Transcribing audio (this may take a while)...")
        
        # Transcribe with word timestamps
        result = self.model.transcribe(
            audio_path,
            word_timestamps=True,
            verbose=True
        )
        
        # Save the full transcription
        with open('transcription_full.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print("Transcription complete!")
        return result
    
    def create_segments(self, transcription, segment_duration=30):
        """Create overlapping segments with timestamps"""
        segments = []
        words = []
        
        # Extract all words with timestamps
        for segment in transcription['segments']:
            if 'words' in segment:
                words.extend(segment['words'])
        
        # Create segments of specified duration
        segment_words = []
        segment_start = None
        segment_end = None
        
        for word in words:
            if segment_start is None:
                segment_start = word['start']
            
            segment_words.append(word['word'])
            segment_end = word['end']
            
            # Check if segment duration is reached
            if segment_end - segment_start >= segment_duration:
                segments.append({
                    'start': segment_start,
                    'end': segment_end,
                    'text': ' '.join(segment_words),
                    'start_formatted': str(timedelta(seconds=int(segment_start))),
                    'end_formatted': str(timedelta(seconds=int(segment_end)))
                })
                
                # Overlap: move start to middle of current segment
                overlap_start = segment_start + (segment_end - segment_start) / 2
                segment_words = []
                segment_start = overlap_start
                
                # Include words that fall within the overlap
                for w in words:
                    if overlap_start <= w['start'] <= segment_end:
                        segment_words.append(w['word'])
        
        # Add last segment if any
        if segment_words:
            segments.append({
                'start': segment_start,
                'end': segment_end,
                'text': ' '.join(segment_words),
                'start_formatted': str(timedelta(seconds=int(segment_start))),
                'end_formatted': str(timedelta(seconds=int(segment_end)))
            })
        
        # Save segments
        with open('segments.json', 'w', encoding='utf-8') as f:
            json.dump(segments, f, indent=2, ensure_ascii=False)
        
        print(f"Created {len(segments)} segments")
        return segments

# Run the transcription
youtube_url = "Rni7Fz7208c&t"  # Replace with actual URL

# Run the transcription - Skip download, use local file
transcriber = PodcastTranscriber(youtube_url)
# audio_path = transcriber.download_audio()  # Comment this out
audio_path = "audio/podcast_audio.mp3"  # Use local file directly
transcription = transcriber.transcribe_with_timestamps(audio_path)
segments = transcriber.create_segments(transcription)