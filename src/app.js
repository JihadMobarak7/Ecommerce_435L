// Import database configuration to establish a connection
require('./config/db');

const express = require('express');
const inventoryRoutes = require('./inventory/routes/inventoryRoutes'); // Adjust the path as necessary

const app = express();
const port = 3000;

app.use(express.json()); // Middleware to parse JSON bodies

app.use('/inventory', inventoryRoutes); // Mount inventory routes

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
