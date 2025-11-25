(function () {
  // Utility: generate UUID v4
  function uuidv4() {
    // Simple UUID generator for demo purposes
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }

  // ----- Data Model -----
  class Task {
    constructor({ id = uuidv4(), text, completed = false, createdAt = Date.now() } = {}) {
      this.id = id;
      this.text = text;
      this.completed = completed;
      this.createdAt = createdAt;
    }

    static fromObject(obj) {
      return new Task({
        id: obj.id,
        text: obj.text,
        completed: obj.completed,
        createdAt: obj.createdAt,
      });
    }
  }

  // In‑memory store
  let tasks = [];
  let currentFilter = 'all'; // all | active | completed
  let draggedTaskId = null;
  let focusedTaskId = null; // for keyboard move shortcuts

  // ----- Persistence -----
  const STORAGE_KEY = 'colorfulTodoTasks';
  const DARK_MODE_KEY = 'colorfulTodoDarkMode';

  function loadTasks() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      try {
        const arr = JSON.parse(raw);
        tasks = arr.map(obj => Task.fromObject(obj));
      } catch (e) {
        console.error('Failed to parse tasks from localStorage', e);
        tasks = [];
      }
    } else {
      tasks = [];
    }
  }

  function saveTasks() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  }

  // ----- UI Rendering -----
  const taskListEl = document.getElementById('taskList');
  if (taskListEl) taskListEl.setAttribute('role', 'list');

  function createTaskElement(task) {
    const li = document.createElement('li');
    li.className = 'task-item';
    li.dataset.id = task.id;
    li.setAttribute('role', 'listitem');
    li.setAttribute('draggable', 'true');
    li.setAttribute('tabindex', '0'); // make focusable

    // Checkbox
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'toggle';
    checkbox.setAttribute('aria-label', 'Mark as completed');
    checkbox.checked = task.completed;
    checkbox.setAttribute('aria-checked', task.completed);
    checkbox.addEventListener('change', () => toggleTask(task.id));

    // Text span
    const span = document.createElement('span');
    span.className = 'task-text';
    span.textContent = task.text;

    // Edit button
    const editBtn = document.createElement('button');
    editBtn.className = 'edit';
    editBtn.setAttribute('aria-label', 'Edit task');
    editBtn.textContent = '✎';
    editBtn.addEventListener('click', () => {
      const newText = prompt('Edit task', task.text);
      if (newText !== null) {
        editTask(task.id, newText.trim());
      }
    });

    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete';
    deleteBtn.setAttribute('aria-label', 'Delete task');
    deleteBtn.textContent = '✖';
    deleteBtn.addEventListener('click', () => deleteTask(task.id));

    // Drag‑and‑Drop handlers
    li.addEventListener('dragstart', e => {
      draggedTaskId = task.id;
      e.dataTransfer.effectAllowed = 'move';
      // For Firefox compatibility
      e.dataTransfer.setData('text/plain', task.id);
    });
    li.addEventListener('dragend', () => {
      draggedTaskId = null;
      // Remove any placeholder styling
      const placeholders = taskListEl.querySelectorAll('.drag-over');
      placeholders.forEach(p => p.classList.remove('drag-over'));
    });
    li.addEventListener('dragover', e => {
      e.preventDefault(); // allow drop
      e.dataTransfer.dropEffect = 'move';
      li.classList.add('drag-over');
    });
    li.addEventListener('dragleave', () => {
      li.classList.remove('drag-over');
    });
    li.addEventListener('drop', e => {
      e.preventDefault();
      li.classList.remove('drag-over');
      const targetId = li.dataset.id;
      if (!draggedTaskId || draggedTaskId === targetId) return;
      const fromIdx = tasks.findIndex(t => t.id === draggedTaskId);
      const toIdx = tasks.findIndex(t => t.id === targetId);
      if (fromIdx === -1 || toIdx === -1) return;
      // Reorder array
      const [moved] = tasks.splice(fromIdx, 1);
      // Insert before the target index (if moving down, adjust index after removal)
      const insertIdx = fromIdx < toIdx ? toIdx : toIdx;
      tasks.splice(insertIdx, 0, moved);
      saveTasks();
      renderTasks(currentFilter);
    });

    // Focus handling for keyboard move shortcuts
    li.addEventListener('focus', () => {
      focusedTaskId = task.id;
    });
    li.addEventListener('blur', () => {
      if (focusedTaskId === task.id) focusedTaskId = null;
    });

    // Assemble
    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(editBtn);
    li.appendChild(deleteBtn);
    return li;
  }

  function renderTasks(filter = 'all') {
    currentFilter = filter;
    // Clear list
    while (taskListEl.firstChild) {
      taskListEl.removeChild(taskListEl.firstChild);
    }
    const filtered = tasks.filter(task => {
      if (filter === 'active') return !task.completed;
      if (filter === 'completed') return task.completed;
      return true; // all
    });
    filtered.forEach(task => {
      const li = createTaskElement(task);
      taskListEl.appendChild(li);
    });
  }

  // ----- CRUD Operations -----
  function addTask(text) {
    if (!text) return;
    const task = new Task({ text: text.trim() });
    tasks.push(task);
    saveTasks();
    renderTasks(currentFilter);
    // Focus the newly added task
    const newLi = taskListEl.querySelector(`li[data-id="${task.id}"]`);
    if (newLi) newLi.focus();
  }

  function editTask(id, newText) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    task.text = newText;
    saveTasks();
    renderTasks(currentFilter);
  }

  function deleteTask(id) {
    const idx = tasks.findIndex(t => t.id === id);
    if (idx === -1) return;
    tasks.splice(idx, 1);
    saveTasks();
    renderTasks(currentFilter);
    // After deletion, focus next sibling if exists
    const nextLi = taskListEl.children[idx] || taskListEl.lastElementChild;
    if (nextLi) nextLi.focus();
  }

  function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    task.completed = !task.completed;
    saveTasks();
    renderTasks(currentFilter);
  }

  // ----- Input Handling -----
  const newTaskInput = document.getElementById('newTaskInput');
  if (newTaskInput) {
    newTaskInput.addEventListener('keydown', e => {
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey || !e.ctrlKey)) {
        // Ctrl+Enter also adds; plain Enter adds as well
        const value = newTaskInput.value.trim();
        if (value) {
          addTask(value);
          newTaskInput.value = '';
        }
        e.preventDefault();
      }
    });
  }

  // ----- Filtering -----
  const filterAllBtn = document.getElementById('filterAll');
  const filterActiveBtn = document.getElementById('filterActive');
  const filterCompletedBtn = document.getElementById('filterCompleted');

  if (filterAllBtn) filterAllBtn.addEventListener('click', () => renderTasks('all'));
  if (filterActiveBtn) filterActiveBtn.addEventListener('click', () => renderTasks('active'));
  if (filterCompletedBtn) filterCompletedBtn.addEventListener('click', () => renderTasks('completed'));

  // ----- Clear Completed -----
  const clearCompletedBtn = document.getElementById('clearCompleted');
  if (clearCompletedBtn) {
    clearCompletedBtn.addEventListener('click', () => {
      tasks = tasks.filter(t => !t.completed);
      saveTasks();
      renderTasks(currentFilter);
    });
  }

  // ----- Dark Mode Toggle -----
  const darkModeToggleBtn = document.getElementById('darkModeToggle');
  function applyDarkMode(enabled) {
    if (enabled) {
      document.documentElement.classList.add('dark-mode');
    } else {
      document.documentElement.classList.remove('dark-mode');
    }
    localStorage.setItem(DARK_MODE_KEY, enabled ? '1' : '0');
  }
  if (darkModeToggleBtn) {
    darkModeToggleBtn.addEventListener('click', () => {
      const currently = document.documentElement.classList.contains('dark-mode');
      applyDarkMode(!currently);
    });
  }
  // Apply persisted dark mode on load
  const darkModePersisted = localStorage.getItem(DARK_MODE_KEY);
  if (darkModePersisted === '1') applyDarkMode(true);

  // ----- Global Keyboard Shortcuts -----
  document.addEventListener('keydown', e => {
    // Ctrl+Shift+L => toggle dark mode
    if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'l') {
      const currently = document.documentElement.classList.contains('dark-mode');
      applyDarkMode(!currently);
      e.preventDefault();
    }
    // Alt+ArrowUp / Alt+ArrowDown => move focused task
    if (e.altKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
      if (!focusedTaskId) return;
      const idx = tasks.findIndex(t => t.id === focusedTaskId);
      if (idx === -1) return;
      const newIdx = e.key === 'ArrowUp' ? idx - 1 : idx + 1;
      if (newIdx < 0 || newIdx >= tasks.length) return;
      // Swap positions
      const temp = tasks[idx];
      tasks[idx] = tasks[newIdx];
      tasks[newIdx] = temp;
      saveTasks();
      renderTasks(currentFilter);
      // Restore focus on moved element
      setTimeout(() => {
        const li = taskListEl.querySelector(`li[data-id="${focusedTaskId}"]`);
        if (li) li.focus();
      }, 0);
      e.preventDefault();
    }
  });

  // ----- Initialization -----
  loadTasks();
  renderTasks();

  // ----- Export for Testing -----
  window.TodoApp = {
    addTask,
    editTask,
    deleteTask,
    toggleTask,
    tasks: () => tasks.slice(), // expose copy
    renderTasks,
    loadTasks,
    saveTasks,
    // expose internal helpers for potential tests
    _private: {
      Task,
      uuidv4,
    },
  };
})();
