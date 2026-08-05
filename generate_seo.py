import os
import csv
import re

# 1. 템플릿 파일 읽기
with open("templates/base.html", "r", encoding="utf-8") as f:
    template_content = f.read()

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 2. 데이터 구조화 (서울, 인천, 경기, 대전 전지역)
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

# (2) 인천광역시 주요 구/동 데이터
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

# (3) 경기도 주요 시/구 데이터
gyeonggi_data = {
    "수원시 장안구": ["영화동", "조원동", "파장동", "정자동", "이목동", "율전동"],
    "수원시 권선구": ["세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "권선동"],
    "성남시 분당구": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "금곡동", "구미동", "판교동"],
    "고양시 일산동구": ["식사동", "중산동", "정발산동", "백석동", "마두동", "장항동"],
    "용인시 수지구": ["풍덕천동", "상현동", "성복동", "죽전동", "동천동", "신봉동"],
    "부천시": ["원미동", "소사동", "역곡동", "중동", "상동", "심곡동"],
    "화성시": ["동탄동", "병점동", "봉담읍", "남양읍", "향남읍"]
}
for dist, towns in gyeonggi_data.items():
    district_to_city[dist] = "gyeonggi"
    district_to_towns[dist] = towns

# (4) 🌟 대전광역시 전지역 (동구, 중구, 서구, 유성구, 대덕구)
daejeon_data = {
    "대전 동구": ["중앙동", "신인동", "효동", "판암1동", "판암2동", "용운동", "대동", "자양동", "가양1동", "가양2동", "용전동", "성남동", "낭월동"],
    "대전 중구": ["은행선화동", "응동", "중촌동", "태평1동", "태평2동", "유천1동", "유천2동", "문화1동", "문화2동", "산성동"],
    "대전 서구": ["복수동", "도마1동", "도마2동", "변동", "용문동", "탄방동", "둔산1동", "둔산2동", "둔산3동", "갈마1동", "갈마2동", "월평1동", "월평2동", "월평3동", "관저1동", "관저2동", "기성동"],
    "대전 유성구": ["진잠동", "교동", "원신흥동", "태평동", "자운동", "반석동", "노은1동", "노은2동", "노은3동", "신성동", "전민동", "구즉동", "관평동"],
    "대전 대덕구": ["오정동", "대화동", "회덕동", "비래동", "송촌동", "중리동", "법동", "신탄진동", "석봉동", "덕암동", "목상동"]
}
for dist, towns in daejeon_data.items():
    district_to_city[dist] = "daejeon"
    district_to_towns[dist] = towns


# 3. 최상위 메인 화면 네비게이션 생성
main_nav_html = '<div class="max-w-5xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-6 text-center">📍 전국 지역별 전문관</h2>'
seoul_dists = [d for d, c in district_to_city.items() if c == "seoul"]
incheon_dists = [d for d, c in district_to_city.items() if c == "incheon"]
gyeonggi_dists = [d for d, c in district_to_city.items() if c == "gyeonggi"]
daejeon_dists = [d for d, c in district_to_city.items() if c == "daejeon"]

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
    main_nav_html += '<h3 class="text-sm font-bold text-gold-400 mb-2">🏡 경기도</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5 mb-6">'
    for dist in gyeonggi_dists:
        main_nav_html += f'<a href="output/gyeonggi/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
    main_nav_html += '</div>'

if daejeon_dists:
    main_nav_html += '<h3 class="text-sm font-bold text-gold-400 mb-2">🌟 대전광역시 (제휴점 2개 단독)</h3><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
    for dist in daejeon_dists:
        main_nav_html += f'<a href="output/daejeon/{dist}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{dist}</a>'
    main_nav_html += '</div>'

main_nav_html += '</div>'


# 4. 페이지 생성 함수 (대전 지역일 경우 다른 업체 전체 제거 및 대전 2개만 노출)
def make_page_html(location_str, nav_html, rel_path_to_root, is_daejeon=False):
    page_html = template_content
    
    seo_title = f"{location_str} 출장마사지 | 맞춤형 힐링 플랫폼"
    seo_desc = f"{location_str} 지역 맞춤형 서비스 및 공식 제휴점 정보 안내. 최적의 만족을 제공하는 {location_str} 전문관입니다."
    
    if "<title>" in page_html:
        page_html = re.sub(r'<title>.*?</title>', f'<title>{seo_title}</title>', page_html)
    else:
        page_html = page_html.replace('</head>', f'<title>{seo_title}</title>\n</head>')
        
    if 'name="description"' in page_html:
        page_html = re.sub(r'<meta name="description" content=".*?>', f'<meta name="description" content="{seo_desc}">', page_html)
    else:
        page_html = page_html.replace('</head>', f'<meta name="description" content="{seo_desc}">\n</head>')

    page_html = page_html.replace("{{ location_name }}", location_str)
    page_html = page_html.replace('href="/"', f'href="{rel_path_to_root}index.html"')
    
    # 대전 전지역 전용 2개 업체 카드 HTML
    daejeon_shops_html = f'''
    <section class="max-w-4xl mx-auto px-4 py-8">
        <div class="bg-[#121215] border border-gold-500/40 rounded-2xl p-6 shadow-xl">
            <h3 class="text-xl font-black text-gold-400 mb-6 text-center">🌟 {location_str} 공식 제휴점 안내</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 제휴점 1 -->
                <div class="bg-[#1a1a1f] p-6 rounded-2xl border border-gold-500/30 text-center shadow-lg hover:border-gold-400 transition-all">
                    <span class="bg-gold-500/20 text-gold-400 text-xs px-3 py-1 rounded-full font-bold">공식 제휴점 1</span>
                    <h4 class="text-xl font-extrabold text-white mt-3">S슬림홈타이</h4>
                    <p class="text-gray-400 text-sm mt-2">친절 예약 및 프리미엄 맞춤 케어 시스템</p>
                    <a href="tel:0507-1280-3342" class="mt-5 inline-block w-full bg-gold-500 hover:bg-gold-600 text-black font-black px-6 py-3 rounded-xl text-base transition-all shadow-md">📞 0507-1280-3342</a>
                </div>
                <!-- 제휴점 2 -->
                <div class="bg-[#1a1a1f] p-6 rounded-2xl border border-gold-500/30 text-center shadow-lg hover:border-gold-400 transition-all">
                    <span class="bg-gold-500/20 text-gold-400 text-xs px-3 py-1 rounded-full font-bold">공식 제휴점 2</span>
                    <h4 class="text-xl font-extrabold text-white mt-3">사쿠라 홈타이</h4>
                    <p class="text-gray-400 text-sm mt-2">신속 방문 및 힐링 전문 홈 케어</p>
                    <a href="tel:0507-1280-3343" class="mt-5 inline-block w-full bg-gold-500 hover:bg-gold-600 text-black font-extrabold px-6 py-3 rounded-xl text-base transition-all shadow-md">📞 0507-1280-3343</a>
                </div>
            </div>
        </div>
    </section>
    '''

    if is_daejeon:
        # base.html에 작성되어 있는 기존 메인 컨텐츠 영역을 대전 2개 업체 전용 섹션으로 완전히 치환
        if "<main" in page_html and "</main>" in page_html:
            main_start = page_html.find("<main")
            main_end = page_html.find("</main>") + 7
            main_open_tag = page_html[main_start:page_html.find(">", main_start) + 1]
            
            new_main_content = f"{main_open_tag}\n{daejeon_shops_html}\n{nav_html if nav_html else ''}\n</main>"
            page_html = page_html[:main_start] + new_main_content + page_html[main_end:]
    else:
        if nav_html and "</main>" in page_html:
            page_html = page_html.replace("</main>", f"{nav_html}</main>")
        
    return page_html

# 5. 최상위 메인 페이지 생성
root_main_html = make_page_html("전국(서울·인천·경기·대전) 전지역", main_nav_html, "")
with open("index.html", "w", encoding="utf-8") as out:
    out.write(root_main_html)
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(root_main_html)

# 6. 모든 구 및 동 페이지 생성
total_towns = 0
created_districts = 0

for district_name, city in district_to_city.items():
    if city == "seoul":
        city_name = "서울특별시"
    elif city == "incheon":
        city_name = "인천광역시"
    elif city == "gyeonggi":
        city_name = "경기도"
    else:
        city_name = "대전광역시"
    
    is_daejeon_region = (city == "daejeon")
    
    # (1) 구/시 메인 페이지
    dist_location = f"{city_name} {district_name}"
    towns_in_dist = district_to_towns.get(district_name, [])
    
    towns_nav = f'<div class="max-w-4xl mx-auto px-4 py-8"><h2 class="text-xl font-black text-white mb-4 text-center">📍 {district_name} 세부 지역별 안내</h2><div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2.5">'
    for t in towns_in_dist:
        towns_nav += f'<a href="{t}/index.html" class="bg-[#18181c] border border-gold-500/30 hover:border-gold-400 text-gray-200 hover:text-gold-400 py-2.5 px-2 rounded-xl text-xs font-bold text-center transition-all shadow-sm">{t}</a>'
    towns_nav += '</div></div>'
    
    dist_html = make_page_html(dist_location + " 전지역", towns_nav, "../../../", is_daejeon=is_daejeon_region)
    dist_dir = os.path.join(output_dir, city, district_name)
    os.makedirs(dist_dir, exist_ok=True)
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as out:
        out.write(dist_html)
    created_districts += 1
    
    # (2) 동 상세 페이지
    for town_name in towns_in_dist:
        town_location = f"{city_name} {district_name} {town_name}"
        town_html = make_page_html(town_location, "", "../../../../", is_daejeon=is_daejeon_region)
        
        town_dir = os.path.join(output_dir, city, district_name, town_name)
        os.makedirs(town_dir, exist_ok=True)
        with open(os.path.join(town_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(town_html)
        total_towns += 1

print(f"✨ 대전 단독 2개 업체 분리 및 전국 통합 빌드 완료! (구/시: {created_districts}개, 동: {total_towns}개)")