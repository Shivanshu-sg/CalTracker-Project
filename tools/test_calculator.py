import json
from math import isclose

ING_PATH = 'static/data/ingredients.json'

with open(ING_PATH, 'r', encoding='utf-8') as f:
    ingredients = json.load(f)

id_map = {i['id']: i for i in ingredients}

# sample test cases: list of ([(id, grams), ...], expected_total)
cases = [
    ([('chicken_breast', 100)], 165),
    ([('white_rice', 200), ('chicken_breast',150)], (130*2)+(165*1.5)),
    ([('olive_oil', 10)], 88.4),
    ([('banana', 118)], 89*1.18),
]

print('Running calculator tests...')
for idx, (items, expected) in enumerate(cases, 1):
    total = 0
    for ident, grams in items:
        item = id_map.get(ident)
        if not item:
            raise AssertionError(f'missing ingredient {ident}')
        total += (grams/100.0) * item['kcal_per_100g']
    ok = isclose(total, expected, rel_tol=1e-3)
    print(f'Test {idx}: computed {total:.3f} kcal, expected {expected:.3f} ->', 'PASS' if ok else 'FAIL')
    if not ok:
        raise SystemExit(1)
print('All tests passed.')
