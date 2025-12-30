from re import escape
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import roc_curve, roc_auc_score

st.set_page_config(
    page_title="장이선 - 최종 모델 리포트",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
        .header {
            text-align: center;
        }
        .box {
            margin: 0 auto;
        }
    </style>
    <div class="header">
        <h1 style='margin: 0;'>은행 이탈고객 예측 모델 리포트</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ============================
# Feature Engineering
# ============================

st.subheader("Feature Engineering")
feature_df = pd.DataFrame(
    {
        "특성": [
            "balance_ratio",
            "credit_usage_rate",
            "has_balance",
            "many_products",
            "long_tenure",
            "score_active",
            "balance_active",
        ],
        "특성 생성 방법": [
            "balance / estimated_salary",
            "balance / credit_score",
            "balance > 0 여부 (이진 특성)",
            "products_number ≥ 3 여부",
            "tenure ≥ 7 여부",
            "credit_score × active_member",
            "balance × active_member",
        ],
        "비고": ["연봉 대비 잔고 수준",
    "신용점수 대비 잔고 수준",
    "잔고 여부",
    "3개 이상 상품 보유 여부",
    "7년 이상 거래 여부",
    "신용점수 × 활동성 지표",
    "잔고 × 활동성 지표",
    ],
    },
)
st.dataframe(feature_df, hide_index=True)

st.divider()

# ============================
# Preprocessing
# ============================

st.subheader("Preprocessing")
st.markdown(":orange-badge[✔️ SVM 및 트리 기반 모델을 함께 사용하기 위해 모든 수치형 변수에 StandardScaler 적용]")
encoding_df = pd.DataFrame(
    {
        "특성": ["성별(Gender)",
            "국가(Country)"],
        "인코딩 방법": ["OHE (pd.get_dummies, drop_first=True)","OHE(pd.get_dummies, drop_first=True)"],
        "비고": ["예: gender_Male (여성=0, 남성=1)",
            "예: country_Germany, country_Spain (France는 기준 범주)"],
    }
)
st.dataframe(encoding_df, hide_index=True)

st.markdown(
    """
        <h4 style="font-size: 1.4rem">Data Splitting Strategy</h4>
        <p>
        <ul>
            <li>초기에는 Stratified KFold를 활용한 교차 검증 및 Optuna 튜닝 시도</li>
            <li>데이터(10,000건) 규모 및 튜닝 시간을 고려하여 최종적으로 Hold-out 방식 채택</li>
            <li>Train / Validation / Test = 60% / 15% / 25% (stratify=y)</li>
        </ul>
        </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ============================
# Models
# ============================

st.subheader("Models")
st.markdown(
    """
        <ul>
<li>최종 예측은 <b>SVM + XGBoost Soft Voting 앙상블</b>의 평균 확률값 기반</li>
<li>초기 실험에서는 트리 기반 모델(XGBoost, GBM)이 AUC 기준 가장 우수한 성능을 보여 주요 후보로 선정</li>
<li>불균형 데이터 특성상 XGBoost는 threshold에 따라 Recall이 크게 흔들려 이탈 고객 탐지에 한계가 존재</li>
<li>SVM은 튜닝을 통해 Recall이 크게 향상되었고 확률 보정 후 AUC도 안정적으로 개선</li>
<li>두 모델의 장점을 결합하기 위해 Soft Voting(확률 평균) 앙상블을 최종 모델로 채택</li>
        </ul>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <style>
            .model_box {
                padding: 20px;
                border: 1px solid #666;
                border-radius: 20px;
                margin-bottom: 40px;
            }
        </style>
        <div class="model_box">
            <h4>SVM의 장점</h4>
            <ul>
                <li>커널(RBF)을 통해 비선형 결정 경계 학습 가능</li>
                <li>상대적으로 적은 특성 수에서도 안정적인 성능</li>
                <li>클래스 가중치 설정으로 <b>불균형 데이터 대응</b> 용이</li>
                <li>확률 보정(Calibration) 이후 <b>ROC-AUC가 안정적으로 향상</b></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="model_box">
            <h4>XGBoost의 장점</h4>
            <ul>
                <li>트리 기반 모델 특성상 <b>범주형/수치형 특성을 자유롭게 처리</b></li>
                <li><code>scale_pos_weight</code>를 통한 불균형 데이터 처리</li>
                <li>정규화와 다양한 규제 파라미터로 과적합 제어</li>
                <li>Feature importance 제공으로 <b>모델 해석력</b>이 높음</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
# Optuna로 튜닝된 파라미터 요약 (2nd_project.ipynb 기준)
param_rows = [
    {"모델": "SVM", "파라미터": "kernel", "사용한 값": "rbf"},
    {"모델": "SVM", "파라미터": "gamma", "사용한 값": "0.001"},
    {"모델": "SVM", "파라미터": "C", "사용한 값": "0.1"},
    {"모델": "SVM", "파라미터": "class_weight", "사용한 값": "{0: 1, 1: 5}"},
    {"모델": "XGBoost", "파라미터": "n_estimators", "사용한 값": "310"},
    {"모델": "XGBoost", "파라미터": "max_depth", "사용한 값": "2"},
    {"모델": "XGBoost", "파라미터": "learning_rate", "사용한 값": "0.0845"},
    {"모델": "XGBoost", "파라미터": "min_child_weight", "사용한 값": "26"},
    {"모델": "XGBoost", "파라미터": "gamma", "사용한 값": "0.2252"},
    {"모델": "XGBoost", "파라미터": "subsample", "사용한 값": "0.6674"},
    {"모델": "XGBoost", "파라미터": "colsample_bytree", "사용한 값": "0.6826"},
    {"모델": "XGBoost", "파라미터": "scale_pos_weight", "사용한 값": "9.5372"},
]

parameter_df = pd.DataFrame(param_rows)

# HTML 테이블로 rowspan 적용해서 출력
html = """
<table style="width:100%; border-collapse:collapse;">
    <thead>
        <tr>
            <th style="border:1px solid #ddd; padding:6px;">모델</th>
            <th style="border:1px solid #ddd; padding:6px;">파라미터</th>
            <th style="border:1px solid #ddd; padding:6px;">사용한 값</th>
        </tr>
    </thead>
    <tbody>
"""

for model, subdf in parameter_df.groupby("모델"):
    rowspan = len(subdf)
    first = True
    for _, row in subdf.iterrows():
        html += "<tr>"
        if first:
            html += f'<td rowspan="{rowspan}" style="border:1px solid #ddd; padding:6px; text-align:center;">{model}</td>'
            first = False
        html += f'<td style="border:1px solid #ddd; padding:6px;">{row["파라미터"]}</td>'
        html += f'<td style="border:1px solid #ddd; padding:6px;">{row["사용한 값"]}</td>'
        html += "</tr>\n"

html += """
    </tbody>
</table>
"""

st.markdown(html, unsafe_allow_html=True)


# ============================
# Post processing (Threshold)
# ============================

st.subheader("Post processing")
st.markdown(
    """
    <ul>
        <li> 목표: 이탈 고객을 최대한 놓치지 않는 것이 중요 (Recall 우선)</li>
        <li> Precision이 너무 낮아지지 않도록 관리 (과도한 이탈 분류 방지)</li>
        <li> Validation Set에서 Soft Voting 확률을 기준으로 임계값 탐색 </li>
        <li><b> 최종 임계값 0.50 (Soft Voting Ensemble 기준) </b></li>
    </ul>
    """,
    unsafe_allow_html=True,
)

# ============================
# ROC AUC + Threshold 비교
# ============================

script_dir = Path(__file__).parent

st.subheader("ROC AUC Curve")

st.markdown("아래는 최종 모델의 ROC AUC Curve 입니다.")

script_dir = Path(__file__).parent
img_path = script_dir / "AUC.png"

st.image(img_path, caption="ROC AUC Curve", use_container_width=True)


# ----------------------------
# Threshold 별 지표 계산 함수
# ----------------------------

st.subheader("Threshold Selection")

st.markdown("아래는 최종 모델의 Threshold를 선택하기 위해 확인한 그래프입니다.")

script_dir = Path(__file__).parent
img_path_2 = script_dir / "threshold.png"

st.image(img_path_2, caption="Threshold", use_container_width=True)

st.divider()

# ============================
# 최종 성능 요약
# ============================
st.subheader("최종 성능 요약")

# 👉 여기서 final_metrics DataFrame을 직접 만든다
final_metrics = pd.DataFrame(
    {
        "Metric": ["ROC-AUC", "Accuracy", "Precision", "Recall", "F1-Score"],
        "Score": [0.83, 0.80, 0.44, 0.76, 0.56], 
    }
)

st.dataframe(final_metrics, hide_index=True)

script_dir = Path(__file__).parent
img_path_3 = script_dir / "shap.png"

st.image(img_path_3, caption="전체 Feature 영향도 분포", use_container_width=True)



script_dir = Path(__file__).parent
img_path_4 = script_dir / "age_shap.png"

st.image(img_path_4, caption="나이(age)에 따른 이탈위험 영향(Dependence Plot)", use_container_width=True)



st.divider()
