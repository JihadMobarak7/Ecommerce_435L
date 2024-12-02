const express = require('express');
const Review = require('../models/review');
const router = express.Router();

// Submit Review
router.post('/', async (req, res) => {
  try {
    const { product, user, rating, comment } = req.body;
    const newReview = await Review.create({ product, user, rating, comment });
    res.status(201).send(newReview);
  } catch (error) {
    res.status(400).send(error);
  }
});

// Update Review
router.put('/:id', async (req, res) => {
  try {
    const { rating, comment } = req.body;
    const updatedReview = await Review.findByIdAndUpdate(req.params.id, { rating, comment }, { new: true });
    res.status(200).send(updatedReview);
  } catch (error) {
    res.status(400).send(error);
  }
});

// Delete Review
router.delete('/:id', async (req, res) => {
  try {
    await Review.findByIdAndDelete(req.params.id);
    res.status(204).send();
  } catch (error) {
    res.status(500).send(error);
  }
});

// Get Product Reviews
router.get('/product/:productId', async (req, res) => {
  try {
    const reviews = await Review.find({ product: req.params.productId });
    res.status(200).send(reviews);
  } catch (error) {
    res.status(500).send(error);
  }
});

// Get Customer Reviews
router.get('/user/:userId', async (req, res) => {
  try {
    const reviews = await Review.find({ user: req.params.userId });
    res.status(200).send(reviews);
  } catch (error) {
    res.status(500).send(error);
  }
});

module.exports = router;
