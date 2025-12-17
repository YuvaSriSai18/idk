from fastapi import FastAPI,Request,Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse,JSONResponse
import json
import google.generativeai as genai

from Repository.Youtube import Youtube
from Repository.Firebase import Firebase

YoutubeObj = Youtube()
FirebaseObj = Firebase()



