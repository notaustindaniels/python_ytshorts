# Video Content Generation

This project is a Python application that automates the process of generating video content. It uses OpenAI's API to generate scripts, system subprocess to generate voiceovers, AssemblyAI to generate subtitles, and Dalle to generate images, and then concatenates them into a final video.

## Getting Started

### Prerequisites

- Python 3.11
- OpenAI API key
- AssemblyAI API key
- ffmpeg (can be installed via Homebrew on macOS with `brew install ffmpeg`)

### Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    ```
2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY=<your_api_key>
    ASSEMBLYAI_API_KEY=<your_assemblyai_api_key>
    ```
4. Activate the virtual environment:
    ```
    source myvenv/bin/activate
    ```

### Usage

Run the main script:
```sh
python main.py

## Scripts

- `input_processing.py`: Processes the input to generate a video idea.
- `script_generation.py`: Generates a script based on the video idea.
- `voiceover_generation.py`: Generates a voiceover from the script.
- `timestamp_subtitle_generation.py`: Generates subtitles from the audio file.
- `image_generation.py`: Generates images based on the sentences in the subtitles.
- `video_concatenation.py`: Concatenates the images, audio file, and subtitles into a final video.
- `burn_subtitles.py`: Burns the subtitles into the final video.