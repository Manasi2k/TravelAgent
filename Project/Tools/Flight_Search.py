#Import Libraries
import os 
from dotenv import load_dotenv
load_dotenv()
import requests


#Import API Key
API_KEY=os.getenv("AVIATIONSTACK_API_KEY")


#Create Function to search flights
def flight_search(query):
    url="https://api.aviationstack.com/v1/flights"

#Here we called API KEY
    params= {
        "access_key":API_KEY,
        "limit":5
    }

#Here we get the response
        #" it means Go to this website and bring me the response that is 5"
    response=requests.get(url,params=params)
    data=response.json()

    flights=[]
#Used loops to get results
    if "data" in data:
        for flight in data["data"][:5]:
            airline=flight.get("airline",{}).get("name","unknown")
            departure=flight.get("departure",{}).get("airport","unknown")
            arrival=flight.get("arrival",{}).get("airport","unknown")
            status=flight.get("flight_status","unknown")
       

#Here we appended all results and stored in flight list
            flights.append(
                f"""
                Airline:{airline}
                Departure:{departure}
                Arrival:{arrival}
                Status:{status}    
                """
            )
#Here we returned result that is stored in flight list 

    return "\n".join(flights)

 
      
    