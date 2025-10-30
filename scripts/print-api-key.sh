set -euo pipefail
STAGE="${1:-dev}"
NAME="agentshield-proxy-${STAGE}-key"
aws apigateway get-api-keys \
  --name-query "$NAME" --include-values --region us-east-2 \
  | jq -r '.items[0].value'
