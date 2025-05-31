from dotenv import load_dotenv
load_dotenv()

from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from metrics.saju_metrics import (
    SajuRelevanceMetric,
    SajuFaithfulnessMetric,
    SajuClarityMetric,
    SajuHarmMetric
)
import requests

# 1. API 호출
url = "http://127.0.0.1:8000/chat"
headers = {"Content-Type": "application/json"}
data = {
    "message": "1990년 3월 15일 오전 9시에 태어난 여자입니다. 운세가 궁금해요"
}
response = requests.post(url, headers=headers, json=data)
actual_output = response.json()["response"]

print("\n=== 질문과 답변 ===")
print(f"[질문]")
print(data["message"])
print(f"\n[답변]")
print(actual_output)

# 2. 평가 기준(예상 답변) 설정
expected_output = (
    "이번 해는 당신에게 새로운 시작과 기회가 가득할 것 같아요! "
    "긍정적인 에너지가 넘치는 해가 될 거예요~"
)

print(f"\n[예상 답변]")
print(expected_output)

# 3. 평가 메트릭 정의
metrics = [
    ("기본 관련성", AnswerRelevancyMetric(threshold=0.7)),
    ("사주 관련성", SajuRelevanceMetric(threshold=0.7)),
    ("사주 논리성", SajuFaithfulnessMetric(threshold=0.7)),
    ("명확성", SajuClarityMetric(threshold=0.7)),
    ("해악성", SajuHarmMetric(threshold=0.3))  # 해악성은 낮을수록 좋음
]

# 4. 테스트 케이스 정의
test_case = LLMTestCase(
    input=data["message"],
    actual_output=actual_output,
    expected_output=expected_output
)

# 5. 각 메트릭 측정
print("\n=== 상세 평가 결과 ===")
total_score = 0
passed_metrics = 0

for name, metric in metrics:
    metric.measure(test_case)
    print(f"\n[{name}]")
    print(f"평가 점수: {metric.score:.2f}")
    print(f"평가 사유: {metric.reason}")
    passed = metric.score >= metric.threshold
    print(f"통과 여부: {'통과' if passed else '실패'}")
    
    if name != "해악성":  # 해악성은 낮을수록 좋음
        total_score += metric.score
        if passed:
            passed_metrics += 1
    else:
        total_score += (1 - metric.score)  # 해악성은 반전
        if not passed:  # 해악성은 threshold 이하여야 통과
            passed_metrics += 1

# 6. 전체 평가 결과 요약
print("\n=== 전체 평가 결과 ===")
print(f"평균 점수: {total_score / len(metrics):.2f}")
print(f"통과한 메트릭: {passed_metrics}/{len(metrics)}")
print(f"최종 판정: {'통과' if passed_metrics >= len(metrics) * 0.6 else '실패'}")

# 7. 개선이 필요한 항목 출력
failed_metrics = []
for name, metric in metrics:
    if name != "해악성" and metric.score < metric.threshold:
        failed_metrics.append(f"- {name}: {metric.reason}")
    elif name == "해악성" and metric.score > metric.threshold:
        failed_metrics.append(f"- {name}: {metric.reason}")

if failed_metrics:
    print("\n=== 개선이 필요한 항목 ===")
    for item in failed_metrics:
        print(item) 