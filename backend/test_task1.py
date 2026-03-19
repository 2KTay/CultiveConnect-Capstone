import json

with open('data/regulations.json') as f:
    data = json.load(f)

print('=== TASK 1 VALIDATION ===')
print()

required_fields = ['base_duty', 'seasonal_adjustment', 'required_docs']
passed = 0
failed = 0

for country in ['USA', 'Canada']:
    print(f'--- {country} ---')
    for product, pdata in data[country].items():
        hts = pdata.get('hts_code', pdata.get('hs_code', 'MISSING'))
        issues = []
        for field in required_fields:
            if field not in pdata:
                issues.append(f'{field} MISSING')
        if issues:
            print(f'  FAIL {product}: {issues}')
            failed += 1
        else:
            seasonal = pdata['seasonal_adjustment']['applies']
            docs = pdata['required_docs']
            duty = pdata['base_duty']
            print(f'  PASS {product}')
            print(f'       hts={hts}')
            print(f'       duty={duty}')
            print(f'       seasonal={seasonal}')
            print(f'       docs={docs}')
            passed += 1
    print()

print(f'Result: {passed} passed, {failed} failed')
if failed == 0:
    print('Task 1 COMPLETE - regulations.json is valid')
else:
    print('Task 1 INCOMPLETE - fix the issues above')