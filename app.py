from flask import Flask, render_template, request
from scanner import scan_network, get_client_ip

app = Flask(__name__)
scan_history = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    results = []
    ip_range = ""
    if request.method == "POST":
        ip_range = request.form.get("ip_range")
        if ip_range:
            results = scan_network(ip_range)
            scan_history.insert(0, {"ip": ip_range, "results": results})
            if len(scan_history) > 5:
                scan_history.pop()
    else:
        ip_range = get_client_ip(request)

    return render_template("scan.html", results=results, ip_range=ip_range, history=scan_history[:5])

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)