import email, sys
from email import policy
sys.stdout.reconfigure(encoding='utf-8')

with open(r'scratch_cover/Mémoire - ALMODOVAR Thomas.mht', 'rb') as f:
    msg = email.message_from_binary_file(f, policy=policy.default)

part0 = next(msg.iter_parts())
payload = part0.get_payload(decode=True)
charset = part0.get_content_charset() or 'utf-8'
print(f"Charset: {charset}, Raw length: {len(payload)}")

# Try decoding
try:
    html_text = payload.decode(charset)
except Exception as e:
    print(f"Decode error with {charset}: {e}, falling back to windows-1252 with replace")
    html_text = payload.decode('windows-1252', errors='replace')

with open('scratch_cover/memoire_extracted.html', 'w', encoding='utf-8') as f:
    f.write(html_text)

print(f"Saved memoire_extracted.html ({len(html_text)} chars)")
