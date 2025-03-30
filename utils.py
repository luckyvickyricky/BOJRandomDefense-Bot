import random

import requests


def choose_random_tier(search_tier: str) -> str:
    """
    solved api에서 b3~b5와 같은 범위검색을 지원하지 않습니다.
    b5같은 세부 티어 혹은 b같은 특정 티어 검색을 지원하기 때문에 입력된 티어 문자연에서 랜덤 선택합니다.
    예: "b3~b5" -> "b3", "b4", 또는 "b5" 중 하나를 랜덤 선택.
         단일 티어 입력("b" 또는 "s2")는 그대로 반환합니다.
    """
    if "~" in search_tier:
        parts = search_tier.split("~")
        prefix = parts[0][0]  # 예: 'b' 또는 's'
        start_tier = int(parts[0][1:])
        # 두번째 부분이 티어 접두어를 포함할 수도, 숫자만 있을 수도 있음.
        if parts[1][0].isalpha():
            end_tier = int(parts[1][1:])
        else:
            end_tier = int(parts[1])
        return f"{prefix}{random.randint(start_tier, end_tier)}"
    else:
        return search_tier


def search_random_problems(chosen_tier: str, solved_threshold: str) -> list:
    """
    solved ac API를 사용하여 랜덤 문제를 검색합니다.

    쿼리 형식: "*[티어]+[푼사람수필터]"
    예: "*b2+s#10000.." 는 브론즈2에서 만 명 이상이 푼 문제를 검색합니다.

    return: 문제 번호(int) 리스트
    """
    query = f"*{chosen_tier} s#{solved_threshold}.."
    api_url = "https://solved.ac/api/v3/search/problem"
    params = {"query": query, "direction": "asc", "page": 1, "sort": "random"}
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise Exception("랜덤 문제 검색에 실패했습니다.")

    data = response.json()
    items = data.get("items", [])
    # 문제 번호만 추출
    problem_ids = [item["problemId"] for item in items]
    return problem_ids


def get_all_solved_problems(user_id: str) -> list:
    """
    solved.ac API를 사용하여 특정 유저가 푼 모든 문제를 조회합니다.

    반환: 문제 목록 (각 문제는 dict 형태)
    """
    page = 1
    all_problems = []

    while True:
        url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=level&direction=desc&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"문제 조회 실패 (user_id: {user_id})")
            break

        data = response.json()
        items = data.get("items", [])
        if not items:
            break

        all_problems.extend(items)
        page += 1

    return all_problems


def get_solved_problem_ids(user_ids: list) -> set:
    """
    여러 유저들의 푼 문제 번호들을 집합(set)으로 합쳐 반환합니다
    """
    solved_set = set()
    for user_id in user_ids:
        problems = get_all_solved_problems(user_id)
        for problem in problems:
            solved_set.add(problem["problemId"])
    return solved_set


def filter_unsolved_problems(
    random_problem_ids: list, solved_problem_ids: set, output_count: int
) -> list:
    """
    랜덤으로 검색된 문제 번호 목록에서 이미 푼 문제를 제거하고,
    output_count 만큼의 문제 번호를 반환합니다
    """
    result = []
    for pid in random_problem_ids:
        if pid not in solved_problem_ids:
            result.append(pid)
            if len(result) >= output_count:
                break
    return result
