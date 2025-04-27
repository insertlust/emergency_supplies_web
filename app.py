from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    fail_step = None

    if request.method == "POST":
        try:
            # Inclusion Criteria
            inclusion1 = request.form.get("inclusion1") == "yes"
            inclusion2 = request.form.get("inclusion2") == "yes"

            if not (inclusion1 and inclusion2):
                result = "fail"
                fail_step = "Inclusion Criteria Not Met"

            # Exclusion Criteria
            exclusions = [
                request.form.get(f"exclusion{i}") == "yes"
                for i in range(1, 10)
            ]
            if any(exclusions):
                result = "fail"
                fail_step = "Exclusion Criteria Triggered"

            # Respiratory Score Check
            rs_score = request.form.get("rs_score") == "yes"
            if result is None and not rs_score:
                result = "fail"
                fail_step = "Respiratory Score Outside Range"

            # Pre-Transfer Conditions
            stable_obs = request.form.get("stable_obs") == "yes"
            icu_consult = request.form.get("icu_consult") == "yes"
            if result is None and not (stable_obs and icu_consult):
                result = "fail"
                fail_step = "Pre-Transfer Conditions Not Met"

            # Passed all checks
            if result is None:
                result = "pass"

        except Exception as e:
            print("Error processing form:", e)
            result = "fail"
            fail_step = "Form Submission Error"

    return render_template("home.html", result=result, fail_step=fail_step)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
