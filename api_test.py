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

    # 랜덤 문제 검색
    try:
        random_problem_ids = utils.search_random_problems(
            chosen_tier, args.solved_threshold
        )
    except Exception as e:
        print(f"랜덤 문제 검색 중 오류 발생: {e}")
        return
    print("\n랜덤 검색된 문제 번호들:")
    print(random_problem_ids)

    # 유저들이 푼 문제 번호 집합 생성
    solved_set = utils.get_solved_problem_ids(args.user_ids)
    print("\n유저들이 푼 문제 번호 집합:")
    print(solved_set)

    # 사용자들이 풀지 않은 문제 선택
    result_ids = utils.filter_unsolved_problems(
        random_problem_ids, solved_set, args.output_count
    )
    print("\n추천 문제 (사용자들이 풀지 않은 문제):")
    print(result_ids)


if __name__ == "__main__":
    main()
