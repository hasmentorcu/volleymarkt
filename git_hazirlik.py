import os

GITIGNORE_CONTENT = """
# Django Standart
*.log
*.pot
*.pyc
__pycache__/
db.sqlite3
media/
staticfiles/
.env
venv/
.vscode/
.idea/
*.DS_Store
"""

def main():
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(GITIGNORE_CONTENT.strip())
    print("✅ .gitignore dosyası oluşturuldu! (Gereksiz dosyalar engellendi)")

if __name__ == '__main__':
    main()