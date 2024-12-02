const express = require('express');
const router = express.Router();
const InventoryItem = require('../models/InventoryItem'); // Adjust the path as necessary

// POST endpoint to add new goods
router.post('/', async (req, res) => {
  const { name, category, pricePerItem, description, countInStock } = req.body;
  try {
    const newItem = new InventoryItem({
      name,
      category,
      pricePerItem,
      description,
      countInStock
    });
    await newItem.save();
    res.status(201).send(newItem);
  } catch (error) {
    res.status(400).send(error);
  }
});

// POST endpoint to deduct goods
router.post('/deduct', async (req, res) => {
  const { itemId, quantity } = req.body;
  try {
    const item = await InventoryItem.findById(itemId);
    if (item && item.countInStock >= quantity) {
      item.countInStock -= quantity;
      await item.save();
      res.status(200).send(item);
    } else {
      res.status(400).send({ message: 'Insufficient stock or item not found' });
    }
  } catch (error) {
    res.status(500).send(error);
  }
});

// PUT endpoint to update goods
router.put('/:itemId', async (req, res) => {
  const { name, category, pricePerItem, description, countInStock } = req.body;
  const { itemId } = req.params;
  try {
    const item = await InventoryItem.findByIdAndUpdate(itemId, {
      name,
      category,
      pricePerItem,
      description,
      countInStock
    }, { new: true });
    if (item) {
      res.status(200).send(item);
    } else {
      res.status(404).send({ message: 'Item not found' });
    }
  } catch (error) {
    res.status(400).send(error);
  }
});

module.exports = router;
