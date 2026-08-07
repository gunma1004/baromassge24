from supabase import create_client, Client

# 1. Supabase 접속 정보
SUPABASE_URL = "https://ilyxesxzqbuswtfhqnww.supabase.co"
SUPABASE_SECRET_KEY = "sb_secret_hs3kdKBwMFzqS9lKm3lllQ_hGqFzNPr"

# 2. 클라이언트 연결
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

# 3. 테스트용 자동 게시글 데이터
new_post = {
    "title": "파이썬 자동 등록 첫 테스트 글",
    "content": "이 글은 Python 스크립트에서 Supabase DB로 자동 저장되었습니다.",
    "category": "seoul"
}

# 4. 'posts' 테이블에 저장
try:
    response = supabase.table("posts").insert(new_post).execute()
    print("✅ 글이 성공적으로 등록되었습니다!")
    print(response)
except Exception as e:
    print("❌ 등록 중 오류 발생:", e)