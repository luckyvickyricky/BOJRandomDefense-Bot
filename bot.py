import os

import discord
from discord import app_commands
from discord.ext import commands

import utils


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
    solved_threshold="입력된 숫자 이상의 사람이 푼 문제를 검색합니다 (예: 100 혹은 1000 혹은 10000)",
    output_count="출력할 문제 개수를 조정합니다",
    user_ids="유저 아이디:해당 유저가 푼 문제는 제외 후 검색합니다(여러 개 입력 가능, 띄어쓰기로 구분)",
)
async def random_problem(
    interaction: discord.Interaction,
    search_tier: str,
    solved_threshold: str,
    output_count: int,
    user_ids: str,
):
    user_ids_list = user_ids.split()

    try:
        chosen_tier = utils.choose_random_tier(search_tier)
        random_problem_ids = utils.search_random_problems(chosen_tier, solved_threshold)
    except Exception as e:
        await interaction.response.send_message(
            f"랜덤 문제 검색 중 오류 발생: {e}", ephemeral=True
        )
        return

    solved_set = utils.get_solved_problem_ids(user_ids_list)
    result_ids = utils.filter_unsolved_problems(
        random_problem_ids, solved_set, output_count
    )

    if not result_ids:
        await interaction.response.send_message(
            "사용자들이 풀지 않은 문제를 찾지 못했습니다.", ephemeral=True
        )
    else:
        result_message = "추천 문제 (문제 번호):\n" + "\n".join(map(str, result_ids))
        await interaction.response.send_message(result_message)


@bot.tree.command(name="help", description="사용 가능한 명령어 목록을 확인합니다.")
async def help_command(interaction: discord.Interaction):
    help_message = (
        "사용 가능한 슬래시 명령어 목록:\n\n"
        "/랜덤디펜스 - 랜덤 문제를 검색합니다.\n"
        "   • search_tier: 검색 티어 (예: b3~b5(브3~브5에서) 또는 s2(실2에서) 또는 g(골드에서))\n"
        "   • solved_threshold: 입력된 숫자 이상의 사람이 푼 문제를 검색합니다.(예: 100명이상 혹은 10000명이상)\n"
        "   • output_count: 출력할 문제 개수\n"
        "   • user_ids: 유저 아이디:해당 유저가 푼 문제는 제외 후 검색합니다 (여러 개 입력 가능, 띄어쓰기로 구분)\n\n"
        "/help - 사용 가능한 명령어 목록을 확인합니다.\n\n"
        "해당 코드는 오픈소스([Github](https://github.com/luckyvickyricky/BOJRandomDefense-Bot))로 개발되었습니다."
        "오류 발견시 수정하셔서 사용하시거나, issue 남겨주시면 감사하겠습니다."
    )
    await interaction.response.send_message(help_message, ephemeral=True)


if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("DISCORD_TOKEN 환경 변수가 설정되지 않았습니다.")
    else:
        bot.run(TOKEN)
