from youtube_transcript_api import YouTubeTranscriptApi
import os
import json
from googleapiclient.discovery import build
import google.generativeai as genai

API_KEY = os.getenv("GCP_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
class Youtube:
    def __init__(self):
        pass
    
    def get_transcript(self, video_id):
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        text_list = [item['text'] for item in transcript]

        return " ".join(text_list)
    
    def get_title_description(self, video_id):
        youtube = build("youtube", "v3", developerKey=API_KEY)

        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        
        title = response["items"][0]["snippet"]["title"]
        description = response["items"][0]["snippet"]["description"]
        
        return {"title": title, "description": description}
    
    def get_formatted_job_openings(self, title, description, transcription):
        
        prompt = f"""
            IMPORTANT:
            - Respond with STRICT VALID JSON only.
            - No markdown.
            - No explanations.
            - No trailing commas.

            You are an AI assistant that extracts job and internship openings from YouTube videos.

            Input Data:

            Video Title:
            {title}

            Video Description:
            {description}

            Video Transcript:
            {transcription}

            Your Tasks:
            1. Determine whether this video contains one or more genuine job or internship openings.
            2. If multiple openings are mentioned, extract EACH opening separately.
            3. Ignore promotions, sponsorships, personal mentoring, WhatsApp channels, referrals, discounts, and unrelated links.
            4. Prefer official application links (Google Forms, company career pages, HR-shared links).
            5. Normalize and correct company names if misspelled due to transcription errors.
            6. If workMode is "Remote", set location explicitly to "WFH".

            Return STRICT JSON in the following schema ONLY:

            {{
            "isJobVideo": boolean,
            "openings": [
                {{
                "company": "string" | null,
                "role": "string" | null,
                "employmentType": "Internship" | "Full-time" | "Contract" | null,
                "workMode": "On-site" | "Remote" | "Hybrid" | null,
                "duration": "string" | null,
                "location": "string" | null,
                "requiredSkills": ["string"],
                "applyLink": "string" | null,
                "summary": "string"
                }}
            ]
            }}

            Rules:
            - If no real job or internship is present, return isJobVideo=false and an empty openings array.
            - Summary must be concise (max 60–80 words per opening).
            - Do not hallucinate missing information; use null if unclear.
            """
            
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(GEMINI_MODEL)

        response = model.generate_content(prompt)
        
        return json.loads(response.text)

        