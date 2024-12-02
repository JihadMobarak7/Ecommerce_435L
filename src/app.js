// Import database configuration to establish a connection
require('./config/db');

const express = require('express');
const mongoose = require('mongoose');
const inventoryRoutes = require('./inventory/routes/inventoryRoutes');

const app = express();
app.use(express.json()); // for parsing application/json
app.use('/inventory', inventoryRoutes);

mongoose.connect('your-mongodb-connection-string', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
