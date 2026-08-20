#!/usr/bin/env bash
# [강제/PreToolUse] .env 계열 파일의 편집·생성을 차단한다.
#
# 동작: Claude 가 Edit/Write 를 시도하면 이 스크립트가 먼저 실행된다.
#   - stdin 으로 도구 호출 정보(JSON)가 들어온다.
#   - 대상 파일이 .env 를 포함하면 exit 2 로 차단하고, stderr 메시지를 Claude 에 전달.
#   - 그 외에는 exit 0 으로 통과.
#
# 검증:
#   Claude 에게 "src/.env 에 API_KEY=test 추가해줘" → 차단돼야 정상.
set -euo pipefail

input=$(cat)
# jq 가 있으면 정확히 파싱, 없으면 grep 폴백
if command -v jq >/dev/null 2>&1; then
  file=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty')
else
  file=$(printf '%s' "$input" | grep -oE '"(file_path|path)"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*:"([^"]*)"/\1/')
fi

case "$file" in
  *.env|*.env.*|*/.env|*/.env.*)
    echo "차단: '$file' 는 .env 계열이라 hook 으로 편집이 금지돼 있습니다. 값이 필요하면 사용자에게 요청하세요." >&2
    exit 2
    ;;
esac
exit 0
