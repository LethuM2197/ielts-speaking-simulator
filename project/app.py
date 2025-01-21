import streamlit as st
import openai
import sounddevice as sd
import numpy as np
import wave
import os
from datetime import datetime
import json
from dotenv import load_dotenv
from process_audio import process_audio

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize session state
if 'current_part' not in st.session_state:
    st.session_state.current_part = 1
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'mode' not in st.session_state:
    st.session_state.mode = None

# IELTS Test Questions
IELTS_QUESTIONS = {
    1: [
        "What is your name?",
        "Where are you from?",
        "Do you work or study?",
        "What do you like about your job/studies?"
    ],
    2: {
        "topic": "Describe a place you like to visit.",
        "points": [
            "Where it is",
            "When you go there",
            "What you do there",
            "Why you like it"
        ]
    },
    3: [
        "What makes a place worth visiting?",
        "How has tourism changed in recent years?",
        "What are the benefits and drawbacks of tourism?"
    ]
}

# Mir colors (you can update with specific colors as per your requirements)
MIR_COLORS = {
    "primary": "#4CBB77",  # Green
    "secondary": "#FF9F00",  # Orange
    "background": "#f8f9fa",  # Light gray background
    "text": "#212529",  # Dark text
    "button": "#007BFF",  # Blue button
}

def list_devices():
    """List all available audio devices"""
    print("Available devices:")
    print(sd.query_devices())

def record_audio(duration=30):
    """Record audio for a specified duration with device handling"""
    sample_rate = 44100
    
    # List available devices to help with device selection
    list_devices()

    # Prompt user to select a device (replace this with device selection logic in your app if necessary)
    device_index = st.number_input("Enter the device index from the list above", min_value=0, step=1)

    try:
        print("Recording...")
        recording = sd.rec(int(duration * sample_rate),
                          samplerate=sample_rate,
                          channels=1,
                          dtype=np.int16,
                          device=device_index)  # Specify device index
        sd.wait()
        print("Recording complete!")
        return recording, sample_rate
    except sd.PortAudioError as e:
        st.error(f"Error opening device: {e}")
        return None, None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None, None

def save_audio(recording, sample_rate, filename="temp_recording.wav"):
    """Save the recorded audio to a WAV file"""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())
    return filename

def analyze_response(text):
    """Analyze the response using OpenAI API"""
    prompt = f"""
    Analyze the following IELTS speaking response and provide scores and feedback:
    Response: {text}
    
    Provide analysis in the following JSON format:
    {{
        "scores": {{
            "fluency": <score 0-9>,
            "vocabulary": <score 0-9>,
            "grammar": <score 0-9>,
            "pronunciation": <score 0-9>
        }},
        "feedback": {{
            "strengths": [<list of strengths>],
            "improvements": [<list of areas to improve>]
        }}
    }}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.choices[0].message.content)

# Custom CSS for Mir colors
st.markdown(f"""
    <style>
        body {{
            background-color: {MIR_COLORS['background']};
            color: {MIR_COLORS['text']};
        }}
        .stButton {{
            background-color: {MIR_COLORS['button']};
            color: white;
        }}
        .stButton:hover {{
            background-color: {MIR_COLORS['primary']};
        }}
        .stSelectbox, .stSlider, .stTextInput {{
            background-color: {MIR_COLORS['secondary']};
            color: {MIR_COLORS['text']};
        }}
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("IELTS Speaking Test Simulator")
    
    if not openai.api_key:
        st.error("OpenAI API key is missing. Please configure it in the environment variables.")
        return
    
    # Mode selection
    if st.session_state.mode is None:
        st.write("Welcome! Please select a mode to begin:")
        if st.button("Practice Mode"):
            st.session_state.mode = "practice"
        if st.button("Test Mode"):
            st.session_state.mode = "test"
        return

    # Display the current mode
    st.write(f"Current Mode: {st.session_state.mode.title()}")

    # Display content for Practice Mode
    if st.session_state.mode == "practice":
        st.subheader("Part 1: Introduction and Interview")
        questions = [
            "What is your name?",
            "Where are you from?",
            "Do you work or study?",
            "What do you like about your job/studies?"
        ]
        for q in questions:
            st.write(q)

        # Recording settings
        duration = st.slider("Set Recording Duration (seconds)", min_value=10, max_value=60, value=30)

        # Recording and feedback
        if st.button("Start Recording"):
            with st.spinner("Recording... Speak now!"):
                recording, sample_rate = record_audio(duration)
                if recording is not None:
                    audio_file = save_audio(recording, sample_rate)
                    if audio_file:
                        st.audio(audio_file)

                        # Process the audio
                        transcription = process_audio(audio_file)
                        if transcription:
                            st.write("Your response:", transcription)

                            # Analyze the response
                            analysis = analyze_response(transcription)
                            if analysis:
                                st.write("### Feedback")
                                st.write("**Fluency:**", f"{analysis['scores']['fluency']}/9")
                                st.write("**Vocabulary:**", f"{analysis['scores']['vocabulary']}/9")
                                st.write("**Grammar:**", f"{analysis['scores']['grammar']}/9")
                                st.write("**Pronunciation:**", f"{analysis['scores']['pronunciation']}/9")

                                st.write("**Strengths:**")
                                for strength in analysis['feedback']['strengths']:
                                    st.write(f"- {strength}")

                                st.write("**Areas for Improvement:**")
                                for improvement in analysis['feedback']['improvements']:
                                    st.write(f"- {improvement}")
                            else:
                                st.error("Unable to analyze the response. Please try again.")
                        else:
                            st.error("Failed to process the audio. Please try again.")

    # Display content for Test Mode
    elif st.session_state.mode == "test":
        # Show questions based on current part
        if st.session_state.current_part == 1:
            st.subheader("Part 1: Introduction and Interview")
            for q in IELTS_QUESTIONS[1]:
                st.write(q)
        elif st.session_state.current_part == 2:
            st.subheader("Part 2: Long Turn")
            st.write(IELTS_QUESTIONS[2]["topic"])
            st.write("You should say:")
            for point in IELTS_QUESTIONS[2]["points"]:
                st.write(f"- {point}")
        elif st.session_state.current_part == 3:
            st.subheader("Part 3: Discussion")
            for q in IELTS_QUESTIONS[3]:
                st.write(q)

        # Recording settings for test mode
        duration = st.slider("Set Recording Duration (seconds)", min_value=10, max_value=60, value=30)

        # Recording and feedback for test mode
        if st.button("Start Recording"):
            with st.spinner("Recording... Speak now!"):
                recording, sample_rate = record_audio(duration)
                if recording is not None:
                    audio_file = save_audio(recording, sample_rate)
                    if audio_file:
                        st.audio(audio_file)

                        # Process the audio
                        transcription = process_audio(audio_file)
                        if transcription:
                            st.write("Your response:", transcription)

                            # Analyze the response
                            analysis = analyze_response(transcription)
                            if analysis:
                                st.write("### Feedback")
                                st.write("**Fluency:**", f"{analysis['scores']['fluency']}/9")
                                st.write("**Vocabulary:**", f"{analysis['scores']['vocabulary']}/9")
                                st.write("**Grammar:**", f"{analysis['scores']['grammar']}/9")
                                st.write("**Pronunciation:**", f"{analysis['scores']['pronunciation']}/9")

                                st.write("**Strengths:**")
                                for strength in analysis['feedback']['strengths']:
                                    st.write(f"- {strength}")

                                st.write("**Areas for Improvement:**")
                                for improvement in analysis['feedback']['improvements']:
                                    st.write(f"- {improvement}")
                            else:
                                st.error("Unable to analyze the response. Please try again.")
                        else:
                            st.error("Failed to process the audio. Please try again.")

        # Navigation buttons for the test mode
        if st.session_state.current_part > 1:
            if st.button("Previous Part"):
                st.session_state.current_part -= 1

        if st.session_state.current_part < 3:
            if st.button("Next Part"):
                st.session_state.current_part += 1

        # Reset Test
        if st.button("Reset Test"):
            st.session_state.current_part = 1
            st.session_state.responses = []

if __name__ == "__main__":
    main()
