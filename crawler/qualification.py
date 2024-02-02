import re
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Qualification(BaseModel):
    code: str
    name: str


async def get_details(qualifications: List[Qualification]):
    details = {}
    for qualification in qualifications:
        soup = crawling(qualification.code, qualification.name)

        schedule = get_schedule(soup)
        fee = get_fee(soup)
        tendency = get_tendency_and_acquisition(soup, "출제경향")
        standard = get_standard_and_question(soup, "출제기준")
        question = get_standard_and_question(soup, "공개문제")
        acquisition = get_tendency_and_acquisition(soup, "취득방법")

        details[qualification.name] = {"시험일정": schedule, "수수료": fee, "출제경향": tendency, "출제기준": standard, "공개문제": question, "취득방법": acquisition}

    return details


# 크롤링
def crawling(code, name):
    url = f"https://www.q-net.or.kr/crf005.do?id=crf00503s02&gSite=Q&gId=&jmInfoDivCcd=B0&jmCd={code}&jmNm={name}"
    response = requests.get(
        url=url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.18 Safari/537.36"}
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup


# 시험일정
def get_schedule(soup):
    div_element = soup.select_one(".tbl_normal.tdCenter.mb0")
    schedule_tables = div_element.select("table")

    schedules = []
    for schedule_table in schedule_tables:
        schedule_rows = schedule_table.select("tbody > tr")

        for row in schedule_rows:
            cells = row.select("td")
            # 구분
            category = cells[0].get_text(strip=True) if cells[0].get_text(strip=True) else None
            # 필기원서접수
            written_app = cells[1].get_text(strip=True) if cells[1].get_text(strip=True) else None
            written_app = re.sub(r'\s*~\s*', '~', written_app)
            # 필기시험
            written_exam = cells[2].get_text(strip=True) if cells[2].get_text(strip=True) else None
            written_exam = re.sub(r'\s*~\s*', '~', written_exam)
            # 필기합격발표
            written_exam_result = cells[3].get_text(strip=True) if cells[3].get_text(strip=True) else None

            # 실기원서접수
            practical_app_raw = cells[4].get_text(" ", strip=True) if cells[4].get_text(" ",strip=True) else None
            practical_app_parts = practical_app_raw.split(" ") if practical_app_raw else None
            practical_app = practical_app_parts[0] if practical_app_parts else None
            practical_app = re.sub(r'\s*~\s*', '~', practical_app)

            # 실기시험
            practical_exam = cells[5].get_text(strip=True) if cells[5].get_text(strip=True) else None
            practical_exam = re.sub(r'\s*~\s*', '~', practical_exam)
            # 최종합격자 발표일
            ptractical_exam_result = cells[6].get_text(strip=True) if cells[6].get_text(strip=True) else None

            schedule = {
                "구분": category,
                "필기원서접수": written_app,
                "필기시험": written_exam,
                "필기합격발표": written_exam_result,
                "실기원서접수": practical_app,
                "실기시험": practical_exam,
                "최종합격자 발표일": ptractical_exam_result,
            }

            schedules.append(schedule)

    return schedules


# 수수료
def get_fee(soup):
    dt_element = soup.find("dt", string="수수료")
    if not dt_element:
        return None

    dd_element = dt_element.find_next_sibling("dd")
    if not dd_element:
        return None

    fee_text = " ".join(dd_element.get_text(strip=True).split())

    fees = {}
    fee_pattern = {
        '필기': r'필기\s*:\s*([\d,]+)\s*원',
        '실기': r'실기\s*:\s*([\d,]+)\s*원',
    }

    for exam_type, pattern in fee_pattern.items():
        match = re.search(pattern, fee_text)
        if match:
            fee = int(match.group(1).replace(',', ''))
            fees[exam_type] = fee
        else:
            fees[exam_type] = None

    return fees


#출제기준 및 공개문제
def get_standard_and_question(soup, title):
    dt_element = soup.find("dt", string=title)
    if not dt_element:
        return None

    dd_element = dt_element.find_next_sibling("dd")
    if not dd_element:
        return None

    file_element = dd_element.select("em.file")
    standards = []

    for file in file_element:
        button = file.find("button")
        onclick = button.get("onclick")
        standard_pattern = re.search(r"fileDown\(\s*'([^']+)',\s*'([^']+)',", onclick)

        if standard_pattern:
            file_path = standard_pattern.group(1)
            file_name = standard_pattern.group(2)
            standard = {
                "filePath": file_path,
                "fileName": file_name
            }
            standards.append(standard)

    return standards


# 출제경향 및 취득방법
def get_tendency_and_acquisition(soup, title):
    dt_element = soup.find("dt", string=title)
    if not dt_element:
        return None

    dd_element = dt_element.find_next_sibling("dd")
    if not dd_element:
        return None

    text_element = dd_element.find("textarea")
    if not text_element:
        return None

    text = "".join(text_element.strings)
    # \r 제거 : \r\n은 윈도우에서 사용하는 줄바꿈 문자로 안드로이드에선 불필요
    text = text.replace('\r', '')
    # \n 앞뒤 공백 제거
    text = re.sub(r'\s*\n\s*', '\n', text)
    # 맨 앞, 맨 뒤 \n 제거
    text = text.lstrip('\n').rstrip('\n')

    return text
