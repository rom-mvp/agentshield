set -euo pipefail

rm -rf layer psycopg2 psycopg2_binary-* psycopg2_binary.libs psycopg2-layer.zip
python3.9 -m pip install psycopg2-binary -t .
mkdir -p layer/python
cp -r psycopg2 psycopg2_binary-* psycopg2_binary.libs layer/python/ || true
( cd layer && zip -r ../psycopg2-layer.zip python )
