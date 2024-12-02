const mongoose = require('mongoose');

const inventoryItemSchema = new mongoose.Schema({
  name: { type: String, required: true },
  category: { type: String, required: true, enum: ['food', 'clothes', 'accessories', 'electronics'] },
  pricePerItem: { type: Number, required: true },
  description: { type: String, required: true },
  countInStock: { type: Number, required: true }
});

const Inventory = mongoose.model('Inventory', inventoryItemSchema);

module.exports = Inventory;
