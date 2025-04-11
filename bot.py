import os
import logging
import discord
from discord import app_commands
from discord.ext import commands
import utils

# 로깅 설정 (INFO 레벨 이상 출력)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()


bot = MyBot()


@bot.tree.command(name="랜덤디펜스", description="랜덤 문제를 검색합니다.")
@app_commands.describe(
    search_tier="검색 티어 (예: b3~b5 혹은 s2 혹은 g)",
    solved_threshold="입력된 숫자 이상의 사람이 푼 문제를 검색합니다 (예: 100, 1000, 10000)",
    output_count="출력할 문제 개수",
    user_ids="(선택) userid 형태로 입력 (여러 개 입력 가능, 띄어쓰기로 구분)",
)
async def random_problem(
    interaction: discord.Interaction,
    search_tier: str,
    solved_threshold: str,
    output_count: int,
    user_ids: str = "",
):
    # 작업 처리 동안 잠시 응답을 지연합니다.
    await interaction.response.defer(ephemeral=False)
    logger.info(
        f"/랜덤디펜스 호출됨: search_tier={search_tier}, "
        f"solved_threshold={solved_threshold}, output_count={output_count}, "
        f"user_ids={user_ids}"
    )

    try:
        # 티어 관련 로직 처리 (랜덤 티어 선택)
        chosen_tier = utils.choose_random_tier(search_tier)
        # 기본 쿼리 생성
        query = f"*{chosen_tier} s#{solved_threshold}.."
        if user_ids.strip():
            # 공백 기준으로 userid를 분리한 후, 각 userid에 접두사 '!@'가 없으면 추가함
            user_list = user_ids.strip().split()
            fixed_users = []
            for user in user_list:
                if not user.startswith("!@"):
                    fixed_users.append(f"!@{user}")
                else:
                    fixed_users.append(user)
            query += " " + " ".join(fixed_users)

        # solved.ac API 호출, 문제 정보 리스트(각 항목이 dict)를 반환받음
        random_problem_items = utils.search_random_problems(query)
    except Exception as e:
        await interaction.followup.send(
            f"랜덤 문제 검색 중 오류 발생: {e}", ephemeral=False
        )
        logger.error(f"문제 검색 중 오류 발생: {e}")
        return

    # output_count만큼의 문제 정보를 선택 (API 검색 결과에서 앞 부분을 선택)
    result_items = random_problem_items[:output_count]

    if not result_items:
        await interaction.followup.send(
            "조건에 맞는 추천 문제를 찾지 못했습니다.", ephemeral=False
        )
        logger.info("추천할 문제가 없습니다.")
    else:
        # 출력 양식에 맞춰 각 문제의 상세 정보를 문자열로 구성합니다.
        lines = []
        for item in result_items:
            result_id = item.get("problemId", "N/A")
            title = item.get("titleKo", "제목 없음")
            user_cnt = item.get("acceptedUserCount", "N/A")
            avg_tries = item.get("averageTries", "N/A")
            line = (
                f"문제번호 - {result_id}, 문제 제목 - {title}, 푼 사람 수 - {user_cnt}, "
                f"평균 시도 - {avg_tries}회, [문제 링크](https://www.acmicpc.net/problem/{result_id})"
            )
            lines.append(line)

        result_message = "추천 문제 :\n" + "\n".join(lines)
        await interaction.followup.send(result_message)
        logger.info(f"추천 문제: {result_message}")


@bot.tree.command(name="help", description="사용 가능한 명령어 목록을 확인합니다.")
async def help_command(interaction: discord.Interaction):
    help_message = (
        "사용 가능한 슬래시 명령어 목록:\n\n"
        "/랜덤디펜스 - 랜덤 문제를 검색합니다.\n"
        "   • search_tier: 검색 티어 (예: b3~b5, s2, g)\n"
        "   • solved_threshold: 입력된 숫자 이상의 사람이 푼 문제 (예: 100, 1000, 10000)\n"
        "   • output_count: 출력할 문제 개수\n"
        "   • user_ids: (선택) userid 입력. 유저들이 풀었던 문제는 제외하고 검색합니다. (예: user1 user2)\n\n"
        "/help - 사용 가능한 명령어 목록 확인.\n\n"
        "해당 코드는 오픈소스([Github](https://github.com/luckyvickyricky/BOJRandomDefense-Bot))로 공개되어 있습니다. "
        "오류 발견 시 수정하여 사용하거나, issue 남겨주시면 감사하겠습니다."
    )
    await interaction.response.send_message(help_message, ephemeral=False)


if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    else:
        bot.run(TOKEN)
