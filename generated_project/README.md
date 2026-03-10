# Simple Hello World API

A minimal Node.js Express server that responds with **"Hello, World!"** on a `GET /` request. This project demonstrates a basic API setup and can be used as a starting point for more complex services.

---

## 📦 Installation

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/your-username/simple-hello-world-api.git
cd simple-hello-world-api

# Install dependencies
npm install
```

---

## 🚀 Start the Server

```bash
npm start
```

The server will start on **http://localhost:3000** (or the port defined in the `PORT` environment variable).

---

## 📡 Example Request

```bash
curl http://localhost:3000/
```

**Response**

```
Hello, World!
```

---

## 🗂️ Project Structure

- `index.js` – The main server file that sets up the Express app and defines the route.
- `package.json` – Project metadata and scripts.
- `README.md` – This documentation.

---

## 📝 Notes

- The API returns the plain text string **"Hello, World!"** when a `GET` request is made to the root path (`/`).
- Feel free to extend the server by adding more routes, middleware, or integrating a database.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
