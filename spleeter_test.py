import os
from spleeter.separator import Separator

def separate_audio(input_path, output_dir='output'):
    """
    Separate audio into stems using Spleeter.
    
    Args:
        input_path (str): Path to input audio file
        output_dir (str): Directory to save separated stems
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Download the model if not already downloaded
        #spleeter_test.download('2stems')
        
        # Initialize separator
        separator = Separator('spleeter:2stems')
        
        # Perform separation
        separator.separate_to_file(input_path, output_dir)
        
        print(f"Audio separation completed. Output saved to {output_dir}")
        
    except Exception as e:
        print(f"Error during audio separation: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_audio = 'input/Not_Like_Us.mp3'
    separate_audio(input_audio)


