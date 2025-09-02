from flask import Flask, render_template, request, send_file, jsonify
import flight_analysis as fa
import os

app = Flask(__name__)

# ---------------- DASHBOARD ----------------
@app.route("/")
def home():
    airlines = sorted(fa.data["Airline"].unique())
    airports = sorted(fa.data["OriginAirport"].unique())
    return render_template("index.html", airlines=airlines, airports=airports)

# ---------------- TABLE VIEWS ----------------
@app.route("/flights/delayed/table")
def delayed_table():
    df = fa.delayed_flights()
    return render_template("table.html", title="Delayed Flights (>30 min)", columns=df.columns, data=df.to_dict(orient="records"))

@app.route("/flights/from_airport", methods=["POST"])
def flights_from_airport():
    airport = request.form.get("airport")
    df = fa.flights_from_airport(airport)
    return render_template("table.html", title=f"Flights from {airport}", columns=df.columns, data=df.to_dict(orient="records"))

@app.route("/flights/by_airline", methods=["POST"])
def flights_by_airline():
    airline = request.form.get("airline")
    df = fa.flights_by_airline(airline)
    return render_template("table.html", title=f"Flights by {airline}", columns=df.columns, data=df.to_dict(orient="records"))

# ---------------- SUMMARIES (HTML TABLES) ----------------
@app.route("/summary/airline/table")
def airline_summary_table():
    df = fa.airline_summary()
    return render_template("table.html", title="Airline Summary", columns=df.columns, data=df.to_dict(orient="records"))

@app.route("/summary/airport/table")
def airport_summary_table():
    df = fa.airport_summary()
    return render_template("table.html", title="Airport Summary", columns=df.columns, data=df.to_dict(orient="records"))

@app.route("/summary/route/table")
def route_summary_table():
    df = fa.route_summary()
    return render_template("table.html", title="Top 5 Delayed Routes", columns=df.columns, data=df.to_dict(orient="records"))

@app.route("/summary/date/table")
def date_summary_table():
    df = fa.date_summary()
    return render_template("table.html", title="Daily Summary", columns=df.columns, data=df.to_dict(orient="records"))

# ---------------- SUMMARIES (JSON API for ThunderClient) ----------------
@app.route("/summary/airline/json")
def airline_summary_json():
    df = fa.airline_summary()
    return jsonify(df.to_dict(orient="records"))

@app.route("/summary/airport/json")
def airport_summary_json():
    df = fa.airport_summary()
    return jsonify(df.to_dict(orient="records"))

@app.route("/summary/route/json")
def route_summary_json():
    df = fa.route_summary()
    return jsonify(df.to_dict(orient="records"))

@app.route("/summary/date/json")
def date_summary_json():
    df = fa.date_summary()
    return jsonify(df.to_dict(orient="records"))

# ---------------- EXPORTS (CSV) ----------------
@app.route("/export/airline_summary")
def export_airline_summary():
    df = fa.airline_summary()
    os.makedirs("exports", exist_ok=True)
    path = "exports/airline_summary.csv"
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True)
@app.route("/export/airport_summary")
def export_airport_summary():
    df = fa.airport_summary()
    os.makedirs("exports", exist_ok=True)
    path = "exports/airport_summary.csv"
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True)
@app.route("/export/route_summary")
def export_route_summary():
    df = fa.route_summary()
    os.makedirs("exports", exist_ok=True)
    path = "exports/route_summary.csv"
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True)
@app.route("/export/date_summary")
def export_date_summary():
    df = fa.date_summary()
    os.makedirs("exports", exist_ok=True)
    path = "exports/date_summary.csv"
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
