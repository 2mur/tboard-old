const mongoose = require('mongoose');
const Schema = mongoose.Schema

/*
day "2025-04-01"
pool "ARENA-NOCHILL"
dex "trader_joe"
ver "v1" 
positive_flow 0.0101224251200717
negative_flow -0.5234683282881094
netflow -0.5133459031680376
volume 0.5335907534081812
*/

const FlowSchema = new Schema({
    day: {
        type: Date,
        required: true,
    },
    pool: {
        type: String,
        required: true,
    },
    dex: {
        type: String,
        required: true,
    },
    ver: {
        type: String,
        required: true,
    },
    positive_flow: {
        type: Number,
        required: true,
    }, 
    negative_flow: {
        type: Number,
        required: true,
    }, 
    netflow: {
        type: Number,
        required: true,
    },
    volume: {
        type: Number,
        required: true,
    },
} );

module.exports = {FlowSchema};