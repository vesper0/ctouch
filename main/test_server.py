"""
    코드의 과정입니다.
    1. 누구 스피커로부터 호출될 때까지 대기합니다.
    2. 요청이 들어왔을 때 test_camera.py로 저장한 1층과 2층 데이터를 불러옵니다.
    3. 요청에 포함된 물건이 데이터에 존재할 경우 위치를 알려줍니다.
        3-1. 그렇지 않을 경우 다른 곳을 찾도록 안내합니다.
        3-2. 요청에 물건이 포함되어있지 않다면 포함하도록 안내합니다.
"""


"""flask로 NUGU의 request와 response를 송수신합니다."""
from flask import Flask, request, jsonify

app = Flask(__name__)


def drawer_check(filename):
    """2를 수행하는 함수입니다."""
    drawers = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            drawer_object, drawer_location = line.strip().split(",")
            drawers.append((drawer_object, drawer_location))
    return drawers


@app.route("/test.action", methods=["POST"])
def handle_nugu_request():
    """1,3을 수행하는 함수입니다."""
    data = request.json
    action = data["action"]
    # action_name = action["actionName"]
    parameters = action["parameters"]

    if "object" in parameters:
        target = parameters["object"]["value"]

        drawers_first = drawer_check("1f.txt")
        drawers_second = drawer_check("2f.txt")

        response_message = ""

        matching_drawer_1f = next(
            (drawer for drawer in drawers_first if drawer[0] == target), None
        )

        matching_drawer_2f = next(
            (drawer for drawer in drawers_second if drawer[0] == target), None
        )

        if matching_drawer_1f:
            drawer_object, drawer_location = matching_drawer_1f
            response_message = f"{drawer_object} 1층 {drawer_location}에 있습니다."

        if matching_drawer_2f:
            drawer_object, drawer_location = matching_drawer_2f
            if response_message:
                response_message += f" 2층 {drawer_location}에도 있습니다."
            else:
                response_message = f"{drawer_object} 2층 {drawer_location}에 있습니다."

        if response_message == "":
            response_message = "말씀하신 물건이 서랍에 없는 것 같습니다. 다른 곳을 찾아보세요."

        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "result": response_message,
            },
            "directives": [],
        }
    else:
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                "result": "찾고 싶은 물건을 함께 말씀해주세요.",
            },
            "directives": [],
        }

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
