from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from dotenv import load_dotenv
from groq import Groq
import os
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(url):
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL. Please check and try again.")
    try:
        ytt = YouTubeTranscriptApi()
        
        transcript_list = ytt.list(video_id)
        
        try:
            transcript = transcript_list.find_manually_created_transcript(
                [t.language_code for t in transcript_list]
            )
        except:
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )
        
        fetched = transcript.fetch()
        text = " ".join([t.text for t in fetched])
        return text[:12000]

    except TranscriptsDisabled:
        raise ValueError("This video has captions disabled. Try another video.")
    except NoTranscriptFound:
        raise ValueError("No transcript found for this video.")
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {str(e)}")

def generate_summary(transcript):
    prompt = f"""
You are an expert lecture summariser. Always respond in English only, regardless of the language of the transcript.
Given the following lecture transcript, generate:
1. A concise structured summary with clear topic-wise bullet points
2. Key takeaways at the end

Transcript:
{transcript}

Format your response exactly like this:

## 📋 Summary
- [bullet point 1]
- [bullet point 2]

## ✅ Key Takeaways
- [takeaway 1]
- [takeaway 2]
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_quiz(transcript):
    prompt = f"""
You are an expert quiz maker for students.
Based on the lecture transcript below, generate exactly 10 multiple choice questions.
Always respond in English only, regardless of the language of the transcript.

Transcript:
{transcript}

Format EXACTLY like this — no extra text, no markdown, just this structure:

Q1: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q2: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q3: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q4: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q5: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q6: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q7: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q8: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q9: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]

Q10: [Question here]
A: [option A]
B: [option B]
C: [option C]
D: [option D]
ANSWER: [A or B or C or D]
EXPLANATION: [one sentence explanation]
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
