"""1주차 연습: 데이터 생성 → 집계 → 결과 CSV/JSON 출력
실행: python solution.py
출력: data.csv(원본), 결과_센터별.csv(제출용), result.json(웹페이지용)
"""
import json
import numpy as np
import pandas as pd

# 1) 연습용 가상 데이터 (실전에서는 주어진 CSV를 pd.read_csv로 읽으면 됨)
np.random.seed(0)
n = 300
df = pd.DataFrame({
    "센터": np.random.choice(["흥해", "청하", "덕산", "두호", "장량", "기계"], n),
    "유형": np.random.choice(["화재", "구조", "구급"], n, p=[0.2, 0.2, 0.6]),
    "도착시간_분": np.random.normal(7, 2, n).round(1),
})
df.loc[np.random.choice(n, 10, replace=False), "도착시간_분"] = np.nan  # 결측 일부러 넣기
df.to_csv("data.csv", index=False, encoding="utf-8-sig")

# 2) 정제: 결측·이상치 처리 (실전에서 제출물.md에 '왜 이렇게 했는지' 적을 부분)
before = len(df)
df = df.dropna(subset=["도착시간_분"])
df = df[(df["도착시간_분"] > 0) & (df["도착시간_분"] < 30)]
print(f"정제: {before}건 → {len(df)}건")

# 3) 집계
res = (
    df.groupby("유형")["도착시간_분"]
    .agg(건수="count", 평균="mean", 최대="max")
    .round(2)
    .reset_index()
    .sort_values("평균")
)
print(res)

# 4) 출력: 제출용 CSV + 웹페이지용 JSON
res.to_csv("결과_유형별.csv", index=False, encoding="utf-8-sig")
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(res.to_dict(orient="records"), f, ensure_ascii=False, indent=2)
print("완료: 결과_센터별.csv, result.json")
