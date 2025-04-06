from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import List, Optional
import time
from rapidfuzz import fuzz
from cachetools import TTLCache
import uvicorn

app = FastAPI(
    title="Moustache Escapes Property Finder",
    description="API to find Moustache Escapes properties within 50km of a given location",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for geocoding results (24-hour TTL)
geocode_cache = TTLCache(maxsize=1000, ttl=86400)

# Initialize geocoder
geolocator = Nominatim(user_agent="moustache_escapes")

# Actual Moustache Escapes property data
PROPERTIES = [
    {"id": 1, "name": "Moustache Udaipur Luxuria", "location": "Udaipur, Rajasthan", "coordinates": (24.5883, 73.6833), "available": True},
    {"id": 2, "name": "Moustache Jaipur", "location": "Jaipur, Rajasthan", "coordinates": (26.9124, 75.7873), "available": True},
    {"id": 3, "name": "Moustache Jaisalmer", "location": "Jaisalmer, Rajasthan", "coordinates": (26.9157, 70.9083), "available": True},
    {"id": 4, "name": "Moustache Udaipur", "location": "Udaipur, Rajasthan", "coordinates": (24.5883, 73.6833), "available": True},
    {"id": 5, "name": "Moustache Rishikesh", "location": "Rishikesh, Uttarakhand", "coordinates": (30.0869, 78.2676), "available": True},
    {"id": 6, "name": "Moustache Rishikesh Luxuria", "location": "Rishikesh, Uttarakhand", "coordinates": (30.0869, 78.2676), "available": True},
    {"id": 7, "name": "Moustache Sissu", "location": "Sissu, Himachal Pradesh", "coordinates": (32.4757, 77.1234), "available": True},
    {"id": 8, "name": "Moustache Koksar", "location": "Koksar, Himachal Pradesh", "coordinates": (32.4757, 77.1234), "available": True},
    {"id": 9, "name": "Moustache Shoja", "location": "Shoja, Himachal Pradesh", "coordinates": (31.8124, 77.2345), "available": True},
    {"id": 10, "name": "Moustache Manali", "location": "Manali, Himachal Pradesh", "coordinates": (32.2432, 77.1892), "available": True},
    {"id": 11, "name": "Moustache Kasol", "location": "Kasol, Himachal Pradesh", "coordinates": (32.0123, 77.3456), "available": True},
    {"id": 12, "name": "Moustache Tosh", "location": "Tosh, Himachal Pradesh", "coordinates": (32.2345, 77.4567), "available": True},
    {"id": 13, "name": "Moustache Bir", "location": "Bir, Himachal Pradesh", "coordinates": (32.0456, 76.6789), "available": True},
    {"id": 14, "name": "Moustache Dharamshala", "location": "Dharamshala, Himachal Pradesh", "coordinates": (32.2190, 76.3234), "available": True},
    {"id": 15, "name": "Moustache McLeodganj", "location": "McLeodganj, Himachal Pradesh", "coordinates": (32.2456, 76.3456), "available": True},
    {"id": 16, "name": "Moustache Dalhousie", "location": "Dalhousie, Himachal Pradesh", "coordinates": (32.5345, 75.9456), "available": True},
    {"id": 17, "name": "Moustache Agra", "location": "Agra, Uttar Pradesh", "coordinates": (27.1767, 78.0081), "available": True},
    {"id": 18, "name": "Moustache Varanasi", "location": "Varanasi, Uttar Pradesh", "coordinates": (25.3176, 82.9739), "available": True},
    {"id": 19, "name": "Moustache Goa", "location": "Goa", "coordinates": (15.4989, 73.8278), "available": True},
    {"id": 20, "name": "Moustache Hampi", "location": "Hampi, Karnataka", "coordinates": (15.3350, 76.4600), "available": True},
    {"id": 21, "name": "Moustache Gokarna", "location": "Gokarna, Karnataka", "coordinates": (14.5500, 74.3167), "available": True},
    {"id": 22, "name": "Moustache Bangalore", "location": "Bangalore, Karnataka", "coordinates": (12.9716, 77.5946), "available": True},
    {"id": 23, "name": "Moustache Delhi", "location": "Delhi", "coordinates": (28.6139, 77.2090), "available": True}
]

# List of known locations for fuzzy matching
KNOWN_LOCATIONS = [prop["location"].split(",")[0].strip() for prop in PROPERTIES]

class Property(BaseModel):
    id: int
    name: str
    location: str
    distance: float
    available: bool

class SearchResponse(BaseModel):
    properties: List[Property]
    search_time: float
    location: str
    coordinates: tuple

def get_coordinates(location: str) -> tuple:
    """Get coordinates for a location using geocoding with caching."""
    # Check cache first
    if location in geocode_cache:
        return geocode_cache[location]
    
    try:
        # Add "India" to improve geocoding accuracy
        location_with_country = f"{location}, India"
        location_data = geolocator.geocode(location_with_country)
        
        if not location_data:
            raise ValueError(f"Location not found: {location}")
        
        coordinates = (location_data.latitude, location_data.longitude)
        geocode_cache[location] = coordinates
        return coordinates
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def find_nearest_properties(location: str, max_distance: float = 50) -> List[Property]:
    """Find properties within max_distance km of the given location."""
    try:
        # Get coordinates for the search location
        search_coords = get_coordinates(location)
        
        # Calculate distances and filter properties
        nearby_properties = []
        for prop in PROPERTIES:
            distance = geodesic(search_coords, prop["coordinates"]).kilometers
            if distance <= max_distance:
                nearby_properties.append(Property(
                    id=prop["id"],
                    name=prop["name"],
                    location=prop["location"],
                    distance=round(distance, 2),
                    available=prop["available"]
                ))
        
        # Sort by distance
        return sorted(nearby_properties, key=lambda x: x.distance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def correct_spelling(location: str) -> str:
    """Correct spelling mistakes in location names."""
    if not location:
        return location
        
    # Convert to lowercase for comparison
    location_lower = location.lower()
    best_match = None
    best_ratio = 0
    
    # Try exact match first
    for known_loc in KNOWN_LOCATIONS:
        if location_lower == known_loc.lower():
            return known_loc
    
    # If no exact match, try fuzzy matching
    for known_loc in KNOWN_LOCATIONS:
        ratio = fuzz.ratio(location_lower, known_loc.lower())
        if ratio > best_ratio and ratio > 75:  # Lowered threshold for better matching
            best_ratio = ratio
            best_match = known_loc
    
    return best_match if best_match else location

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Moustache Escapes Property Finder API is running"}

@app.get("/search")
async def search_properties(location: str) -> SearchResponse:
    """
    Search for properties near a given location.
    
    Args:
        location: Name of the location to search near
        
    Returns:
        List of properties within 50km of the location
    """
    start_time = time.time()
    
    try:
        # Correct spelling if needed
        corrected_location = correct_spelling(location)
        if corrected_location != location:
            location = corrected_location
        
        # Get coordinates for the search location
        search_coords = get_coordinates(location)
        
        # Find nearby properties
        properties = find_nearest_properties(location)
        
        search_time = time.time() - start_time
        
        return SearchResponse(
            properties=properties,
            search_time=round(search_time, 3),
            location=location,
            coordinates=search_coords
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=["."]) 