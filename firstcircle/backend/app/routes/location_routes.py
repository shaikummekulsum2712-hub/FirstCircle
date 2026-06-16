from fastapi import APIRouter

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("")
def list_locations():
    """
    Returns standard preconfigured coordinates for activities.
    """
    return [
        {
            "name": "Geek Haven Cafe",
            "address": "404 Fictional Ave, Downtown",
            "latitude": 37.7749,
            "longitude": -122.4194
        },
        {
            "name": "Echo Canyon Trailhead Parking",
            "address": "State Route 15, Mountain View",
            "latitude": 37.8044,
            "longitude": -122.2711
        },
        {
            "name": "Central Market Clocktower",
            "address": "800 Market St, Center District",
            "latitude": 37.7891,
            "longitude": -122.4014
        }
    ]
