from typing import List
from fastapi import FastAPI, HTTPException
from crawler.qualification import get_details, Qualification
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

app = FastAPI()


# KoBERT 모델과 토크나이저 로드해오기
model_name = "monologg/kobert"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=7)

# 감정 분석 파이프라인 생성하기
emotion_analysis = pipeline("text-classification", model=model, tokenizer=tokenizer, return_all_scores=True)

# 분석할 문장(임시)
text = "이 영화 정말 재미있어요! 다음에 또 보고 싶어요!"

# 감정 분석 수행
result = emotion_analysis(text)

# 감정 라벨 매핑 정의
emotion_labels = {
    'LABEL_0': '기쁨 (Joy)',
    'LABEL_1': '슬픔 (Sadness)',
    'LABEL_2': '분노 (Anger)',
    'LABEL_3': '공포 (Fear)',
    'LABEL_4': '혐오 (Disgust)',
    'LABEL_5': '놀람 (Surprise)',
    'LABEL_6': '중립 (Neutral)'
}

# 가장 높은 점수를 가진 감정 리턴 및 감정 이름으로 변환
highest_emotion = max(result[0], key=lambda x: x['score'])
emotion_name = emotion_labels[highest_emotion['label']]
highest_emotion['label'] = emotion_name

print(result)
print(highest_emotion)
print(highest_emotion)
print(highest_emotion)

@app.post("/qualification")
async def qualification_details(qualifications: List[Qualification]):
    try:
        details = await get_details(qualifications)
        return details
    except Exception as e:
        print(f"Error occurred while getting details: {e}")
        raise HTTPException(status_code=400, detail=str(e))
