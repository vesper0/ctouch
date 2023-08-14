"""
    코드의 과정입니다.
    1. 초음파 센서 변화로 서랍 열리는 것 감지, 몇 층인지 판단한 이후 실시간 스트리밍 시작
    2. 초음파 센서 변화로 서랍 닫히는 것 감지, 실시간 스트리밍 종료 및 촬영
    3. 촬영한 사진을 Rekognition 처리
        3-1. 물체 인식
        3-2. 물체의 이름을 한글로 번역
        3-3. 물체가 왼쪽에 있는지 오른쪽에 있는지 판단 
    4. 3의 결과물을 (이름,위치) 형식으로 xf.txt 파일로 저장
"""

"""아마존에서 제공하는 Rekognition과 Translation을 사용하기 위한 boto3"""
import boto3
from googletrans import Translator

translator = Translator()
rekognition_client = boto3.client("rekognition")
translate_client = boto3.client("translate")

"""영상처리를 위한 cv2"""
import cv2


blacklisted_labels = [
    "Furniture",
    "Man",
    "Adult",
    "Male",
    "Person",
    "Electronics",
    "Hardware",
    "Desk",
    "White Board",
]  # 결과에 나오면 안 되는 라벨 모음


def process_labels(image_data):
    """3-1, 3-2를 수행하는 함수입니다."""
    response = rekognition_client.detect_labels(
        Image={"Bytes": image_data}, MaxLabels=10, MinConfidence=70.0
    )
    label_locations = {}

    for label in response["Labels"]:
        label_name = label["Name"]
        instances = label.get("Instances", [])

        if label_name in blacklisted_labels:
            continue

        response = translate_client.translate_text(
            Text=label_name, SourceLanguageCode="en", TargetLanguageCode="ko"
        )

        label_name = response['TranslatedText']

        for instance in instances:
            bounding_box = instance.get("BoundingBox", {})
            if bounding_box:
                location = get_box_location(bounding_box)

                if location not in label_locations:
                    label_locations[location] = []
                label_locations[location].append(label_name)

                print(f"{label_name} - {location}")

    return label_locations


def get_box_location(bounding_box):
    """3-3을 수행하는 함수입니다."""
    left_boundary = 0.5
    box_center_x = bounding_box["Left"] + bounding_box["Width"] / 2

    if box_center_x < left_boundary:
        return "왼쪽"
    else:
        return "오른쪽"


def save_as_text(label_locations, floor_info):
    """4를 수행하는 함수입니다."""
    with open(f"{floor_info}f.txt", "w") as txt_file:
        for location, names in label_locations.items():
            for name in names:
                txt_file.write(f"{name},{location}\n")


def main():
    """1과 2를 수행하는 메인 함수입니다."""
    floor_info = 1  # 초음파 센서로 제어할 수 있게 바꿔야 합니다 -> 1층이 열리면 1 2층이 열리면 2

    camera = cv2.VideoCapture(0)
    while True:  # 여기도 마찬가지로 초음파 센서 연동으로 제어
        _, frame = camera.read()
        cv2.imshow("Result", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            return 0
        elif key == ord("1"):
            floor_info = 1
        elif key == ord("2"):
            floor_info = 2
        elif key == ord("s"):
            cv2.imwrite("sample.jpg", frame)
            break

    image_path = "sample.jpg"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    label_locations = process_labels(image_data)

    save_as_text(label_locations, floor_info)


if __name__ == "__main__":
    main()
