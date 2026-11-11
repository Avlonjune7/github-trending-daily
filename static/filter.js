const input = document.querySelector('#search');
if (input) {
  const list = document.querySelector('#projects');
  const cards = [...list.querySelectorAll('[data-project]')];
  const language = document.querySelector('#language');
  const category = document.querySelector('#category');
  const sort = document.querySelector('#sort');
  const reset = document.querySelector('#reset-filters');
  const fields = { q: input, language, category, sort };
  const restore = () => {
    const params = new URLSearchParams(location.search);
    for (const [key, field] of Object.entries(fields)) {
      const value = params.get(key) || (key === 'sort' ? 'rank' : '');
      field.value = value;
      if (field.tagName === 'SELECT' && field.selectedIndex < 0) {
        field.value = key === 'sort' ? 'rank' : '';
      }
    }
  };
  const filter = (syncURL = true) => {
    const query = input.value.trim().toLocaleLowerCase();
    let visible = 0;
    const ordered = [...cards].sort((a, b) => {
      if (sort.value === 'stars') return Number(b.dataset.stars) - Number(a.dataset.stars) || Number(a.dataset.rank) - Number(b.dataset.rank);
      if (sort.value === 'name') return a.dataset.name.localeCompare(b.dataset.name);
      return Number(a.dataset.rank) - Number(b.dataset.rank);
    });
    for (const card of ordered) {
      card.hidden = !card.dataset.search.toLocaleLowerCase().includes(query)
        || (language.value !== '' && card.dataset.language !== language.value)
        || (category.value !== '' && card.dataset.category !== category.value);
      if (!card.hidden) visible++;
      list.append(card);
    }
    document.querySelector('#count').textContent = visible === cards.length ? `${visible} 个项目` : `${visible} / ${cards.length} 个项目`;
    document.querySelector('#empty').hidden = visible !== 0;
    document.querySelector('.ranking-table').hidden = visible === 0;
    reset.hidden = !query && !language.value && !category.value && sort.value === 'rank';
    if (syncURL) {
      const url = new URL(location.href);
      for (const [key, field] of Object.entries(fields)) {
        if (field.value && !(key === 'sort' && field.value === 'rank')) url.searchParams.set(key, field.value);
        else url.searchParams.delete(key);
      }
      history.replaceState(null, '', url);
    }
  };
  const clear = () => {
    input.value = language.value = category.value = '';
    sort.value = 'rank';
    filter();
    input.focus();
  };
  input.addEventListener('input', () => filter());
  for (const select of [language, category, sort]) select.addEventListener('change', () => filter());
  reset.addEventListener('click', clear);
  document.querySelector('#clear-search').addEventListener('click', clear);
  window.addEventListener('popstate', () => { restore(); filter(false); });
  restore();
  filter(false);
}

// Keep the owner's initial visible if GitHub's avatar CDN is unavailable.
for (const avatar of document.querySelectorAll('.repo-avatar img')) {
  avatar.addEventListener('error', () => { avatar.hidden = true; });
  if (avatar.complete && !avatar.naturalWidth) avatar.hidden = true;
}

// Native dialog supplies modal focus containment and Escape handling.
const projectRows = document.querySelectorAll('[data-project]');
if (projectRows.length && typeof HTMLDialogElement !== 'undefined') {
  const dialog = document.createElement('dialog');
  dialog.className = 'project-dialog';
  dialog.setAttribute('aria-labelledby', 'project-dialog-title');
  dialog.innerHTML = '<header class="dialog-header"><div><p class="eyebrow">项目详情</p><h2 id="project-dialog-title"></h2><p class="dialog-meta"></p></div><button class="dialog-close" type="button" aria-label="关闭项目详情" autofocus>×</button></header><div class="dialog-body"></div><footer class="dialog-footer"><a class="dialog-repo" href="#">在 GitHub 查看 ↗</a><button class="dialog-done" type="button">关闭</button></footer>';
  document.body.append(dialog);
  let opener;
  const close = () => dialog.close();
  dialog.querySelector('.dialog-close').addEventListener('click', close);
  dialog.querySelector('.dialog-done').addEventListener('click', close);
  let backdropDown = false;
  const outside = event => {
    const rect = dialog.getBoundingClientRect();
    return event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom;
  };
  dialog.addEventListener('pointerdown', event => { backdropDown = outside(event); });
  dialog.addEventListener('click', event => { if (backdropDown && outside(event)) close(); backdropDown = false; });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('dialog-open');
    opener?.focus({ preventScroll: true });
  });
  for (const row of projectRows) {
    const details = row.querySelector('.project-details');
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'project-dialog-trigger';
    button.textContent = '了解项目 ↗';
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-label', `了解项目 ${row.dataset.name}`);
    details.before(button);
    details.hidden = true;
    button.addEventListener('click', () => {
      opener = button;
      dialog.querySelector('#project-dialog-title').textContent = row.dataset.name;
      dialog.querySelector('.dialog-meta').textContent = `官方排名 #${row.dataset.rank} · 本期增星 +${Number(row.dataset.stars).toLocaleString()}`;
      const body = dialog.querySelector('.dialog-body');
      body.replaceChildren();
      const heading = document.createElement('h3');
      heading.textContent = '项目概况';
      const description = document.createElement('p');
      description.className = 'dialog-description';
      description.textContent = details.querySelector('.project-overview-section dd')?.textContent || row.querySelector('.project-description').textContent;
      const metrics = row.querySelector('.project-metrics').cloneNode(true);
      metrics.className = 'dialog-metrics';
      metrics.querySelectorAll('[data-label]').forEach(metric => {
        const label = document.createElement('span');
        label.className = 'dialog-metric-label';
        label.textContent = metric.dataset.label;
        metric.prepend(label);
      });
      const panel = details.querySelector('.project-detail-panel').cloneNode(true);
      panel.querySelector('.detail-source')?.remove();
      panel.querySelector('.project-overview-section')?.remove();
      body.append(heading, description, metrics, panel);
      dialog.querySelector('.dialog-repo').href = row.querySelector('.repo').href;
      dialog.showModal();
      document.documentElement.classList.add('dialog-open');
      body.scrollTop = 0;
    });
  }
}
