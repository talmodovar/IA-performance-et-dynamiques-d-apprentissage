import json

with open('scratch_cover/sections_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for sec in data[:2]:
    text = sec['raw_text']
    # Check for accents
    has_e_aigu = 'é' in text
    has_apostrophe = '’' in text or "'" in text
    print(f"{sec['id']}: has 'é' -> {has_e_aigu}, sample: {text[50:180]}")
