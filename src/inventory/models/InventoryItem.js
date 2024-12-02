const mongoose = require('mongoose');

const inventoryItemSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  category: {
    type: String,
    required: true,
    enum: ['food', 'clothes', 'accessories', 'electronics'],
    trim: true
  },
  pricePerItem: {
    type: Number,
    required: true
  },
  description: {
    type: String,
    required: false,
    trim: true
  },
  countInStock: {
    type: Number,
    required: true,
    min: 0
  }
});

const InventoryItem = mongoose.model('InventoryItem', inventoryItemSchema);

module.exports = InventoryItem;
