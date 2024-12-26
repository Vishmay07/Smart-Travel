from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Function to load data from CSV file
def load_attractions():
    attractions = []
    with open('destinations.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            attractions.append({
                'place': row[0],
                'attraction': row[1],
                'distance': row[2],
                'cost': row[3]
            })
    return attractions

# Function to get nearest attractions based on user's input place
def get_nearest_attractions(user_place):
    attractions = load_attractions()
    nearest = []
    for attraction in attractions:
        if user_place.lower() in attraction['place'].lower():
            nearest.append(attraction)
    return nearest

# Function to suggest activities based on solo or family trip
def suggest_trip_type(trip_type):
    if trip_type.lower() == 'solo':
        return "For a solo trip, you might enjoy activities like hiking, solo city tours, and exploring local cafes."
    else:
        return "For a family trip, you might enjoy theme parks, museums, and family-friendly attractions."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_place = request.form['place']
        trip_type = request.form['trip-type']
        days = int(request.form['days'])
        budget = int(request.form['budget'])
        
        # Get nearest attractions based on user's input place
        nearest_attractions = get_nearest_attractions(user_place)
        
        # Suggest activities based on trip type
        trip_suggestion = suggest_trip_type(trip_type)
        
        # Filter attractions based on budget
        budget_friendly_attractions = [attraction for attraction in nearest_attractions if int(attraction['cost']) <= budget]
        
        return render_template("index.html", 
                               user_place=user_place,
                               trip_type=trip_type,
                               days=days,
                               budget=budget,
                               nearest_attractions=nearest_attractions,
                               trip_suggestion=trip_suggestion,
                               budget_friendly_attractions=budget_friendly_attractions)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
