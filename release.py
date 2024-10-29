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

try:
    run_command(f"git checkout -b release-v{version}", "raise")
except Exception:
    run_command(f"git switch release-v{version}")

with open("version", "w") as f:
    f.write(str(version))

run_command("git add .")
run_command('git commit -a -m "bump version"')
run_command(f"git push -u origin release-v{version}")

# Создаём pull request для релиза
run_command(f'gh pr create --base main --head release-v{version} --title "Release v{version}" --body "Автоматический PR для релиза версии {version}"')

# Автоматически мержим pull request
run_command(f'gh pr merge release-v{version} --merge --auto --delete-branch')

# Создаём релиз
run_command(f'gh release create v{version} --generate-notes {"-p" if prerelease else ""} --title v{version}')

print("Релиз успешно создан и pull request автоматически смержен.")