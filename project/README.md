# IELTS Speaking Test Simulator

This application provides a real-time IELTS Speaking Test simulation using Python, Streamlit, and OpenAI's GPT-4 for analysis.

## Features

- Practice Mode and Test Mode
- Real-time audio recording
- Automated scoring and feedback
- Part 1, 2, and 3 of IELTS Speaking Test
- Detailed analysis of fluency, vocabulary, grammar, and pronunciation
- Progress tracking
- Downloadable session reports

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your OpenAI API key:
   - Copy the `.env.example` file to `.env`
   - Add your OpenAI API key to the `.env` file

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select either Practice Mode or Test Mode
2. Follow the on-screen instructions
3. Click "Start Recording" to begin speaking
4. Receive instant feedback and scores
5. Navigate through different parts of the test (in Test Mode)

## Technical Details

- Built with Python 3.8+
- Uses Streamlit for the web interface
- Integrates OpenAI's GPT-4 for response analysis
- Records audio using sounddevice
- Stores session data locally

## Note

This is a demonstration version. In a production environment, you would want to:
- Implement proper speech-to-text conversion
- Add user authentication
- Include more robust error handling
- Add proper data persistence
- Implement more sophisticated scoring algorithm