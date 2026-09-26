import glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')

files = glob.glob('lecture/*.html')
print(f'Checking {len(files)} files...')

total_errors = 0

# Check digital.hec.ca link
p1 = open('lecture/partie-1.html', encoding='utf-8').read()
if 'digital.hec.ca' in p1:
    m = re.search(r'<a href="https://digital\.hec\.ca/blog/ciblage-publicitaire-meta-intelligence-artificielle" target="_blank" rel="noopener noreferrer">[^<]+</a>', p1)
    if m:
        print('✅ digital.hec.ca properly linkified:', m.group(0)[:90])
    else:
        print('❌ digital.hec.ca not properly linkified!')
        total_errors += 1
else:
    print('❌ digital.hec.ca not found!')
    total_errors += 1

# Check broken words
for f in files:
    content = open(f, encoding='utf-8').read()
    for bad in ['transitio n', 'sa tisfaction', 'entr aînement', 'l \'apprentissage', 'e t répétitives', 'c \'est']:
        if bad in content:
            print(f'❌ Broken word "{bad}" in {f}!')
            total_errors += 1

# Check figures
for num in range(1, 13):
    found = False
    for f in files:
        if f'id="fig-{num}"' in open(f, encoding='utf-8').read():
            found = True
            break
    if not found:
        print(f'❌ Figure {num} missing!')
        total_errors += 1
    else:
        print(f'✅ Figure {num} found!')

# Check SVG book icon
for f in files:
    content = open(f, encoding='utf-8').read()
    if 'd="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"' not in content:
        print(f'❌ Book icon missing in {f}!')
        total_errors += 1

# Check Synthèse éditoriale
for f in files:
    content = open(f, encoding='utf-8').read()
    if 'Synthèse éditoriale à valider' in content:
        print(f'❌ "Synthèse éditoriale à valider" found in {f}!')
        total_errors += 1

if total_errors == 0:
    print('\n🎉 ALL CHECKS PASSED WITH 0 ERRORS!')
else:
    print(f'\n⚠️ Total errors: {total_errors}')
