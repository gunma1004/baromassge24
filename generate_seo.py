import os
import csv

# 1. 템플릿 파일 읽기
with open("templates/base.html", "r", encoding="utf-8") as f:
    template_content = f.read()

# 2. output 폴더 생성
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 3. 데이터 구조화 (CSV 읽기 + 인천 데이터 자동 확장)
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

# (2) 인천광역시 주요 구/동 데이터 자동 추가 (원하시면 언제든 수정 가능)
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

# 4. 최상위 메인 화면용 [지역별 바로가기 네비게이션] 생성 (서울 / 인천 분리)
main_nav_html = '<div class="max-w-5xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-6 text-center">📍 전국 지역별 전문관</h2>'

seoul_dists = [d for d, c in district_to_city.items() if c == "seoul"]
incheon_dists = [d for d, c in district_to_city.items() if c == "incheon"]

if seoul_dists:
    main_nav_html += '<h3 class="text-sm font-bold text-gold-400 mb-2">🏙️ 서울특별시</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5 mb-6">'
    for dist in seoul_dists:
        main_nav_html += f'<a href="output/seoul/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
    main_nav_html += '</div>'

if incheon_dists:
    main_nav_html += '<h3 class="text-sm font-bold text-gold-400 mb-2">⚓ 인천광역시</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
    for dist in incheon_dists:
        main_nav_html += f'<a href="output/incheon/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
    main_nav_html += '</div>'

main_nav_html += '</div>'

# 5. 최상위 메인 페이지 생성
root_main_html = template_content.replace("{{ location_name }}", "전국(서울·인천) 전지역")
root_main_html = root_main_html.replace('href="/"', 'href="index.html"')
if "</main>" in root_main_html:
    root_main_html = root_main_html.replace("</main>", f"{main_nav_html}</main>")

with open("index.html", "w", encoding="utf-8") as out:
    out.write(root_main_html)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(root_main_html)

# 6. 모든 구 메인 페이지 및 동별 세부 페이지 생성
total_towns = 0
created_districts = 0

for district_name, city in district_to_city.items():
    city_name = "서울특별시" if city == "seoul" else "인천광역시"
    
    # 구 메인 페이지 생성
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

print(f"✨ 서울 + 인천 통합 빌드 완료! (구: {created_districts}개, 동: {total_towns}개)")