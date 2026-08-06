import subprocess
import sys
import os

def run_step(step_name, script_name):
    print(f"\n{'='*50}")
    print(f"Running {step_name}...")
    print(f"{'='*50}\n")
    
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ {step_name} completed successfully")
        print(result.stdout)
    else:
        print(f"✗ {step_name} failed")
        print(result.stderr)
        sys.exit(1)

def main():
    print("Starting Podcast Bot Setup...")
    
    # Step 1: Check if transcription exists
    if not os.path.exists('segments.json'):
        print("\nStep 1: Transcribing podcast...")
        run_step("Transcription", "transcribe_podcast.py")
    else:
        print("\nStep 1: Transcription already exists, skipping...")
    
    # Step 2: Build search index
    if not os.path.exists('podcast_index.faiss'):
        print("\nStep 2: Building search index...")
        run_step("Index Building", "build_index.py")
    else:
        print("\nStep 2: Search index already exists, skipping...")
    
    # Step 3: Start web application
    print("\nStep 3: Starting web application...")
    print("\n" + "="*50)
    print("Podcast Bot is ready!")
    print("Open your browser and go to: http://localhost:5000")
    print("="*50 + "\n")
    
    # Start Flask app
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    main()