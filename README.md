# Cubrism


## :bookmark: 목차
+ [개요](#pushpin-개요)
+ [API Docs](#abacus-api-docs)
+ [적용 기술](#screwdriver-적용-기술)
+ [시스템 구조도](#gear-시스템-구조도)
+ [팀](#family_man_woman_boy_boy-팀)

</br>

## :pushpin: 개요
자격증은 개인의 전문성과 능력을 나타내는 중요한 지표에 해당한다. 따라서 우리는 자격증 취득을 위해 공부하는 현대인들로 하여금 정보 취득이 용이하도록, 관련 자료를 한데 모아 그 편의성을 높인 모바일 어플리케이션을 제작하였다. Cubrism은 Cube와 -ism을 결합한 단어로써 큐브와 같은 구조적이고 다면적인 기능을 통해 사용자들은 ‘관심 자격증’을 설정하여 본인이 취득하고자 하는 자격 정보를 간편하게 열람할 수 있으며, 스터디 그룹에 참가하여 목표를 세우고 함께 공부함으로써 동기부여를 높일 수 있다. 또한 Q&A 게시판을 통해 타 사용자들과 지식을 공유하고, 일정 관리 기능을 활용하여 계획적인 학습 환경을 조성하는 등 다양한 측면에서 유용한 도움을 얻을 수 있다.

</br>

## :abacus: API Docs
### 자격증 상세정보 요청하기

| **HTTP** | **Path**  |
| --------- | --------- |
| POST | /qualification |

#### 요청
```json
[
    {
        "code": "1320",
        "name": "정보처리기사"
    },
    ···
]
```

#### 응답
```json
[
    {
        "name": "정보처리기사",
        "code": "1320",
        "schedule": [
            {
                "category": "2024년 정기 기사 1회",
                "writtenApp": "2024.01.23~2024.01.26",
                "writtenExam": "2024.02.15~2024.03.07",
                "writtenExamResult": "2024.03.13",
                "practicalApp": "2024.03.26~2024.03.29",
                "practicalExam": "2024.04.27~2024.05.17",
                "practicalExamResult": "2024.06.18"
            },
            ···
        ],
        "fee": {
            "writtenFee": 19400,
            "practicalFee": 22600
        },
        "tendency": "<실기시험 출제 경향>\n정보시스템 등의 개발 요구 사항을 이해하여 각 업무에 맞는 소프트웨어의 기능에 관한 설계, 구현 및 테스트를 수행에 필요한\n1. 현행 시스템 분석 및 요구사항 확인(소프트웨어 공학 기술의 요구사항 분석 기법 활용)\n2. 데이터 입출력 구현(논리, 물리데이터베이스 설계, 조작 프로시저 등) ···",
        "standard": [
            {
                "filePath": "bbs/Q006/Q006_2204043",
                "fileName": "정보처리기사 출제기준(2020.1.1.~2022.12.31).hwp"
            },
            ···
        ],
        "question": null,
        "acquisition": "① 시 행 처 : 한국산업인력공단\n② 관련학과 : 모든 학과 응시가능 ···",
        "books": [
            {
                "authors": [
                    "에듀채널 편집부"
                ],
                "datetime": "2024-05-17T00:00:00.000+09:00",
                "price": 9000,
                "publisher": "북스케치",
                "sale_price": -1,
                "thumbnail": "https://search1.kakaocdn.net/thumb/R120x174.q85/?fname=http%3A%2F%2Ft1.daumcdn.net%2Flbook%2Fimage%2F6635273",
                "title": "정보처리산업기사 필기 기출 및 예상 문제",
                "url": "https://search.daum.net/search?w=bookpage&bookId=6635273&q=%EC%A0%95%EB%B3%B4%EC%B2%98%EB%A6%AC%EC%82%B0%EC%97%85%EA%B8%B0%EC%82%AC+%ED%95%84%EA%B8%B0+%EA%B8%B0%EC%B6%9C+%EB%B0%8F+%EC%98%88%EC%83%81+%EB%AC%B8%EC%A0%9C"
            },
            ···
        ]
    },
    ···
]
```

</br>

## :screwdriver: 적용 기술
<ul>
  <li>Language: <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"></li>
  <li>Framework: <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"></li>
  <li>tool: <img src="https://img.shields.io/badge/pycharm-000000?style=for-the-badge&logo=pycharm&logoColor=white"></li>
</ul>

</br>

## :gear: 시스템 구조도
![시스템 구조도](https://raw.githubusercontent.com/caadiq/Cubrism/master/image/%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B5%AC%EC%84%B1%EB%8F%84.png)

</br>

## :family_man_woman_boy_boy: 팀
