(() => {
  const data = window.__IDEAS__ || [];
  const stats = window.__STATS__ || { total: data.length, expanded: data.length };
  const grid = document.querySelector('#idea-grid');
  if (!grid) return;

  const searchInput = document.querySelector('#filter-search');
  const groupSelect = document.querySelector('#filter-group');
  const phaseSelect = document.querySelector('#filter-phase');
  const statusSelect = document.querySelector('#filter-status');
  const kindSelect = document.querySelector('#filter-kind');
  const expandedCountEl = document.querySelector('#expanded-count');
  const totalCountEl = document.querySelector('#total-count');
  const filterCountEl = document.querySelector('#filter-count');

  const buildOptions = (select, values, label) => {
    const unique = [...new Set(values.filter(Boolean))].sort();
    select.innerHTML = '';
    const defaultOption = document.createElement('option');
    defaultOption.value = 'all';
    defaultOption.textContent = label;
    select.appendChild(defaultOption);
    unique.forEach((value) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
  };

  buildOptions(groupSelect, data.map((item) => item.group), '全部分组');
  buildOptions(phaseSelect, data.map((item) => item.phase), '全部阶段');
  buildOptions(kindSelect, data.map((item) => item.kind), '全部类型');
  buildOptions(statusSelect, data.map((item) => item.status), '全部状态');

  const state = {
    query: '',
    group: 'all',
    phase: 'all',
    kind: 'all',
    status: 'all',
  };

  const matches = (item) => {
    const text = `${item.title} ${item.summary || ''} ${item.group || ''}`.toLowerCase();
    const query = state.query.trim().toLowerCase();
    if (query && !text.includes(query)) return false;
    if (state.group !== 'all' && item.group !== state.group) return false;
    if (state.phase !== 'all' && item.phase !== state.phase) return false;
    if (state.kind !== 'all' && item.kind !== state.kind) return false;
    if (state.status !== 'all' && item.status !== state.status) return false;
    return true;
  };

  const render = () => {
    const filtered = data.filter(matches);
    grid.innerHTML = '';
    if (expandedCountEl) expandedCountEl.textContent = String(stats.expanded || 0);
    if (totalCountEl) totalCountEl.textContent = String(stats.total || data.length);
    if (filterCountEl) filterCountEl.textContent = `当前筛选：${filtered.length}`;

    if (!filtered.length) {
      grid.innerHTML = '<div class="empty-state">没有匹配的 idea，请调整筛选条件。</div>';
      return;
    }

    filtered.forEach((item, index) => {
      const card = document.createElement(item.status === 'draft' ? 'div' : 'a');
      card.className = 'idea-card';
      card.style.setProperty('--delay', `${Math.min(index * 0.04, 0.6)}s`);
      if (item.status !== 'draft') {
        card.href = `ideas/${item.slug}.html`;
      }

      const idChip = `<span class="chip accent">#${item.id}</span>`;
      const groupChip = item.group ? `<span class="chip teal">${item.group}</span>` : '';
      const statusChip = item.status === 'draft'
        ? '<span class="chip blue">待扩展</span>'
        : '<span class="chip">已扩展</span>';

      const summary = item.summary || item.concept || '暂无描述。';
      const phase = item.phase ? `<span>${item.phase}</span>` : '';
      const statusLabel = item.status === 'draft' ? '待扩展' : '已扩展';

      card.innerHTML = `
        <div class="card-top">
          ${idChip}
          ${groupChip}
          ${statusChip}
        </div>
        <h3>${item.title}</h3>
        <p>${summary}</p>
        <div class="card-meta">
          ${phase}
          <span class="${item.status === 'draft' ? 'status-draft' : 'status-expanded'}">${statusLabel}</span>
        </div>
      `;
      grid.appendChild(card);
    });
  };

  const updateState = (key, value) => {
    state[key] = value;
    render();
  };

  searchInput.addEventListener('input', (event) => updateState('query', event.target.value));
  groupSelect.addEventListener('change', (event) => updateState('group', event.target.value));
  phaseSelect.addEventListener('change', (event) => updateState('phase', event.target.value));
  kindSelect.addEventListener('change', (event) => updateState('kind', event.target.value));
  statusSelect.addEventListener('change', (event) => updateState('status', event.target.value));

  render();
})();
