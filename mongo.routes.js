const express = require('express');
const { getDistribution, getFlow } = require('../controllers/Controller');

const router = express.Router();

router.get('/dist/:id', getDistribution);
router.get('/flow/:id', getFlow);

module.exports = router;