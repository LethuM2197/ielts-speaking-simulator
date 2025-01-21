import React, { useState, useRef, useEffect } from 'react';
import {
  ChakraProvider,
  Box,
  VStack,
  Heading,
  Button,
  Text,
  Progress,
  useToast,
  Grid,
  GridItem,
  List,
  ListItem,
  ListIcon,
} from '@chakra-ui/react';
import { MdCheckCircle, MdWarning } from 'react-icons/md';

// IELTS Test Questions
const IELTS_QUESTIONS = {
  1: [
    "What is your name?",
    "Where are you from?",
    "Do you work or study?",
    "What do you like about your job/studies?"
  ],
  2: {
    topic: "Describe a place you like to visit.",
    points: [
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
};

function App() {
  const [mode, setMode] = useState<'practice' | 'test' | null>(null);
  const [currentPart, setCurrentPart] = useState(1);
  const [isRecording, setIsRecording] = useState(false);
  const [responses, setResponses] = useState<any[]>([]);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const toast = useToast();

  useEffect(() => {
    // Clean up audio URL when component unmounts
    return () => {
      if (audioURL) {
        URL.revokeObjectURL(audioURL);
      }
    };
  }, [audioURL]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (e) => {
        audioChunks.current.push(e.data);
      };

      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);

        // Simulate speech-to-text and analysis
        // In a production environment, you would send the audio to a server
        // for processing with a speech-to-text service
        await simulateAnalysis();
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      
      // Record for 30 seconds
      setTimeout(() => {
        if (mediaRecorder.current?.state === 'recording') {
          mediaRecorder.current.stop();
          setIsRecording(false);
          
          // Stop all tracks in the stream
          stream.getTracks().forEach(track => track.stop());
        }
      }, 30000);
    } catch (err) {
      toast({
        title: 'Error',
        description: 'Could not access microphone. Please check permissions.',
        status: 'error',
        duration: 5000,
      });
    }
  };

  const simulateAnalysis = async () => {
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    const analysis = {
      scores: {
        fluency: 7,
        vocabulary: 6,
        grammar: 7,
        pronunciation: 6
      },
      feedback: {
        strengths: [
          "Good use of linking words",
          "Clear expression of ideas",
          "Appropriate vocabulary usage"
        ],
        improvements: [
          "Work on reducing hesitations",
          "Practice more complex grammatical structures",
          "Focus on word stress patterns"
        ]
      }
    };

    setResponses([...responses, {
      part: currentPart,
      analysis
    }]);
  };

  const renderCurrentSection = () => {
    switch (currentPart) {
      case 1:
        return (
          <Box>
            <Heading size="md" mb={4}>Part 1: Introduction and Interview</Heading>
            <List spacing={3}>
              {IELTS_QUESTIONS[1].map((q, i) => (
                <ListItem key={i}>{q}</ListItem>
              ))}
            </List>
          </Box>
        );
      case 2:
        return (
          <Box>
            <Heading size="md" mb={4}>Part 2: Long Turn</Heading>
            <Text fontWeight="bold">{IELTS_QUESTIONS[2].topic}</Text>
            <Text mt={2}>You should say:</Text>
            <List spacing={3} mt={2}>
              {IELTS_QUESTIONS[2].points.map((point, i) => (
                <ListItem key={i}>{point}</ListItem>
              ))}
            </List>
          </Box>
        );
      case 3:
        return (
          <Box>
            <Heading size="md" mb={4}>Part 3: Discussion</Heading>
            <List spacing={3}>
              {IELTS_QUESTIONS[3].map((q, i) => (
                <ListItem key={i}>{q}</ListItem>
              ))}
            </List>
          </Box>
        );
    }
  };

  const renderFeedback = () => {
    const lastResponse = responses[responses.length - 1];
    if (!lastResponse) return null;

    return (
      <Box mt={6}>
        <Heading size="md" mb={4}>Feedback</Heading>
        <Grid templateColumns="repeat(4, 1fr)" gap={4} mb={6}>
          <GridItem>
            <Text fontWeight="bold">Fluency</Text>
            <Progress value={lastResponse.analysis.scores.fluency * 11.11} />
            <Text>{lastResponse.analysis.scores.fluency}/9</Text>
          </GridItem>
          <GridItem>
            <Text fontWeight="bold">Vocabulary</Text>
            <Progress value={lastResponse.analysis.scores.vocabulary * 11.11} />
            <Text>{lastResponse.analysis.scores.vocabulary}/9</Text>
          </GridItem>
          <GridItem>
            <Text fontWeight="bold">Grammar</Text>
            <Progress value={lastResponse.analysis.scores.grammar * 11.11} />
            <Text>{lastResponse.analysis.scores.grammar}/9</Text>
          </GridItem>
          <GridItem>
            <Text fontWeight="bold">Pronunciation</Text>
            <Progress value={lastResponse.analysis.scores.pronunciation * 11.11} />
            <Text>{lastResponse.analysis.scores.pronunciation}/9</Text>
          </GridItem>
        </Grid>
        
        <Box>
          <Heading size="sm" mb={2}>Strengths</Heading>
          <List spacing={2}>
            {lastResponse.analysis.feedback.strengths.map((strength: string, i: number) => (
              <ListItem key={i}>
                <ListIcon as={MdCheckCircle} color="green.500" />
                {strength}
              </ListItem>
            ))}
          </List>
        </Box>
        
        <Box mt={4}>
          <Heading size="sm" mb={2}>Areas for Improvement</Heading>
          <List spacing={2}>
            {lastResponse.analysis.feedback.improvements.map((improvement: string, i: number) => (
              <ListItem key={i}>
                <ListIcon as={MdWarning} color="orange.500" />
                {improvement}
              </ListItem>
            ))}
          </List>
        </Box>
      </Box>
    );
  };

  if (!mode) {
    return (
      <ChakraProvider>
        <Box p={8}>
          <VStack spacing={6}>
            <Heading>IELTS Speaking Test Simulator</Heading>
            <Text>Welcome! Please select a mode to begin:</Text>
            <Button colorScheme="blue" onClick={() => setMode('practice')}>
              Practice Mode
            </Button>
            <Button colorScheme="green" onClick={() => setMode('test')}>
              Test Mode
            </Button>
          </VStack>
        </Box>
      </ChakraProvider>
    );
  }

  return (
    <ChakraProvider>
      <Box p={8}>
        <VStack spacing={6} align="stretch">
          <Heading>IELTS Speaking Test Simulator</Heading>
          <Text>Current Mode: {mode === 'practice' ? 'Practice' : 'Test'}</Text>
          
          {mode === 'test' && (
            <Text>Part {currentPart} of 3</Text>
          )}
          
          {renderCurrentSection()}
          
          <Button
            colorScheme={isRecording ? 'red' : 'blue'}
            onClick={startRecording}
            isDisabled={isRecording}
          >
            {isRecording ? 'Recording...' : 'Start Recording'}
          </Button>

          {audioURL && (
            <Box>
              <Heading size="sm" mb={2}>Your Recording</Heading>
              <audio src={audioURL} controls />
            </Box>
          )}
          
          {renderFeedback()}
          
          {mode === 'test' && (
            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
              <Button
                isDisabled={currentPart === 1}
                onClick={() => setCurrentPart(prev => prev - 1)}
              >
                Previous Part
              </Button>
              <Button
                isDisabled={currentPart === 3}
                onClick={() => setCurrentPart(prev => prev + 1)}
              >
                Next Part
              </Button>
            </Grid>
          )}
          
          <Button
            colorScheme="red"
            onClick={() => {
              setMode(null);
              setCurrentPart(1);
              setResponses([]);
              setAudioURL(null);
            }}
          >
            Reset Test
          </Button>
        </VStack>
      </Box>
    </ChakraProvider>
  );
}

export default App;