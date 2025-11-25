# ColorfulTodo 🌈 (its generated via Cantata)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](#)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)](#)

---

## 📖 Overview
**ColorfulTodo** is a lightweight, browser‑only todo‑list application that lets you manage tasks with a splash of color.  It runs entirely on the client side – no server, no build step, just open `index.html` and start adding, dragging, and completing tasks.  Dark‑mode support and drag‑and‑drop reordering are built‑in, making the experience both pleasant and functional.

---

## 🛠️ Tech Stack
- **HTML5** – structure and markup
- **CSS3** – styling, responsive layout, dark‑mode via CSS variables
- **Vanilla JavaScript (ES6+)** – core logic, localStorage persistence, drag‑and‑drop API
- **Assets** – simple SVG icons and optional background images stored in `assets/`

---

## ✨ Features (as per project plan)
- **Add / Edit / Delete tasks** – quick inline editing.
- **Color tagging** – assign a color label to each task for visual grouping.
- **Dark‑mode** – automatically follows the OS preference; toggle available.
- **Drag‑and‑drop reordering** – intuitive rearrangement using the native HTML5 DnD API.
- **Persistence** – tasks are saved in `localStorage` and restored on page load.
- **Responsive design** – works on desktop and mobile browsers.

---

## 📦 Installation & Usage
The app has **zero dependencies** and does **not** require any build tools.

```bash
# 1. Clone the repository
git clone https://github.com/your‑username/colorfultodo.git
cd colorfultodo

# 2. Open the app in a browser (no npm install, no bundler)
#    You can double‑click `index.html` or run:
open index.html   # macOS
# or
xdg-open index.html   # Linux
# or simply drag the file into any modern browser.
```

Once opened, you can start adding tasks immediately.  All data is stored locally in the browser’s `localStorage`.

---

## 📁 Folder Structure
```
colorfultodo/
├─ index.html          # Main entry point – loads CSS & JS
├─ styles.css          # Global styles, dark‑mode variables, layout
├─ app.js              # Core application logic (task CRUD, DnD, storage)
├─ assets/             # Images, icons, favicons
│   └─ ...
└─ README.md           # You are reading it right now!
```

- **index.html** – minimal markup that references `styles.css` and `app.js`.
- **styles.css** – contains CSS custom properties for light/dark themes, task card styling, and responsive rules.
- **app.js** – a single‑module script that:
  1. Loads tasks from `localStorage`.
  2. Renders them into the DOM.
  3. Handles UI events (add, edit, delete, color change).
  4. Implements drag‑and‑drop using the native `dragstart`, `dragover`, `drop`, etc.
  5. Persists any change back to `localStorage`.
- **assets/** – optional static files (e.g., a logo SVG, background patterns).

---

## 🛠️ Development Notes
### Task Storage
- Tasks are stored as an array of objects in `localStorage` under the key `colorfulTodoTasks`.
- Each task object shape:
  ```js
  {
    id: "uuid-or-timestamp",
    text: "Buy groceries",
    color: "#ff6b6b", // hex string
    completed: false,
    order: 0 // numeric index for sorting
  }
  ```
- On every mutation (add, edit, delete, reorder, toggle complete) the array is serialized with `JSON.stringify` and saved.

### Dark‑Mode Implementation
- CSS variables (`--bg`, `--text`, `--card-bg`, etc.) are defined for both light and dark themes.
- The `prefers-color-scheme` media query sets the default theme.
- A tiny toggle button in the UI adds/removes a `data-theme="dark"` attribute on `<html>` to override the OS setting.

### Drag‑and‑Drop Logic
1. **dragstart** – store the dragged task’s `id` in `event.dataTransfer`.
2. **dragover** – prevent default to allow dropping and add a visual placeholder.
3. **drop** – retrieve the dragged `id`, compute the new index based on the drop target, update the `order` property of all affected tasks, re‑render, and persist.
4. Accessibility – `draggable="true"` is set on each task card, and ARIA attributes (`aria-grabbed`) are updated for screen readers.

---

## 🤝 Contribution Guidelines
1. **Fork** the repository.
2. **Create a branch** for your feature or bug‑fix:
   ```bash
   git checkout -b feature/awesome‑feature
   ```
3. **Make your changes** – keep the code vanilla and avoid adding heavy dependencies.
4. **Test locally** by opening `index.html`.
5. **Commit** with a clear message and **push** to your fork.
6. Open a **Pull Request** against the `main` branch.  Include a short description of what you changed and why.
7. Ensure the README stays up‑to‑date if you add new features.

---

## 📄 License
[MIT License](LICENSE) – *Replace this placeholder with the actual license file when ready.*

---

## 📚 Code Snippets
### Running the app locally (already covered in Installation)
```bash
open index.html   # macOS
# or simply double‑click the file.
```

### Extending the app – adding a priority field
1. Update the task schema in `app.js`:
   ```js
   // New property
   priority: "medium" // low | medium | high
   ```
2. Add a UI control (e.g., a dropdown) inside each task card.
3. Persist the new property alongside the existing ones.
4. Optionally, style tasks based on priority using CSS classes.
```

---

*Happy coding! 🎉*
