const mongoose = require('mongoose');

const connectionURL = 'mongodb://127.0.0.1:27017/yourDatabaseName'; // Replace 'yourDatabaseName' with the actual name of your MongoDB database.

mongoose.connect(connectionURL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('MongoDB connected successfully.'))
  .catch(err => console.error('MongoDB connection error:', err));
