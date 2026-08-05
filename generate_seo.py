import os
import csv

# 1. 템플릿 파일 읽기
with open("templates/base.html", "r", encoding="utf-8") as f:
    template_content = f.read()

# 2. output 폴더 생성
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 3. CSV 데이터 읽어서 구별 동 목록 구조화하기
district_to_towns = {}
district_to_city = {}

with open("data/regions_with_shop.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        city = row.get("city_code", "seoul")
        district_name = row.get("district_name", "송파구")
        town_name = row.get("town_name", "잠실동")
        
        district_to_city[district_name] = city
        if district_name not in district_to_towns:
            district_to_towns[district_name] = []
        if town_name not in district_to_towns[district_name]:
            district_to_towns[district_name].append(town_name)

# 4. 최상위 메인 화면용 [구 선택 네비게이션 HTML] 생성
main_nav_html = '<div class="max-w-4xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-4 text-center">📍 서울시 지역별 전문관</h2><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
for dist, city in district_to_city.items():
    # 최상위 루트 기준 구 페이지 경로 (output/seoul/강서구/index.html 이므로 웹서버 루트 기준 상대경로 설정)
    main_nav_html += f'<a href="output/{city}/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
main_nav_html += '</div></div>'

# 5. 최상위 메인 페이지 생성 (root 및 output/index.html)
root_main_html = template_content.replace("{{ location_name }}", "서울시 전지역")
root_main_html = root_main_html.replace('href="/"', 'href="index.html"')
if "</main>" in root_main_html:
    root_main_html = root_main_html.replace("</main>", f"{main_nav_html}</main>")

with open("index.html", "w", encoding="utf-8") as out:
    out.write(root_main_html)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(root_main_html)

# 6. 구 메인 페이지 및 동별 세부 페이지 생성
count = 0
created_districts = set()

with open("data/regions_with_shop.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        city = row.get("city_code", "seoul")
        city_name = row.get("city_name", "서울시")
        district_name = row.get("district_name", "송파구")
        town_name = row.get("town_name", "잠실동")
        
        # --- [A] 동별 세부 페이지 생성 (output/seoul/구이름/동이름/index.html)
        town_location = f"{city_name} {district_name} {town_name}"
        town_html = template_content.replace("{{ location_name }}", town_location)
        # 동 페이지에서 최상위 메인으로 갈 때 (상위로 4번 올라가기)
        town_html = town_html.replace('href="/"', 'href="../../../../index.html"')
        
        town_dir = os.path.join(output_dir, city, district_name, town_name)
        os.makedirs(town_dir, exist_ok=True)
        
        with open(os.path.join(town_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(town_html)
        count += 1
        
        # --- [B] 구 단위 메인 페이지 생성 (output/seoul/구이름/index.html)
        if district_name not in created_districts:
            dist_location = f"{city_name} {district_name} 전지역"
            dist_html = template_content.replace("{{ location_name }}", dist_location)
            # 구 메인 페이지에서 최상위 메인으로 갈 때 (상위로 3번 올라가기)
            dist_html = dist_html.replace('href="/"', 'href="../../../index.html"')
            
            # 해당 구에 속한 모든 동들로 바로 이동할 수 있는 [동 바로가기 버튼 목록] 생성
            towns_in_dist = district_to_towns.get(district_name, [])
            towns_nav = f'<div class="max-w-4xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-4 text-center">📍 {district_name} 세부 지역별 안내</h2><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
            for t in towns_in_dist:
                # 구 메인(output/seoul/강서구/index.html)에서 동(output/seoul/강서구/가양동/index.html)으로 가려면 하위 폴더명 바로 지정
                towns_nav += f'<a href="{t}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{t}</a>'
            towns_nav += '</div></div>'
            
            if "</main>" in dist_html:
                dist_html = dist_html.replace("</main>", f"{towns_nav}</main>")
            
            dist_dir = os.path.join(output_dir, city, district_name)
            os.makedirs(dist_dir, exist_ok=True)
            
            with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as out:
                out.write(dist_html)
            
            created_districts.add(district_name)

print(f"✨ 완벽 연동 빌드 완료! (구 메인 페이지: {len(created_districts)}개, 동 상세 페이지: {count}개)")