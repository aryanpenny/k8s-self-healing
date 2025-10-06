from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def alert():
    """Receives alerts from Alertmanager and executes remediation actions."""
    payload = request.get_json()
    alerts = payload.get("alerts", [])
    
    for al in alerts:
        alertname = al.get("labels", {}).get("alertname")
        target = al.get("labels", {}).get("remediation_target") # deployment/demo-app
        status = al.get("status") 
        
        # ACT ONLY on FIRING alerts for the specified target
        if status == "firing" and alertname in ("PodRestartsHigh", "DeploymentUnavailable") and target:
            print(f"ALERT FIRED: {alertname} on {target}. Initiating auto-heal.")
            
            try:
                # Remediation Action: kubectl rollout restart
                subprocess.run(
                    ["kubectl", "rollout", "restart", target, "-n", "default"], 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                print(f"Successfully executed rollout restart for {target}.")
            except subprocess.CalledProcessError as e:
                # Log the failure, but prevent crashing the webhook itself
                print(f"Error during kubectl rollout restart: {e.stderr}")
                return jsonify({"status": "remediation_failed"}), 500
                
    return jsonify({"status": "ok", "message": "Remediation checked/executed"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
