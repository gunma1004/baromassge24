import os
import csv

# 1. 템플릿 파일 읽기
with open("templates/base.html", "r", encoding="utf-8") as f:
    template_content = f.read()

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 2. 데이터 구조화 (서울, 인천, 경기 통합)
district_to_towns = {}
district_to_city = {}

# (1) 기존 CSV 파일 읽기
csv_path = "data/regions_with_shop.csv"
if os.path.exists(csv_path):
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row.get("city_code", "seoul")
            district_name = row.get("district_name", "")
            town_name = row.get("town_name", "")
            if district_name and town_name:
                district_to_city[district_name] = city
                if district_name not in district_to_towns:
                    district_to_towns[district_name] = []
                if town_name not in district_to_towns[district_name]:
                    district_to_towns[district_name].append(town_name)

# (2) 인천광역시 주요 구/동 데이터 추가
incheon_data = {
    "남동구": ["구월1동", "구월2동", "구월3동", "구월4동", "간석1동", "간석2동", "간석3동", "만수1동", "만수2동", "서창동", "논현동"],
    "연수구": ["옥련동", "선학동", "연수동", "청학동", "동춘동", "송도1동", "송도2동", "송도3동", "송도4동", "송도5동"],
    "부평구": ["부평1동", "부평2동", "부평3동", "산곡동", "청천동", "갈산동", "삼산동", "부개동", "십정동"],
    "서구": ["검암동", "경서동", "연희동", "가정동", "신현동", "석남동", "가좌동", "당하동", "마전동", "아라동"],
    "계양구": ["효성동", "계산동", "작전동", "작전서운동", "계양동"]
}
for dist, towns in incheon_data.items():
    district_to_city[dist] = "incheon"
    district_to_towns[dist] = towns

# (3) 경기도 주요 시/구 및 대표 동 데이터 추가
gyeonggi_data = {
    "수원시 장안구": ["영화동", "조원동", "파장동", "정자동", "이목동", "율전동"],
    "수원시 권선구": ["세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "권선동"],
    "수원시 팔달구": ["매교동", "매산동", "고등동", "화서동", "인계동", "지동", "우만동"],
    "수원시 영통구": ["매탄동", "원천동", "영통동", "이의동", "하동"],
    "성남시 수정구": ["신흥동", "태평동", "산성동", "단대동", "고등동"],
    "성남시 중원구": ["성남동", "중앙동", "금광동", "은행동", "하대원동", "도촌동"],
    "성남시 분당구": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "금곡동", "구미동", "판교동"],
    "고양시 덕양구": ["원신동", "흥도동", "효자동", "삼송동", "화정동", "행신동"],
    "고양시 일산동구": ["식사동", "중산동", "정발산동", "백석동", "마두동", "장항동"],
    "고양시 일산서구": ["탄현동", "일산동", "주엽동", "대화동", "덕이동"],
    "용인시 처인구": ["포곡읍", "모현읍", "역삼동", "유림동", "양지면"],
    "용인시 기흥구": ["신갈동", "영덕동", "마북동", "구성동", "동백동", "보정동"],
    "용인시 수지구": ["풍덕천동", "상현동", "성복동", "죽전동", "동천동", "신봉동"],
    "안양시 동안구": ["비산동", "관양동", "평촌동", "호계동", "부림동"],
    "부천시": ["원미동", "소사동", "역곡동", "중동", "상동", "심곡동"],
    "화성시": ["동탄동", "병점동", "봉담읍", "남양읍", "향남읍"],
    "평택시": ["평택동", "송탄동", "팽성읍", "비전동", "서정동"],
    "파주시": ["금촌동", "문산읍", "운정동", "교하동"],
    "의정부시": ["의정부동", "가능동", "호원동", "신곡동"],
    "시흥시": ["정왕동", "대야동", "신천동", "은행동", "배곧동"],
    "광주시": ["오포읍", "초월읍", "곤지암읍", "경안동"]
}
for dist, towns in gyeonggi_data.items():
    district_to_city[dist] = "gyeonggi"
    district_to_towns[dist] = towns

# 3. 최상위 메인 화면 네비게이션 생성
main_nav_html = '<div class="max-w-5xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-6 text-center">📍 전국 지역별 전문관</h2>'
seoul_dists = [d for d, c in district_to_city.items() if c == "seoul"]
incheon_dists = [d for d, c in district_to_city.items() if c == "incheon"]
gyeonggi_dists = [d for d, c in district_to_city.items() if c == "gyeonggi"]

if seoul_dists:
    main_nav_html += '<h3 class="text-sm font-bold text-gold-400 mb-2">🏙️ 서울특별시</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5 mb-6">'
    for dist in seoul_dists:
        main_nav_html += f'<a href="output/seoul/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
    main_nav_html += '</div>'

if incheon_dists:
    main_nav_html += '<h3 class="text-sm font-bold text-gold-400 mb-2">⚓ 인천광역시</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5 mb-6">'
    for dist in incheon_dists:
        main_nav_html += f'<a href="output/incheon/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
    main_nav_html += '</div>'

if gyeonggi_dists:
    main_nav_html += '<h3 class="text-sm font-bold text-gold-400 mb-2">🏡 경기도</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
    for dist in gyeonggi_dists:
        main_nav_html += f'<a href="output/gyeonggi/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
    main_nav_html += '</div>'
main_nav_html += '</div>'

# 4. 공통 메타 생성 함수 (페이지마다 타이틀과 디스크립션을 완전히 다르게 주입)
def make_page_html(location_str, nav_html, rel_path_to_root):
    page_html = template_content
    
    # 고유 SEO 타이틀 및 메타 디스크립션 생성
    seo_title = f"{location_str} 전문 안내 | 맞춤형 서비스 플랫폼"
    seo_desc = f"{location_str} 지역 맞춤형 서비스 안내 및 제휴점 정보. 최적의 만족을 제공하는 {location_str} 전문관입니다."
    
    # 템플릿 내에 타이틀이나 메타 태그 자리가 있다면 교체, 없으면 <head> 내부에 주입
    if "<title>" in page_html:
        # 기존 title 대체
        import re
        page_html = re.sub(r'<title>.*?</title>', f'<title>{seo_title}</title>', page_html)
    else:
        page_html = page_html.replace('</head>', f'<title>{seo_title}</title>\n</head>')
        
    if 'name="description"' in page_html:
        page_html = re.sub(r'<meta name="description" content=".*?>', f'<meta name="description" content="{seo_desc}">', page_html)
    else:
        page_html = page_html.replace('</head>', f'<meta name="description" content="{seo_desc}">\n</head>')

    # 지역 이름 치환
    page_html = page_html.replace("{{ location_name }}", location_str)
    
    # 상대 경로 정돈
    page_html = page_html.replace('href="/"', f'href="{rel_path_to_root}index.html"')
    
    # 네비게이션 주입
    if nav_html and "</main>" in page_html:
        page_html = page_html.replace("</main>", f"{nav_html}</main>")
        
    return page_html

# 5. 최상위 메인 페이지 생성
root_main_html = make_page_html("전국(서울·인천·경기) 전지역", main_nav_html, "")
with open("index.html", "w", encoding="utf-8") as out:
    out.write(root_main_html)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(root_main_html)

# 6. 모든 구 및 동 페이지 생성
total_towns = 0
created_districts = 0

for district_name, city in district_to_city.items():
    city_name = "서울특별시" if city == "seoul" else ("인천광역시" if city == "incheon" else "경기도")
    
    # (1) 구 메인 페이지
    dist_location = f"{city_name} {district_name}"
    towns_in_dist = district_to_towns.get(district_name, [])
    
    towns_nav = f'<div class="max-w-4xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-4 text-center">📍 {district_name} 세부 지역별 안내</h2><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
    for t in towns_in_dist:
        towns_nav += f'<a href="{t}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{t}</a>'
    towns_nav += '</div></div>'
    
    dist_html = make_page_html(dist_location + " 전지역", towns_nav, "../../../")
    dist_dir = os.path.join(output_dir, city, district_name)
    os.makedirs(dist_dir, exist_ok=True)
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as out:
        out.write(dist_html)
    created_districts += 1
    
    # (2) 동 상세 페이지
    for town_name in towns_in_dist:
        town_location = f"{city_name} {district_name} {town_name}"
        town_html = make_page_html(town_location, "", "../../../../")
        
        town_dir = os.path.join(output_dir, city, district_name, town_name)
        os.makedirs(town_dir, exist_ok=True)
        with open(os.path.join(town_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(town_html)
        total_towns += 1

print(f"✨ SEO 메타태그 동적 최적화 빌드 완료! (구/시: {created_districts}개, 동: {total_towns}개)")