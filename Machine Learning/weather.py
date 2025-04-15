    # importing the libraries
import requests
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# extratcion of API keys
API_KEY = 'df53afdf30de4858cc6365563c7d4c7e'

# Function to get weather data of a city
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        print("Could not get weather data.")
        return None
    data = response.json()
    weather = {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "desc": data["weather"][0]["description"]
    }
    return weather

# Load dataset and part of pre-processign...
def load_data():
    try:
        df = pd.read_csv("weather_data.csv")
        df = df[["MinTemp", "MaxTemp", "Humidity9am", "Humidity3pm", "WindSpeed9am", "WindSpeed3pm"]].dropna()

        df["temp"] = (df["MinTemp"] + df["MaxTemp"]) / 2
        df["humidity"] = (df["Humidity9am"] + df["Humidity3pm"]) / 2
        df["wind"] = (df["WindSpeed9am"] + df["WindSpeed3pm"]) / 2

        def label_weather(t):
            if t <= 15:
                return "cold"
            elif t <= 25:
                return "mild"
            else:
                return "hot"

        df["label"] = df["temp"].apply(label_weather)
        return df[["temp", "humidity", "wind", "label"]]
    except:
        print("Error")
        return pd.DataFrame()

# Training by Algorithm(decision tree classifire) 
def train_model(data):
    X = data[["temp", "humidity", "wind"]]
    y = data["label"]
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

# the options
def main():
    print("Choose option:")
    print("1. Use city name for live weather")
    print("2. Enter values manually")
    choice = input("Enter 1 or 2: ")

    data = load_data()
    if data.empty:
        return
    model = train_model(data)

    if choice == "1":
        city = input("Enter city name: ")
        weather = get_weather(city)
        if weather:
            input_data = pd.DataFrame([{
                "temp": weather["temp"],
                "humidity": weather["humidity"],
                "wind": weather["wind"]
            }])
            prediction = model.predict(input_data)
            print(f"\nWeather in {city}: {weather['desc']}")
            print(f"\nTemperature: {weather['temp']}°C")
            print(f"\nHumidity: {weather['humidity']}%")
            print(f"\nWind Speed: {weather['wind']} m/s")
            print(f"\nPrediction: It's a {prediction[0]} day.")
    elif choice == "2":
        try:
            t = float(input("Enter temperature (°C): "))
            h = float(input("Enter humidity (%): "))
            w = float(input("Enter wind speed (m/s): "))
            input_data = pd.DataFrame([{
                "temp": t,
                "humidity": h,
                "wind": w
            }])
            prediction = model.predict(input_data)
            print(f"\nPrediction: It's a {prediction[0]} day.")
        except:
            print("Invalid input.")
    else:
        print("Invalid choice.")

# Run the app
if __name__ == "__main__":
    main()
