import os
import csv

# 1. 템플릿 파일 읽기
with open("templates/base.html", "r", encoding="utf-8") as f:
    template_content = f.read()

# 2. output 폴더 생성
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 3. 데이터 구조화 (CSV 읽기 + 인천/경기 자동 확장)
district_to_towns = {}
district_to_city = {}

# (1) 기존 CSV 파일 읽기 (서울 및 기존 데이터)
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
    # 수원시 구별
    "수원시 장안구": ["영화동", "조원동", "파장동", "정자동", "이목동", "율전동", "상광교동", "하광교동"],
    "수원시 권선구": ["세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "권선동", "곡반정동"],
    "수원시 팔달구": ["매교동", "매산동", "고등동", "화서동", "수원동", "인계동", "지동", "우만동"],
    "수원시 영통구": ["매탄동", "원천동", "영통동", "이의동", "하동", "보광동"],
    
    # 성남시 구별
    "성남시 수정구": ["신흥동", "태평동", "산성동", "단대동", "상적동", "둔촌동", "시흥동", "고등동"],
    "성남시 중원구": ["성남동", "중앙동", "금광동", "은행동", "하대원동", "도촌동"],
    "성남시 분당구": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "금곡동", "구미동", "판교동", "삼평동", "백현동", "운중동"],
    
    # 고양시 구별
    "고양시 덕양구": ["원신동", "흥도동", "효자동", "삼송동", "고양동", "관산동", "화정동", "행신동", "성사동"],
    "고양시 일산동구": ["식사동", "중산동", "정발산동", "풍산동", "백석동", "마두동", "장항동"],
    "고양시 일산서구": ["탄현동", "일산동", "주엽동", "대화동", "송포동", "덕이동"],
    
    # 용인시 구별
    "용인시 처인구": ["포곡읍", "모현읍", "역삼동", "유림동", "동부동", "양지면"],
    "용인시 기흥구": ["신갈동", "영덕동", "마북동", "구성동", "동백동", "상갈동", "보정동", "기흥동", "서농동"],
    "용인시 수지구": ["풍덕천동", "상현동", "성복동", "죽전동", "동천동", "신봉동"],
    
    # 기타 주요 시 (안양, 부천, 화성, 평택, 시흥, 파주, 의정부, 광주 등)
    "안양시 동안구": ["비산동", "관양동", "평촌동", "호계동", "부림동"],
    "안양시 만안구": ["안양동", "석수동", "박달동"],
    "부천시": ["원미동", "소사동", "역곡동", "중동", "상동", "심곡동", "약대동", "오정동", "내동"],
    "화성시": ["동탄동", "병점동", "봉담읍", "남양읍", "향남읍", "반월동"],
    "평택시": ["평택동", "송탄동", "팽성읍", "고덕면", "비전동", "서정동"],
    "파주시": ["금촌동", "문산읍", "운정동", "교하동", "법원읍"],
    "의정부시": ["의정부동", "가능동", "호원동", "신곡동", "송산동", "자금동"],
    "시흥시": ["정왕동", "대야동", "신천동", "은행동", "목감동", "배곧동"],
    "광주시": ["오포읍", "초월읍", "곤지암읍", "퇴촌면", "경안동", "송정동"]
}

for dist, towns in gyeonggi_data.items():
    district_to_city[dist] = "gyeonggi"
    district_to_towns[dist] = towns

# 4. 최상위 메인 화면용 [지역별 바로가기 네비게이션] 생성 (서울 / 인천 / 경기 분리)
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

# 5. 최상위 메인 페이지 생성
root_main_html = template_content.replace("{{ location_name }}", "전국(서울·인천·경기) 전지역")
root_main_html = root_main_html.replace('href="/"', 'href="index.html"')
if "</main>" in root_main_html:
    root_main_html = root_main_html.replace("</main>", f"{main_nav_html}</main>")

with open("index.html", "w", encoding="utf-8") as out:
    out.write(root_main_html)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(root_main_html)

# 6. 모든 구/시 메인 페이지 및 동별 세부 페이지 생성
total_towns = 0
created_districts = 0

for district_name, city in district_to_city.items():
    if city == "seoul":
        city_name = "서울특별시"
    elif city == "incheon":
        city_name = "인천광역시"
    else:
        city_name = "경기도"
    
    # 구/시 메인 페이지 생성
    dist_location = f"{city_name} {district_name} 전지역"
    dist_html = template_content.replace("{{ location_name }}", dist_location)
    dist_html = dist_html.replace('href="/"', 'href="../../../index.html"')
    
    towns_in_dist = district_to_towns.get(district_name, [])
    towns_nav = f'<div class="max-w-4xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-4 text-center">📍 {district_name} 세부 지역별 안내</h2><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
    for t in towns_in_dist:
        towns_nav += f'<a href="{t}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{t}</a>'
    towns_nav += '</div></div>'
    
    if "</main>" in dist_html:
        dist_html = dist_html.replace("</main>", f"{towns_nav}</main>")
    
    dist_dir = os.path.join(output_dir, city, district_name)
    os.makedirs(dist_dir, exist_ok=True)
    
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as out:
        out.write(dist_html)
    created_districts += 1
    
    # 동별 세부 페이지 생성
    for town_name in towns_in_dist:
        town_location = f"{city_name} {district_name} {town_name}"
        town_html = template_content.replace("{{ location_name }}", town_location)
        town_html = town_html.replace('href="/"', 'href="../../../../index.html"')
        
        town_dir = os.path.join(output_dir, city, district_name, town_name)
        os.makedirs(town_dir, exist_ok=True)
        
        with open(os.path.join(town_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(town_html)
        total_towns += 1

print(f"✨ 서울 + 인천 + 경기 전지역 통합 빌드 완료! (구/시: {created_districts}개, 동: {total_towns}개)")