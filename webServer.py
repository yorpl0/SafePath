from flask import Flask, request, jsonify

app = Flask(__name__)

sos = False

@app.route('/check', methods=['POST'])
def check_location():

    data = request.json
    latitude = data.get('lat')
    longitude = data.get('long')

    CCTV_id = -1
    if CCTV_id == -1:
        return jsonify({"error": "No CCTV data available"}), 404
    response = {
        "CCTV" : str(CCTV_id),
    }

    return jsonify(response), 200

@app.route('/upd', methods=['POST'])
def upd():
    global sos
    data = request.json
    danger = data.get('sos') # Request : { "sos" : int (0/1) }
    sos = (int(danger))
    if sos:
        print("SOS")
    return jsonify({"status": "success"}), 200


@app.route('/getsos', methods=['GET'])
def getsos():
    global sos
    return str(sos), 200

if __name__ == '__main__':
    app.run(debug=True)
