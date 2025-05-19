from euriai import EuriaiClient
from flask import Flask, render_template, request, redirect, jsonify
import requests
from sklearn.preprocessing import LabelEncoder
import pickle
import joblib
import requests
import openrouteservice
from euriai import EuriaiClient
import folium  # for map generation 
from geopy.geocoders import Nominatim
import re
from datetime import datetime , date
from geopy.exc import GeocoderTimedOut
import random
from flask_cors import CORS  
from euriai import EuriaiClient
import traceback
from bs4 import BeautifulSoup
import re
import geocoder




app = Flask(__name__)

saved_coordinates = []  
g = geocoder.ip('me')

@app.route('/',methods=['GET','POST'])
def home_page():
    return render_template('home_page.html')
            



def latitude_and_longitude_for_traffic_at_paricular_location(jagah):
    geolocator = Nominatim(user_agent="latitude_Contact_me_at_trafficapp.support@example.com")
    new_jagah = geolocator.geocode(jagah)
    if new_jagah: 
        return new_jagah.latitude,new_jagah.longitude            
    else:       
        return None      # yahi hain jo final destination ki latitude aur longitude batayega


@app.route('/traffic_prediction', methods=['GET', 'POST'])
def traffic_prediction(): 
    route_ans=[]
    vehicle_count=None 
    answer=None  
    prediction=None 
    response,data=None,None 
    api_key = 'zoTCtKUznF14iFNir0zAe6lzKkThUQWn' 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    
    if request.method=='POST':
        current_latitude=g.latlng[0]
        current_longitude= g.latlng[1] 
        print(current_latitude,current_longitude) 
        location=request.form['destination']
        date_today=date.today() 
        print(date)  
        time=request.form['time']               
        # weekday= datetime.strptime(str(date),"%Y-%m-%d")
        # weekday=weekday.strftime("%A") 
        api_key = 'AlzaSyTRYk9XaW7YEd_XJoxxPfbJ7kCOoKEw3-V' 
        destination_lat, destination_lon = latitude_and_longitude_for_traffic_at_paricular_location(location)

        url = f"https://maps.gomaps.pro/maps/api/directions/json?origin={current_latitude},{current_longitude}&destination={destination_lat},{destination_lon}&key={api_key}"  

        response = requests.get(url)
        data=response.json()
                
        def clean_html(instruction):
            # Remove HTML tags like <b>, <div>, etc.
            return re.sub(r'<.*?>', '', instruction)

        if data["status"] == "OK":
            route = data["routes"][0]
            leg = route["legs"][0] 
            print("🛣️ Distance:", leg["distance"]["text"])
            print("⏱️ Duration:", leg["duration"]["text"])
            print("\n🔽 Route Steps:\n")

            for i, step in enumerate(leg["steps"], start=1):
                instruction = clean_html(step["html_instructions"])
                distance = step["distance"]["text"]
                duration = step["duration"]["text"]
                answer=f"Step {i}: {instruction} ({distance}, {duration})"
                route_ans.append(answer) 
                print(answer) 
        else:
            route_ans.append("Route not found. ")        
            
                                 
    return render_template('traffic_prediction_page.html',route_ans=route_ans)     



@app.route('/api/map-click', methods=['POST'])
def handle_map_click():
    try:
        if not request.is_json:
            return jsonify({"success": False, "error": "JSON डेटा अपेक्षित"}), 400

        data = request.get_json()
        print("🌍 मैप पर क्लिक की गई जानकारी:", data) 

        if 'latitude' not in data or 'longitude' not in data:
            return jsonify({"success": False, "error": "अमान्य निर्देशांक"}), 400

        lat = float(data['latitude'])
        lng = float(data['longitude'])
        timestamp = data.get('timestamp', datetime.now().isoformat())
        time_str = data.get('time')  # यूज़र का टाइम

        saved_coordinates.append({
            'lat': lat, 
            'lng': lng, 
            'timestamp': timestamp
        })

        try:
            api_key = 'zoTCtKUznF14iFNir0zAe6lzKkThUQWn'
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lng}&key={api_key}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            tomtom_data = response.json()
            flow = tomtom_data.get("flowSegmentData", {})

            current_speed = flow.get("currentSpeed", "N/A")
            free_flow_speed = flow.get("freeFlowSpeed", "N/A")
            constant = 100
            
            if current_speed == 0 or current_speed == "N/A" or free_flow_speed == "N/A":
                vehicle_count = 50
                prediction = "No Info"
            else:

                vehicle_count = (free_flow_speed / current_speed) * constant
                current_time = datetime.now()

                if time_str:
                    hours, minutes = map(int, time_str.split(':'))
                    current_time = current_time.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                    

                time_str = current_time.strftime("%H:%M:%S")
                time_hours = current_time.hour
                time_minutes = current_time.minute
                time_seconds = current_time.second

                current_date = datetime.now()
                weekday = current_date.strftime("%A")
                model = joblib.load('models/grid_knearest.pkl')
                labelenc = joblib.load('models/labelenc.pkl')
                weekday_encoded = labelenc.transform([weekday])

                car_count = int(vehicle_count // 2)
                bike_count = int(vehicle_count // 6)
                bus_count = int(vehicle_count // 6)
                truck_count = int(vehicle_count // 7)

                day_of_month = current_date.day
                input_data = [[
                    day_of_month, 
                    weekday_encoded[0],
                    car_count, 
                    bike_count, 
                    bus_count, 
                    truck_count,
                    vehicle_count,
                    time_hours,
                    time_minutes,
                    time_seconds
                ]]
                print(current_speed,free_flow_speed) 
                print(input_data) 
                answer = model.predict(input_data)[0]

                if answer == 0:
                    prediction = "Heavy"
                elif answer == 1:
                    prediction = "High"
                elif answer == 2:
                    prediction = "Low"
                elif answer == 3:
                    prediction = "Normal"
                else:
                    prediction = "No Info"

            prediction_result = {
                "traffic_density": prediction,
                "vehicle_count": float(vehicle_count)
            }

            print("परिणाम:", prediction_result)

            return jsonify({
                "success": True,
                "message": "Have Patience",
                "prediction": prediction_result,
            
            })

        except Exception as model_error:
            print("🔥 मॉडल त्रुटि:", str(model_error))
            traceback_info = traceback.format_exc()
            return jsonify({
                "success": True,
                "message": "Error",
                "prediction": {
                    "traffic_density": "No Info", 
                    "estimated_travel_time": "No Info",
                    "error_message": str(model_error)
                }
            })

    except Exception as e:
        traceback_info = traceback.format_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "stack_trace": traceback_info
        }), 500


@app.route('/accident_info', methods=['GET', 'POST'])
def traffic_pred():
    response = None
    dest_coords = None
    location = None  # Initialize here to avoid UnboundLocalError

    if request.method == 'POST':
        location = request.form['destination']

        # AI prompt
        prompt = f"""Act as a professional news reporter.
        Task:  
        1. Provide a verified, concise (50 to 60 words) road accident or traffic event update for {location} and its surrounding 25 km radius.  
        - If no such update exists, return exactly:  
            "No recent updates found on {location} or nearby."

        2. If an accident or event is found, also provide the fastest route from Bhauti to {location}, listing only the exact roads and highways to be taken.  
        - If no update is found, do not provide any route or road information.

        Important Instructions:  
        - Do not include any explanations, links, or internal notes.  
        - Only mention roads/highways if an accident or event occurred.  
        - Response should be structured cleanly and consistently for automated use.
        """

        client = EuriaiClient(
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxZWU2NTg0MS1hZDQ0LTQ1YmMtODcxNy1kZDRkNzM2ZTE1YjIiLCJlbWFpbCI6ImFsb2t0cmlwYXRoaTA3MEBnbWFpbC5jb20iLCJpYXQiOjE3NDYwNjM1NDQsImV4cCI6MTc3NzU5OTU0NH0.r17aL4xvJnvhrfGJzalSTjerrh6RG09kkGKd6qe7Rd4",
            model="gpt-4.1-nano"
        )

        result = client.generate_completion(
            prompt=prompt,
            temperature=0.7,
            max_tokens=500
        )

        response = result['choices'][0]['message']['content']
        if response!=f"No recent updates found on {location} or nearby.":
            # yaha se red mark dikhao road par aur jab aur aage ka raod dikhao . bas 
        # Geocode safely
            geo_url = f'https://nominatim.openstreetmap.org/search?format=json&q={location}'
            geo_response = requests.get(geo_url, headers={'User-Agent': 'TrafficApp/1.0'})
            if geo_response.status_code == 200 and geo_response.text.strip():
                geo_data = geo_response.json()
                if geo_data:
                    dest_coords = {
                        'lat': float(geo_data[0]['lat']),
                        'lng': float(geo_data[0]['lon']),
                        'name': location
                    }


    return render_template('accident.html', response=response, dest_coords=dest_coords)


if __name__ == '__main__':
    app.run(debug=True)




























# '''Act as a professional news reporter.

# Task:  
# 1. Provide a verified, concise (50–60 words) road accident or traffic event update for {location} and its surrounding 25 km radius.  
#    - If no such update exists, return exactly:  
#      "No recent updates found on {location} or nearby."

# 2. If an accident or event is found, also provide the fastest route from Bhauti to {location}, listing only the exact roads and highways to be taken.  
#    - If no update is found, do not provide any route or road information.

# Important Instructions:  
# - Do not include any explanations, links, or internal notes.  
# - Only mention roads/highways if an accident or event occurred.  
# - Response should be structured cleanly and consistently for automated use.'''


