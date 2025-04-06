# Moustache Escapes Property Finder

A FastAPI-based backend service that helps tele-calling agents find Moustache Escapes properties within a 50km radius of any given location in India.

## Features

- 🔍 Search properties by location name
- 📍 Find properties within 50km radius
- ✨ Handles spelling mistakes in location names
- ⚡ Fast response times (< 2 seconds)
- 🗺️ Accurate distance calculations
- 🏨 Real property data from Moustache Escapes

## Tech Stack

- Python 3.8+
- FastAPI
- Geopy
- RapidFuzz
- CacheTools
- Uvicorn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/InvertedPallete/formi_assignment_2.git
cd formi_assignment_2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

### Root Endpoint

```
GET /
```
Health check endpoint to verify the API is running.

### Search Properties

```
GET /search?location={location_name}
```

Parameters:
- `location`: Name of the location to search near (city, state, or area name)

Example Response:
```json
{
  "properties": [
    {
      "id": 1,
      "name": "Moustache Udaipur Luxuria",
      "location": "Udaipur, Rajasthan",
      "distance": 1.1,
      "available": true
    }
  ],
  "search_time": 0.748,
  "location": "Udaipur",
  "coordinates": [24.578721, 73.6862571]
}
```

## Testing

Run the test suite:
```bash
python test_api.py
```

The test suite includes:
- Location searches
- Spelling mistake handling
- Edge cases
- Performance testing

## Project Structure

```
formi_assignment_2/
├── main.py           # FastAPI application and core logic
├── test_api.py       # Test suite
├── requirements.txt  # Dependencies
├── README.md        # This documentation
└── SUBMISSION.md    # Submission details and answers
```

## License

MIT 