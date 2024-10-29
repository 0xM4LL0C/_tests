import subprocess
import sys
from semver import Version
import git

repo = git.Repo()

tags = repo.tags



tag = list(filter(lambda t: t.name.startswith("v"), tags))[-1]

version = Version.parse(tag.name.replace("v", "", 1))





def run_command(command: str):
    """Выполняет команду в shell и завершает скрипт при ошибке"""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\n\nКоманда '{command}' завершилась с ошибкой.")
        sys.exit(1)

prerelease = False






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

head = repo.create_head(f"release-v{version}")
head.checkout()
run_command("git status")

repo.index.add(["."])
repo.index.commit("test bump")

with open("version", "w") as f:
    f.write(str(version))

# Создаём pull request для релиза
run_command(f'gh pr create --base main --head release-v{version} --title "Release v{version}" --body "Автоматическое создание PR для релиза версии {version}"')

# Мержим pull request в main (автоматически)
run_command('gh pr merge --squash --auto --delete-branch')

# Создаём релиз на GitHub после слияния pull request
run_command(f'gh release create v{version} --notes-file release_body.md {"-p" if prerelease else ""} --title v{version}')

print("Релиз успешно создан и опубликован.")
