
from flask import Blueprint, request, render_template, flash, redirect
from app.fred import func

results_routes = Blueprint("results_routes", __name__)


@results_routes.route("/form/recommendation", methods=['POST'])
def recommendation():
    print("FORM DATA:", dict(request.form))
    request_data = dict(request.form)
    state_id = request_data["state_id"]
    results = func(state_id)
    if results:
        flash("Recommendation Generated Successfully!", "success")
        Median_Price, Recommendation = func(state_id)
        return render_template("results.html", median_price=Median_Price, recommendation=Recommendation, state_id=state_id)
    else:
        flash("Input Error. Please try again!", "danger")
        return render_template("form.html")
