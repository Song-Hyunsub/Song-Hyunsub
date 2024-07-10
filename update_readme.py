import json
import os
from github import Github

# GitHub 토큰을 환경 변수에서 가져오기
token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')

# GitHub 리포지토리 접근
g = Github(token)
repo = g.get_repo(repo_name)

# languages.json 파일 로드
with open('languages.json') as f:
    languages = json.load(f)

# 언어 비율 계산
total_bytes = sum(languages.values())
language_percentages = {lang: (bytes / total_bytes) * 100 for lang, bytes in languages.items()}

# README.md 업데이트
readme_content = f"""
# My GitHub Profile

## Languages Used

{', '.join([f'{lang}: {percentage:.2f}%' for lang, percentage in language_percentages.items()])}
"""

# 기존 README.md 파일 로드
contents = repo.get_contents("README.md")
readme_content_old = contents.decoded_content.decode()

# 파일 내용이 변경된 경우에만 업데이트
if readme_content != readme_content_old:
    repo.update_file(contents.path, "Update README with latest languages", readme_content, contents.sha)
