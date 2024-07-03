import json
from uuid import uuid4 as uuid
from datetime import datetime

def create_file(content, source):
    timestamp = datetime.now().isoformat()
    metadata = {
        'timestamp': timestamp,
        'source': source
        }
    file_content = {
        'metadata': metadata,
        'content': content
    }
    file_name = f'{timestamp}_{source}_{uuid()}.json'
    with open(file_name, 'w') as f:
        f.write(json.dumps(file_content))