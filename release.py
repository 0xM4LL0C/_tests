import atexit
import subprocess
import sys
from typing import Literal
from semver import Version
import git

# cspell: disable

repo = git.Repo()

tags = repo.tags


tag = list(filter(lambda t: t.name.startswith("v"), tags))[-1]

version = Version.parse(tag.name.replace("v", "", 1))


def run_command(command: str, mode: Literal["exit", "raise"] = "exit"):
    """Выполняет команду в shell и завершает скрипт при ошибке"""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        if mode == "raise":
            raise e
        print(f"\n\nКоманда '{command}' завершилась с ошибкой.")
        sys.exit(1)


prerelease = False


def on_exit():
    try:
        run_command("git switch dev")
    except Exception as e:
        print(e)


atexit.register(on_exit)


match sys.argv[1].lower():
    case "major":
        version = version.bump_major()
    case "minor":
        version = version.bump_minor()
    case "patch":
        version = version.bump_patch()
    case "prerelease":
        version = version.bump_prerelease()
        prerelease = True
    case "build":
        version = version.bump_build()

run_command("git switch dev")

with open("version", "w") as f:
    f.write(str(version))

run_command("git status")

run_command('git add . && git commit -a -m "bump version" && git push')
run_command("git switch main")

run_command(f'gh pr create --base main --head release-v{version} --title "Release v{version}" --body "Автоматический PR для релиза версии {version}"')

run_command(f'gh pr merge release-v{version} --merge --delete-branch')

run_command(
    f'gh release create v{version} --target main --generate-notes {"-p" if prerelease else ""} --title v{version}'
)

print("Релиз успешно создан и опубликован.")

print("Релиз успешно создан и pull request автоматически смержен.")
run_command("git switch dev")
run_command("git fetch --tags")
