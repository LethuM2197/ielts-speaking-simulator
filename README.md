


aiIntegrator
IELTS Speaking Test Simulator
An advanced tool to simulate the IELTS Speaking Test, offering real-time feedback, scoring, and detailed analysis powered by AI and modern web technologies.

Features
🎯 Practice Mode and Test Mode
🎤 Real-time Speech-to-Text integration
📊 Automated scoring and personalized feedback
📝 Simulation of the complete IELTS Speaking Test (Parts 1, 2, and 3)
📈 Detailed performance breakdown:
Fluency
Vocabulary
Grammar
Pronunciation
🔄 Progress tracking over multiple sessions
🎯 Instant, actionable insights for improvement
🎨 User-friendly interface built with Chakra UI
Prerequisites
Before you begin, make sure you have the following installed:

Node.js (v14.0.0 or higher)
npm (v6.0.0 or higher)
A modern web browser
Google Cloud credentials for Speech-to-Text
OpenAI API key
Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/LethuM2197/ielts-speaking-simulator.git  
Navigate to the project directory:

bash
Copy
Edit
cd ielts-speaking-simulator  
Install dependencies:

bash
Copy
Edit
npm install  
Set up environment variables:
Create a .env file in the root directory and add your credentials:

makefile
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here  
GOOGLE_APPLICATION_CREDENTIALS=path_to_google_credentials.json  
Running the Application
Frontend (React):
Start the development server:

bash
Copy
Edit
npm run dev  
Open your browser and navigate to:

arduino
Copy
Edit
http://127.0.0.1:5173/  
Backend (Streamlit):
Navigate to the backend directory and run:

bash
Copy
Edit
streamlit run app.py  
Project Structure
php
Copy
Edit
ielts-speaking-simulator/  
├── frontend/  
│   ├── src/  
│   │   ├── App.tsx           # Main application component  
│   │   ├── main.tsx          # Application entry point  
│   │   └── vite-env.d.ts     # TypeScript declarations  
│   ├── public/               # Static assets  
│   ├── package.json          # Project dependencies and scripts  
│   ├── tsconfig.json         # TypeScript configuration  
│   ├── vite.config.ts        # Vite configuration  
│   └── README.md             # Project documentation  
├── backend/  
│   ├── app.py                # Streamlit backend  
│   ├── requirements.txt      # Python dependencies  
│   ├── models/               # Scoring and feedback models  
│   └── utils/                # Helper functions  
Technologies Used
React 18
TypeScript
Vite
Chakra UI
OpenAI API
Google Cloud Speech-to-Text
Streamlit (Backend)
Python
Web Audio API
Available Scripts
Frontend
npm run dev - Start development server
npm run build - Build for production
npm run preview - Preview production build
Backend
streamlit run app.py - Start backend server
Browser Support
This application works with all modern browsers supporting the MediaRecorder API:

Chrome (latest)
Firefox (latest)
Safari (latest)
Edge (latest)
Contributing
Fork the repository
Create a feature branch:
bash
Copy
Edit
git checkout -b feature/AmazingFeature  
Commit your changes:
bash
Copy
Edit
git commit -m 'Add some AmazingFeature'  
Push to the branch:
bash
Copy
Edit
git push origin feature/AmazingFeature  
Open a Pull Request
Known Issues
HTTPS is required for audio recording in production environments
Microphone access requires explicit browser permissions
Future Improvements
Add user authentication for personalized tracking
Expand question bank for practice
Include sample answers and band score benchmarks
Support offline access
Integrate advanced analytics for progress tracking
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
IELTS Format and scoring inspired by official guidelines
Chakra UI for intuitive design components
Web Audio API for audio processing
