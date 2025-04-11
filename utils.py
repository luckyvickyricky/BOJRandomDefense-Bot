import random
import requests


def choose_random_tier(search_tier: str) -> str:
    """
    티어 문자열이 범위 형식(b3~b5)이라면, 해당 범위 내에서 무작위 티어 선택 후 반환합니다.
    단일 티어 입력(예: "b" 또는 "s2")의 경우 그대로 반환합니다.
    """
    if "~" in search_tier:
        parts = search_tier.split("~")
        prefix = parts[0][0]  # 예: 'b' 또는 's'
        start_tier = int(parts[0][1:])
        # 두 번째 부분이 티어 접두어를 포함할 수도, 숫자만 있을 수도 있음.
        if parts[1][0].isalpha():
            end_tier = int(parts[1][1:])
        else:
            end_tier = int(parts[1])
        return f"{prefix}{random.randint(start_tier, end_tier)}"
    else:
        return search_tier


def search_random_problems(query: str) -> list:
    """
    solved.ac API를 사용하여 랜덤 문제를 검색합니다.

    쿼리 예시: "*b2 s#10000.. !@user1 !@user2"
    반환값: 문제 정보(dict) 리스트
    """
    api_url = "https://solved.ac/api/v3/search/problem"
    params = {"query": query, "direction": "asc", "page": 1, "sort": "random"}
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise Exception("랜덤 문제 검색에 실패했습니다.")

    data = response.json()
    items = data.get("items", [])
    return items
