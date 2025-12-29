async function loadIngredients() {
  const path = '/static/data/ingredients.json';
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error('Failed to load ingredients (' + res.status + ')');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('Could not load ingredients:', err);
    return [];
  }
}

function createRow(ingredients) {
  const row = document.createElement('div');
  row.className = 'row';
  row.style.marginTop = '10px';

  const select = document.createElement('select');
  select.className = 'select-ingredient';
  select.style.minWidth = '0';
  select.style.flex = '1';
  ingredients.forEach(i => {
    const opt = document.createElement('option');
    opt.value = i.id;
    opt.textContent = `${i.name} (${i.kcal_per_100g} kcal/100g)`;
    select.appendChild(opt);
  });

  const input = document.createElement('input');
  input.type = 'number';
  input.placeholder = 'grams';
  input.min = '0';
  input.value = '100';
  input.className = 'input-grams';

  const remove = document.createElement('button');
  remove.type = 'button';
  remove.textContent = 'Remove';
  remove.className = 'btn-remove';
  remove.style.marginLeft = '8px';
  remove.onclick = () => row.remove();

  row.appendChild(select);
  row.appendChild(input);
  row.appendChild(remove);
  return row;
}

async function setup() {
  const ingredients = await loadIngredients();
  const list = document.getElementById('ingredients-list');
  const addBtn = document.getElementById('add-ingredient');
  const calcBtn = document.getElementById('calculate');
  const resultBox = document.getElementById('result');

  // start with two rows
  list.appendChild(createRow(ingredients));
  list.appendChild(createRow(ingredients));

  addBtn.onclick = () => list.appendChild(createRow(ingredients));

  calcBtn.onclick = () => {
    const rows = Array.from(list.querySelectorAll('.row'));
    let totalKcal = 0;
    const breakdown = [];
    rows.forEach(r => {
      const sel = r.querySelector('.select-ingredient') || r.querySelector('select');
      const gramsEl = r.querySelector('.input-grams') || r.querySelector('input');
      const grams = parseFloat(gramsEl.value) || 0;
      const item = ingredients.find(it => it.id === sel.value);
      if (item && grams > 0) {
        const kcal = (grams / 100) * item.kcal_per_100g;
        totalKcal += kcal;
        breakdown.push({ name: item.name, grams, kcal: Math.round(kcal) });
      }
    });

    resultBox.innerHTML = '';
    const h = document.createElement('h3');
    h.textContent = `Estimated calories: ${Math.round(totalKcal)} kcal`;
    resultBox.appendChild(h);

    const ul = document.createElement('ul');
    breakdown.forEach(b => {
      const li = document.createElement('li');
      li.textContent = `${b.name}: ${b.grams} g → ${b.kcal} kcal`;
      ul.appendChild(li);
    });
    resultBox.appendChild(ul);
  };
}

window.addEventListener('DOMContentLoaded', setup);