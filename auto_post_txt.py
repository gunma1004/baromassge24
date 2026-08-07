from supabase import create_client, Client

# 1. Supabase 접속 정보
SUPABASE_URL = "https://ilyxesxzqbuswtfhqnww.supabase.co"
SUPABASE_SECRET_KEY = "sb_publishable_MsZQkYYDbioESCVT3t7lGw_kyJQRqPg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

TITLE_FILE = "titles.txt"
CONTENT_FILE = "contents.txt"
CATEGORY_FILE = "categories.txt"

def pop_first_line(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            return None
        first_line = lines[0].strip()
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])
        return first_line
    except FileNotFoundError:
        print(f"❌ {file_path} 파일을 찾을 수 없습니다.")
        return None

def post_from_text_files():
    title = pop_first_line(TITLE_FILE)
    content = pop_first_line(CONTENT_FILE)
    category = pop_first_line(CATEGORY_FILE)

    if not title or not content:
        print("💡 남은 제목이나 내용이 없습니다. 메모장 파일을 확인해 주세요.")
        return

    if not category:
        category = "서울"

    final_title = title.replace("{키워드}", category)
    final_content = content.replace("{키워드}", category).replace("<br>", "\n")

    try:
        supabase.table("posts").insert({
            "title": final_title,
            "content": final_content,
            "category": category
        }).execute()
        print(f"✅ 치환 완료 및 자동 등록 성공!")
        print(f"📌 변환된 제목: {final_title}")
        print(f"🏷️ 적용된 키워드: {category}")
    except Exception as e:
        print(f"❌ DB 등록 실패: {e}")

if __name__ == "__main__":
    post_from_text_files()