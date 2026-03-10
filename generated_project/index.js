// index.js
// Simple Express server entry point
// This file starts an HTTP server that responds with "Hello, World!" at the root path.

import express from 'express';

// Create an Express application instance
const app = express();

// Define the port – use the environment variable PORT if provided, otherwise default to 3000
const PORT = process.env.PORT || 3000;

// Root route – returns a friendly greeting
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// Start the server and log a message when it is ready
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
