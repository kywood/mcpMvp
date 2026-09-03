# mcpMvp
mcpMvp





docker network create mcpmvp_net 





2026-09.02
 - airflow 까진 셋함.


== 이걸로 일단은 LLM 까진 올림 ===
docker exec -it llm-ollama-1 bash
ollama pull qwen2.5:7b-instruct-q4_K_M
cd /llm-config && ollama create airflow-sre -f Modelfile
ollama run airflow-sre



