const mongoose = require('mongoose');
const Schema = mongoose.Schema

/*
_id 67eb73f6ee43945704a495d9
rank 2
bin "[100-500)"
buy_count 0
sell_count 7
buy_bin_volume 0
sell_bin_volume 1917.6931744520757
*/

const DistributionSchema = new Schema({
    rank: {
        type: Number,
        required: true,
    },
    bin: {
        type: String,
        required: true,
    },
    buy_count: {
        type: Number,
        required: true,
    },
    sell_count: {
        type: Number,
        required: true,
    },
    buy_bin_volume: {
        type: Number,
        required: true,
    },
    sell_bin_volume: {
        type: Number,
        required: true,
    },
} );

module.exports = {DistributionSchema};