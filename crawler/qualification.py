import logging
import re
from time import sleep
from typing import List

import requests
import urllib3
from bs4 import BeautifulSoup
from pydantic import BaseModel

import config

logging.basicConfig(level=logging.INFO)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Qualification(BaseModel):
    code: str
    name: str


async def get_details(qualifications: List[Qualification]):
    details = []
    for qualification in qualifications:
        soup = crawling(qualification.code, qualification.name)

        schedule = get_schedule(soup)
        fee = get_fee(soup)
        tendency = get_tendency_and_acquisition(soup, "출제경향")
        standard = get_standard_and_question(soup, "출제기준")
        question = get_standard_and_question(soup, "공개문제")
        acquisition = get_tendency_and_acquisition(soup, "취득방법")

        book_info = get_book_info(qualification.name)
        books = parse_book_info(book_info)

        qualification_details = {"name": qualification.name, "code": qualification.code, "schedule": schedule,
                                 "fee": fee, "tendency": tendency, "standard": standard, "question": question,
                                 "acquisition": acquisition, "books": books}
        details.append(qualification_details)

        logging.info(f"{qualification.name} : {qualification_details}")

    return details


# 크롤링
def crawling(code, name):
    url = f"https://www.q-net.or.kr/crf005.do?id=crf00503s02&gSite=Q&gId=&jmInfoDivCcd=B0&jmCd={code}&jmNm={name}"
    try:
        response = requests.get(
            url=url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.18 Safari/537.36"},
            verify=False
        )
    except ConnectionError:
        logging.error("Connection refused")
        return None

    sleep(0.5)  # max tries exceeded with url 에러 방지를 위해 0.5초 딜레이 추가

    soup = BeautifulSoup(response.content, 'html.parser')

    return soup


# 시험일정
def get_schedule(soup):
    div_element = soup.select_one(".tbl_normal.tdCenter.mb0")
    if not div_element:
        return None

    schedule_rows = div_element.select("tbody > tr")
    schedules = []

    for row in schedule_rows:
        cells = row.select("td")
        schedule_data = []

        for cell in cells:
            text = cell.text.strip().replace('\n', ' ').replace('\r', '').replace('\t', '')
            text = re.sub(r'\s*~\s*', '~', text)
            colspan = cell.get('colspan')

            if colspan:
                colspan = int(colspan)
                schedule_data.extend([text] * colspan)
            else:
                schedule_data.append(text)

        if "시험 일정이 없습니다." in schedule_data:
            return None

        if len(schedule_data) > 4:
            practical_app_raw = schedule_data[4]
            practical_app_parts = practical_app_raw.split(" ") if practical_app_raw else None
            practical_app = practical_app_parts[0] if practical_app_parts else None
            schedule_data[4] = practical_app

        if len(schedule_data) >= 7:
            schedule = {
                "category": schedule_data[0] if schedule_data[0] else None,  # 구분
                "writtenApp": schedule_data[1] if schedule_data[1] else None,  # 필기원서접수
                "writtenExam": schedule_data[2] if schedule_data[2] else None,  # 필기시험
                "writtenExamResult": schedule_data[3] if schedule_data[3] else None,  # 필기합격발표
                "practicalApp": schedule_data[4] if schedule_data[4] else None,  # 실기원서접수
                "practicalExam": schedule_data[5] if schedule_data[5] else None,  # 실기시험
                "practicalExamResult": schedule_data[6] if schedule_data[6] else None  # 최종합격자 팔표일
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
        'writtenFee': r'필기\s*:\s*([\d,]+)\s*원',
        'practicalFee': r'실기\s*:\s*([\d,]+)\s*원',
    }

    for exam_type, pattern in fee_pattern.items():
        match = re.search(pattern, fee_text)
        if match:
            fee = int(match.group(1).replace(',', ''))
            fees[exam_type] = fee
        else:
            fees[exam_type] = None

    return fees


# 출제기준 및 공개문제
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


# 카카오 책 검색 API
def get_book_info(query):
    url = f"https://dapi.kakao.com/v3/search/book?target=title&sort=latest&size=5&query={query}"
    headers = {"Authorization": f"KakaoAK {config.kakao_api_key}"}
    response = requests.get(url, headers=headers)
    return response.json()


def parse_book_info(book_info):
    books = []
    for document in book_info["documents"]:
        book = {
            "authors": document["authors"],  # 저자
            "datetime": document["datetime"],  # 출간일
            "price": document["price"],  # 정가
            "publisher": document["publisher"],  # 출판사
            "sale_price": document["sale_price"],  # 판매가
            "thumbnail": document["thumbnail"],  # 책 표지
            "title": document["title"],  # 제목
            "url": document["url"]  # 링크
        }
        books.append(book)
    return books
