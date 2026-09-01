# LLM 모델 관리 이력

## 현재 사용 모델

| 커스텀 모델명 | 베이스 모델 | 용도 | 등록일 |
|---|---|---|---|
| airflow-analyst | qwen2.5:7b-instruct-q4_K_M | Airflow 실패 원인 분석 | 2026-09-02 |

## 선택 배경

- **하드웨어**: RTX 4060, VRAM 8GB (Xwayland 상시 점유 ~1GB 감안 시 실사용 ~7GB)
- **베이스 모델 선정 이유**: Qwen2.5-7B가 7~8B급 중 툴콜링/구조화된 지시 따르기에 강함.
  4bit 양자화(q4_K_M) 시 가중치 약 4.7GB로 VRAM 예산 내 안전하게 적재됨.
- **후보였으나 보류**: Qwen2.5-Coder-7B (로그/코드 분석 특화, 정확도 아쉬우면 전환 검토)
- **제외**: Qwen3-27B (VRAM 8GB로는 4bit여도 불가능, 최소 13~15GB 필요)

## 변경 이력

### 2026-09-02
- `airflow-analyst` 최초 생성
- 베이스: qwen2.5:7b-instruct-q4_K_M
- system prompt: Airflow 실패 분석 역할 부여, temperature 0.3, num_ctx 8192
- 변경 사유: MVP 초기 구성

## 향후 검토 사항

- MCP 도구 목록 확정 후 SYSTEM 프롬프트에 실제 도구명/스펙 반영 필요
- RAG 연동 후 컨텍스트 길이(num_ctx) 재검토 필요할 수 있음
- Ollama → vLLM 전환 시 파라미터(temperature, top_p 등) 재검증 필요