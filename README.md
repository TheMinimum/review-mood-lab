# Review Mood Lab

영어 영화 리뷰를 VADER 감성 분석 모델로 분석하는 로컬 웹앱입니다. 리뷰를 입력하거나 예시를 불러오면 긍정·부정·중립 판정, compound 점수, 긍정/중립/부정 비율을 보여줍니다. 결과는 사전 학습 모델에 기반한 추정치입니다.

## 사용 환경과 모델

- Python 3.10 이상 권장 (테스트 환경: Python 3.14.5)
- FastAPI + Uvicorn
- VADER `vaderSentiment 3.3.2`
- 일반 노트북 CPU에서 별도 모델 다운로드 없이 실행

## 설치

가상환경 없이 설치하려면 프로젝트 폴더에서 다음을 실행합니다.

```bash
python3 -m pip install -r requirements.txt
```

## 실행

```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

브라우저에서 <http://127.0.0.1:8000>을 엽니다. 종료하려면 실행 중인 터미널에서 `Ctrl+C`를 누릅니다.

## API 사용 예시

상태 확인:

```bash
curl http://127.0.0.1:8000/health
```

리뷰 분석:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"text":"A beautiful and moving movie with brilliant performances."}'
```

`/analyze`의 `text`는 비어 있지 않은 최대 5,000자 문자열이어야 합니다. 형식이 올바르지 않으면 HTTP 422를 반환합니다.

## 향후 모델 개선 및 재배포 계획 (MLOps)

모델 의존 코드는 `model.py`에 분리했습니다. 다음 단계에서는 실제 라벨이 있는 리뷰 데이터를 수집·비식별화하고, 학습/검증/테스트 세트를 고정해 재현 가능한 평가를 진행합니다. VADER와 개선 모델의 정확도, F1, 클래스별 성능 및 편향을 비교하고, 모델 버전·데이터 버전·실험 파라미터를 기록합니다.

검증된 모델은 `model.py`의 동일한 `analyze_sentiment` 인터페이스로 교체하고, `MODEL_VERSION`을 갱신합니다. CI에서 테스트와 API 스모크 테스트를 실행한 뒤, 컨테이너 이미지 또는 고정된 의존성 패키지로 배포하고 `/health`와 오류율·응답 시간·예측 분포를 모니터링합니다. 성능 저하나 데이터 분포 변화가 감지되면 이전 모델로 롤백하고 재학습합니다.
