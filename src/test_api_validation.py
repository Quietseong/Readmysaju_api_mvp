import requests
import json
from typing import Dict, Any

# API 서버의 기본 URL
BASE_URL = "http://localhost:8001"

# data/system_prompt.json 에서 가져온 값
OUT_OF_SCOPE_RESPONSE = "I\'m sorry, I cannot assist with that request. I am specialized in Saju and fortune telling only."

def print_test_result(test_name: str, success: bool, details: str = "") -> None:
    """테스트 결과를 출력합니다."""
    status = "✅ 통과" if success else "❌ 실패"
    print(f"{status} - {test_name}")
    if details:
        print(f"   detalles: {details}")

def validate_response_structure(response_json: Dict[str, Any], expected_keys: list[str]) -> bool:
    """응답 JSON 구조를 검증합니다."""
    if not isinstance(response_json, dict):
        return False
    return all(key in response_json for key in expected_keys)

def test_get_tones() -> None:
    """/tones 엔드포인트를 테스트하고 응답을 검증합니다."""
    test_name = "/tones 엔드포인트 테스트"
    try:
        response = requests.get(f"{BASE_URL}/tones", timeout=10)
        if response.status_code == 200:
            data = response.json()
            # 응답이 딕셔너리 형태이고, 최소한 하나의 키(톤)가 있는지 확인
            if isinstance(data, dict) and len(data) > 0:
                # 각 톤이 예상된 구조를 가졌는지 확인 (예: 첫 번째 톤만 샘플로 확인)
                first_tone_key = list(data.keys())[0]
                if validate_response_structure(data[first_tone_key], ["name", "description", "characteristics", "example"]):
                    print_test_result(test_name, True)
                    return
            print_test_result(test_name, False, f"응답 데이터 구조가 예상과 다릅니다: {data}")
        else:
            print_test_result(test_name, False, f"잘못된 상태 코드: {response.status_code}, 응답: {response.text}")
    except requests.RequestException as e:
        print_test_result(test_name, False, f"요청 중 에러 발생: {e}")

def test_chat_endpoint_valid_saju_query() -> None:
    """/chat 엔드포인트에 유효한 사주 관련 질문을 테스트하고 응답을 검증합니다."""
    test_name = "/chat 유효한 사주 질문 테스트"
    payload = {
        "message": "내 생일은 1990년 5월 15일이야. 내 연애운은 어때?",
        "tone": "mystical_oracle"
    }
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=20) # LLM 응답 시간 고려
        if response.status_code == 200:
            data = response.json()
            if validate_response_structure(data, ["response", "tone"]):
                if data["tone"] == payload["tone"] and isinstance(data["response"], str) and data["response"] != OUT_OF_SCOPE_RESPONSE:
                    print_test_result(test_name, True, f"응답: {data['response'][:50]}...")
                    return
            print_test_result(test_name, False, f"응답 데이터 구조 또는 내용이 예상과 다릅니다: {data}")
        else:
            print_test_result(test_name, False, f"잘못된 상태 코드: {response.status_code}, 응답: {response.text}")
    except requests.RequestException as e:
        print_test_result(test_name, False, f"요청 중 에러 발생: {e}")

def test_chat_endpoint_out_of_scope_query() -> None:
    """/chat 엔드포인트에 사주와 관련 없는 질문을 테스트하고 범위 벗어남 응답을 검증합니다."""
    test_name = "/chat 범위 벗어난 질문 테스트"
    payload = {
        "message": "오늘 날씨 어때?",
        "tone": "wise_mentor"
    }
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=20)
        if response.status_code == 200: # 범위 벗어난 응답도 200 OK 로 처리될 수 있음 (API 설계에 따라 다름)
            data = response.json()
            if validate_response_structure(data, ["response", "tone"]):
                # API 설계상 out_of_scope_response는 ChatResponse의 response 필드로 반환됩니다.
                if data["response"].strip() == OUT_OF_SCOPE_RESPONSE:
                    print_test_result(test_name, True, f"정상적으로 범위 벗어남 응답 수신: {data['response']}")
                    return
            print_test_result(test_name, False, f"범위 벗어남 응답이 예상과 다릅니다: {data}")
        else:
            print_test_result(test_name, False, f"잘못된 상태 코드: {response.status_code}, 응답: {response.text}")
    except requests.RequestException as e:
        print_test_result(test_name, False, f"요청 중 에러 발생: {e}")

def test_chat_endpoint_invalid_tone() -> None:
    """/chat 엔드포인트에 유효하지 않은 톤으로 요청 시 에러를 검증합니다."""
    test_name = "/chat 유효하지 않은 톤 테스트"
    payload = {
        "message": "내 생일은 1985년 10월 1일이야.",
        "tone": "non_existent_tone"
    }
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
        # Chat.py의 change_tone 메서드에서 ValueError를 발생시키고,
        # api.py의 chat_endpoint에서 이를 HTTPException 500으로 변환합니다.
        if response.status_code == 500:
            data = response.json()
            if "detail" in data and "Invalid tone key: non_existent_tone" in data["detail"]:
                print_test_result(test_name, True, "정상적으로 500 에러 및 상세 메시지 수신")
                return
            print_test_result(test_name, False, f"500 에러 상세 메시지가 예상과 다릅니다: {data.get('detail')}")
        else:
            print_test_result(test_name, False, f"예상치 못한 상태 코드: {response.status_code}, 올바른 에러 처리가 필요합니다.")
    except requests.RequestException as e:
        print_test_result(test_name, False, f"요청 중 에러 발생: {e}")


if __name__ == "__main__":
    print("API 테스트를 시작합니다...")
    print(f"대상 서버: {BASE_URL}")
    
    # 서버가 실행될 시간을 약간 줍니다.
    # import time
    # time.sleep(1)

    test_get_tones()
    test_chat_endpoint_valid_saju_query()
    test_chat_endpoint_out_of_scope_query()
    test_chat_endpoint_invalid_tone()

    print("\nAPI 테스트 완료.") 