import argparse

import utils


def main():
    parser = argparse.ArgumentParser(description="solved.ac 쿼리 테스트 스크립트")
    parser.add_argument(
        "--search_tier",
        type=str,
        default="b",
        help='검색 티어 (예: "b3~b5" 또는 "s2") (기본값: "b")',
    )
    parser.add_argument(
        "--solved_threshold",
        type=str,
        default="10000",
        help='푼 사람수 기준 (예: "10000") (기본값: "10000")',
    )
    parser.add_argument(
        "--output_count", type=int, default=1, help="출력할 문제 갯수 (기본값: 1)"
    )
    parser.add_argument(
        "--user_ids",
        nargs="+",
        default=["kms39273"],
        help="유저 아이디 목록 (예: user1 user2)",
    )

    args = parser.parse_args()

    print("입력된 파라미터:")
    print(f"  검색 티어: {args.search_tier}")
    print(f"  푼 사람수 기준: {args.solved_threshold}")
    print(f"  출력할 문제 갯수: {args.output_count}")
    print(f"  유저 아이디: {args.user_ids}")

    # 랜덤 티어 선택
    chosen_tier = utils.choose_random_tier(args.search_tier)
    print(f"\n선택된 티어: {chosen_tier}")

    # 쿼리 문자열 생성
    query = f"*{chosen_tier} s#{args.solved_threshold}.."
    if args.user_ids:
        fixed_users = []
        for user in args.user_ids:
            # 만약 !@ 접두사가 없는 경우 자동 추가
            if not user.startswith("!@"):
                fixed_users.append(f"!@{user}")
            else:
                fixed_users.append(user)
        query += " " + " ".join(fixed_users)
    print(f"\n생성된 쿼리: {query}")

    # solved.ac API 호출
    try:
        # 반환되는 items는 문제 정보(dict) 리스트입니다.
        items = utils.search_random_problems(query)
    except Exception as e:
        print(f"\n랜덤 문제 검색 중 오류 발생: {e}")
        return

    # 검색된 전체 문제 정보 리스트 출력 (디버깅용)
    print(f"\n검색된 문제 개수: {len(items)}")
    for i, item in enumerate(items, start=1):
        print(f"[{i}] 문제번호: {item.get('problemId')}, 제목: {item.get('titleKo')}")

    # output_count만큼의 문제를 선택하여 최종 출력
    result_items = items[: args.output_count]
    if not result_items:
        print("\n조건에 맞는 추천 문제를 찾지 못했습니다.")
    else:
        print("\n추천 문제 :")
        for item in result_items:
            result_id = item.get("problemId", "N/A")
            title = item.get("titleKo", "제목 없음")
            user_cnt = item.get("acceptedUserCount", "N/A")
            avg_tries = item.get("averageTries", "N/A")
            # 최종 출력 양식에 맞추어 출력
            output_line = (
                f"문제번호 - {result_id}, 문제 제목 - {title}, 푼 사람 수 - {user_cnt}, "
                f"평균 시도 - {avg_tries}, [문제 링크](https://www.acmicpc.net/problem/{result_id})"
            )
            print(output_line)


if __name__ == "__main__":
    main()
