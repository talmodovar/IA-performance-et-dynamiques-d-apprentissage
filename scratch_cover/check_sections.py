import json

with open('scratch_cover/sections_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for sec in data:
    sec_id = sec['id']
    sec_title = sec['title']
    print(f"=== {sec_id} ({sec_title}) ===")
    lines = [l.strip() for l in sec['raw_text'].split('\n') if l.strip() and not l.startswith('<!--')]
    print("  Line count:", len(lines))
    print("  First lines:", lines[:3])
    print("  Last lines:", lines[-2:])
