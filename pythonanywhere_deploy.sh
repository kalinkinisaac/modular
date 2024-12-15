/usr/local/bin/python3.10 -m venv venv
source venv/bin/activate
while IFS= read -r line; do echo "$line" && pip install "$line"  --no-cache-dir; done < requirements_webserver.txt