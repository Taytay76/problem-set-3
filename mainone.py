# Python script to create separate shapefiles for each of the three forward positions within the boundary of Sweden using NHL's undocumented statistics API

# Import necessary libraries
import requests
import json
import shapefile

# Define the country and positions
country = "Sweden"
positions = ["C", "RW", "LW"]

# Define the API endpoint for NHL player statistics
api_endpoint = "https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster"

# Send request to the API endpoint
response = requests.get(api_endpoint)

# Load the response data in json format
data = json.loads(response.content)

# Create a list to store player data
player_data = []

# Loop through each team in the response data
for team in data["teams"]:
    # Check if the "country" key is present in the "venue" dictionary for the team
    if "country" in team["venue"] and team["venue"]["country"] == country:
        # Loop through each player in the team roster
        for player in team["roster"]["roster"]:
            # Check if the player is a forward and in one of the defined positions
            if player["position"]["type"] == "Forward" and player["position"]["abbreviation"] in positions:
                # Add the player data to the list
                player_data.append({
                    "player_id": player["person"]["id"],
                    "player_name": player["person"]["fullName"],
                    "position": player["position"]["abbreviation"],
                    "height_inches": player["person"]["height"],
                    "weight_pounds": player["person"]["weight"],
                })

# Create separate shapefiles for each position
for position in positions:
    # Define the shapefile name
    shapefile_name = f"{country}_{position}.shp"

    # Create a new shapefile
    with shapefile.Writer(shapefile_name) as shp:
        # Define the fields for the shapefile
        shp.field("Player_ID", "N")
        shp.field("Player_Name", "C", size=50)
        shp.field("Position", "C", size=2)
        shp.field("Height_cm", "N")
        shp.field("Weight_kg", "N")

        # Loop through each player in the player data list
        for player in player_data:
            # Check if the player is in the current position
            if player["position"] == position:
                # Convert the height and weight to metric units
                height_cm = player["height_inches"] * 2.54
                weight_kg = player["weight_pounds"] * 0.453592

                # Add the player data to the shapefile
                shp.point(0, 0)
                shp.record(player["player_id"], player["player_name"], player["position"], height_cm, weight_kg)

# Print a message indicating the script has completed
print("Shapefile creation complete!")
