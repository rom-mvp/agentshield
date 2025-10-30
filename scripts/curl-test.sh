set -euo pipefail
STAGE="${1:-dev}"
BASE="https://<your-gateway-id>.execute-api.us-east-2.amazonaws.com"
URL="$BASE/$STAGE/proxy/test"
API_KEY="${API_KEY:-}"
EXTRA=()
[ -n "$API_KEY" ] && EXTRA+=( -H "x-api-key: $API_KEY" )

curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: cli-test" \
  "${EXTRA[@]}" \
  -d '{"email":"foo@example.com"}' | jq .
