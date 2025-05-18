import librosa
import soundfile as sf
import numpy as np
import subprocess
import os

def convert_mp3_to_wav(mp3_path):
    # Create a temporary WAV file path
    wav_path = mp3_path.rsplit('.', 1)[0] + '_temp.wav'
    
    # Convert MP3 to WAV using ffmpeg
    try:
        subprocess.run(['ffmpeg', '-i', mp3_path, wav_path], 
                      check=True, 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        return wav_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting file: {e}")
        raise

def remove_vocals(input_file, output_file):
    # If input is MP3, convert to WAV first
    if input_file.lower().endswith('.mp3'):
        print("Converting MP3 to WAV format...")
        input_file = convert_mp3_to_wav(input_file)
    
    # Load the audio file
    print("Loading audio file...")
    y, sr = librosa.load(input_file, mono=False)
    
    # If the audio is mono, convert to stereo
    if len(y.shape) == 1:
        print("Converting audio to stereo")
        y = np.vstack((y, y))
    
    # Extract the center channel (where vocals are typically located)
    print("Removing vocals...")
    center = (y[0] + y[1]) / 2
    
    # Create the instrumental version by subtracting the center channel
    instrumental = y - center
    
    # Normalize the audio
    instrumental = instrumental / np.max(np.abs(instrumental))
    
    # Save the result
    print("Saving output file...")
    sf.write(output_file, instrumental.T, sr)
    
    # Clean up temporary WAV file if it was created
    if input_file.endswith('_temp.wav'):
        os.remove(input_file)

if __name__ == "__main__":
    input_file = "data/Not_Like_Us.mp3"
    output_file = "data/instrumental_not_like_us.wav"
    
    try:
        remove_vocals(input_file, output_file)
        print(f"Vocal removal completed. Output saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
