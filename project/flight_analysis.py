import pandas as pd
import os

# ---------------- LOAD DATASET ----------------
data = pd.read_csv("data/flights.csv")

# ---------------- FILTERING FUNCTIONS ----------------
def delayed_flights():
    return data[data["DepartureDelay"] > 30]

def flights_from_airport(airport):
    return data[data["OriginAirport"] == airport]

def flights_by_airline(airline):
    return data[data["Airline"] == airline]

# ---------------- SUMMARY FUNCTIONS ----------------
def airline_summary():
    grouped = data.groupby("Airline").agg(
        AverageDepartureDelay=("DepartureDelay", "mean"),
        AverageArrivalDelay=("ArrivalDelay", "mean"),
        TotalFlights=("FlightID", "count")
    ).reset_index()
    grouped["AverageDelay"] = (grouped["AverageDepartureDelay"] + grouped["AverageArrivalDelay"]) / 2
    return grouped[["Airline", "AverageDelay", "TotalFlights"]]

def airport_summary():
    total = data.groupby("OriginAirport")["FlightID"].count().reset_index()
    delayed = data[data["DepartureDelay"] > 30].groupby("OriginAirport")["FlightID"].count().reset_index()
    merged = pd.merge(total, delayed, on="OriginAirport", how="left").fillna(0)
    merged["PercentDelayed"] = (merged["FlightID_y"] / merged["FlightID_x"]) * 100
    return merged.rename(columns={"FlightID_x": "TotalFlights", "FlightID_y": "DelayedFlights"})

def route_summary():
    grouped = data.groupby(["OriginAirport", "DestinationAirport"]).agg(
        AverageDepartureDelay=("DepartureDelay", "mean"),
        AverageArrivalDelay=("ArrivalDelay", "mean"),
        TotalFlights=("FlightID", "count")
    ).reset_index()
    grouped["AverageDelay"] = (grouped["AverageDepartureDelay"] + grouped["AverageArrivalDelay"]) / 2
    top5 = grouped.sort_values(by="AverageDelay", ascending=False).head(5)
    return top5[["OriginAirport", "DestinationAirport", "AverageDelay", "TotalFlights"]]

def date_summary():
    grouped = data.groupby("Date").agg(
        AverageDepartureDelay=("DepartureDelay", "mean"),
        AverageArrivalDelay=("ArrivalDelay", "mean"),
        TotalFlights=("FlightID", "count")
    ).reset_index()
    grouped["AverageDelay"] = (grouped["AverageDepartureDelay"] + grouped["AverageArrivalDelay"]) / 2
    return grouped[["Date", "AverageDelay", "TotalFlights"]]

# ---------------- EXECUTION & CSV EXPORT ----------------
if __name__ == "__main__":
    print("---- Flight Analysis Module Running ----\n")
    print(f"Dataset loaded successfully. Total rows: {len(data)}\n")

    # Create exports folder
    os.makedirs("exports", exist_ok=True)

    # Delayed Flights
    print("Delayed Flights (>30 mins):")
    df_delayed = delayed_flights()
    print(df_delayed.head(), "\n")


    # Airline Summary
    df_airline_summary = airline_summary()
    airline_csv = "exports/airline_summary.csv"
    df_airline_summary.to_csv(airline_csv, index=False)
    print("Airline Summary:")
    print(df_airline_summary.head())
    print(f"Airline summary exported to {airline_csv}\n")

    # Airport Summary
    df_airport_summary = airport_summary()
    airport_csv = "exports/airport_summary.csv"
    df_airport_summary.to_csv(airport_csv, index=False)
    print("Airport Summary:")
    print(df_airport_summary.head())
    print(f"Airport summary exported to {airport_csv}\n")

    # Top 5 Delayed Routes
    df_route_summary = route_summary()
    route_csv = "exports/route_summary.csv"
    df_route_summary.to_csv(route_csv, index=False)
    print("Top 5 Delayed Routes:")
    print(df_route_summary)
    print(f"Route summary exported to {route_csv}\n")

    print("---- End of Flight Analysis ----")
