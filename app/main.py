import random
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Endpoint for the home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to generate artistic inspiration
@app.post("/inspiration", response_class=HTMLResponse)
async def get_inspiration(request: Request, keyword: str = Form(...)):
    if not keyword.strip():
        return templates.TemplateResponse("index.html", {"request": request, "error": "Please enter a valid art style or keyword."})
    
    # Initialize artwork and quote data containers
    artwork_data = {}
    quote_data = {}

    # Fetch artworks from the Metropolitan Museum of Art API
    try:
        search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={keyword}&hasImages=true"
        search_response = requests.get(search_url, timeout=5)
        search_response.raise_for_status()
        search_results = search_response.json()
        object_ids = search_results.get("objectIDs", [])
        if not object_ids:
            artwork_data = {"error": "No artworks found for the given keyword."}
        else:
            # Choose a random artwork ID
            random_id = random.choice(object_ids)
            object_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{random_id}"
            object_response = requests.get(object_url, timeout=5)
            object_response.raise_for_status()
            artwork_data = object_response.json()
    except Exception as e:
        artwork_data = {"error": "Error retrieving artwork information."}

    # Fetch a random inspirational quote from the Quotable API
    try:
        quote_url = "https://api.quotable.io/random"
        quote_response = requests.get(quote_url, timeout=5)
        quote_response.raise_for_status()
        quote_data = quote_response.json()
    except Exception as e:
        quote_data = {"error": "Error retrieving inspirational quote."}

    return templates.TemplateResponse(
        "inspiration.html",
        {
            "request": request,
            "keyword": keyword,
            "artwork": artwork_data,
            "quote": quote_data,
        },
    )
