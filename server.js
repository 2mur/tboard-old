require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const mongoRoutes = require('./routes/mongo.routes');

const app = express();
app.use(express.json());

app.use( (req,res,next) => {
    console.log(req.path, req.method)
    next()
})

app.use('/api/data', mongoRoutes);

mongoose.connect(process.env.MONGO_URI)
.then(() => {
    app.listen(process.env.PORT, () => {
        console.log(`Connected to MongoDB - Server is running on port ${process.env.PORT}`);
    });
})
.catch((err) => console.error('Failed to connect to MongoDB', err));
