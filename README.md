# 편한손길 스마트 서랍장

* 노인이나 디지털 기기를 과도하게 사용하는 현대인 등, 기억력 저하를 겪는 사람들에게 도움이 되는 보조기기를 목표하였습니다.
* 보조기기를 사용하고 있다는 부담감과 거부감을 줄이기 위해, 일상생활에 녹아들 수 있는 형태로 제작하였습니다.
* 제4회 국립재활원 보조기기 해커톤 출품작입니다.

## Mechanism

* 작동 과정입니다.

```shell
1. 서랍장 뒤에 위치한 초음파 센서로 서랍의 개폐 여부를 확인합니다.
2. 서랍이 열려 초음파 센서 값이 임계값을 넘어갔을 때, 카메라가 작동 대기 상태가 됩니다.
3. 서랍이 닫혀 초음파 센서 값이 일정 시간 안에 임계값 아래로 내려갔을 때, 카메라가 서랍 내부를 촬영합니다.
4. 촬영한 사진을 바탕으로 물건의 위치를 인식합니다. (왼쪽, 오른쪽)
5. 데이터베이스에 물건, 층, 위치 정보를 저장합니다. (e.g. 펜 1층 오른쪽)
6. 사용자가 NUGU 스피커를 통해 물건의 위치를 요청합니다. "아리아, 서랍장 펜 어디있어?"
여기서 "아리아"는 NUGU 스피커 발화, "서랍장"은 Play 호출, "어디있어?"는 의도 파악, "펜"은 의도의 목표입니다.
7. 스피커가 NUGU Play를 통해 DB에 접근하여 정보를 가져온 뒤 응답합니다. "펜 1층 오른쪽에 있습니다."
8. 서랍 내부에 위치한 LED 또한 빛나며 물건 위치 파악을 돕습니다.
```

## Environment

* 개발 환경입니다.

```
* Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
* 32GB RAM
* Windows 11
* Python 3.9
```

## Output

* 시연 영상입니다.

  [Youtube](https://www.youtube.com/watch?v=_rKvaTeL_Ys)


## Appendix

* 코드와 3D 모델 파일 등 모든 프로젝트 관련 자료는 국립재활원 보조기기 열린플랫폼에서 확인할 수 있습니다.

  [편한손길 스마트 서랍장](http://www.nrc.go.kr/at_rd/web/lay2/program/S1T88C89/openPlatform/deviceInfo/view.do?open_platform_seq=471&start_dt=&end_dt=&keyword=&category1=&category2=&category3=&rows=6&cpage=6&order_type=OPEN_PLATFORM_SEQ)
