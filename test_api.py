import requests
import time
from typing import Dict, Any
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test an API endpoint and return the response."""
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            return {
                "status": "success",
                "data": response.json(),
                "response_time": round(response_time, 3)
            }
        else:
            return {
                "status": "error",
                "error": response.text,
                "status_code": response.status_code,
                "response_time": round(response_time, 3)
            }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "response_time": round(time.time() - start_time, 3)
        }

def print_test_result(test_name: str, result: Dict[str, Any]):
    """Print test results in a formatted way."""
    print(f"\nTest: {test_name}")
    print("-" * 50)
    if result["status"] == "success":
        print(f"Status: ✅ Success")
        print(f"Response Time: {result['response_time']} seconds")
        print("\nResponse Data:")
        print(json.dumps(result["data"], indent=2))
    else:
        print(f"Status: ❌ Error")
        print(f"Error: {result['error']}")
        if "status_code" in result:
            print(f"Status Code: {result['status_code']}")
        print(f"Response Time: {result['response_time']} seconds")
    print("-" * 50)

def main():
    print("Testing Moustache Escapes Property Finder API")
    print("=" * 50)
    
    # Test root endpoint
    print_test_result("Root Endpoint", test_endpoint(""))
    
    # Test cases with actual Moustache Escapes locations
    test_cases = [
        # Cities with multiple properties
        "Udaipur",  # Should show both Udaipur properties
        "Rishikesh",  # Should show both Rishikesh properties
        
        # Cities near other properties
        "Sissu",  # Should show Koksar property
        "Manali",  # Should show nearby properties
        
        # Major tourist destinations
        "Jaipur",
        "Agra",
        "Goa",
        
        # Spelling mistakes
        "delih",  # Should correct to Delhi
        "bangalre",  # Should correct to Bangalore
        
        # Remote location test
        "Leh"  # Should show no properties
    ]
    
    for location in test_cases:
        print_test_result(f"Search Properties Near {location}", 
                         test_endpoint("search", {"location": location}))

if __name__ == "__main__":
    main() 