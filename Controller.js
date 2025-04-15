const mongoose = require('mongoose');
const {DistributionSchema} = require('../models/DistributionModel')
const {FlowSchema} = require('../models/FlowModel')

//const UserGraph = require('../models/GraphModel')

const getDistribution = async (req, res) => {
    try {
        const { id } = req.params;
        coname = id+'-dist';
        const modelDistribution = mongoose.model(coname, DistributionSchema, coname)
        const distribution = await modelDistribution.find({}).sort({rank:1});
        res.status(200).json(distribution);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching distributions', error });
    }
};

const getFlow = async (req, res) => {
    try {
        const { id } = req.params;
        coname = id+'-flow';
        
        const modelFlow = mongoose.model(coname, FlowSchema, coname)
        const flow = await modelFlow.aggregate([{ $group : { 
                                                    _id: { day: '$day', dex: '$dex', }, 
                                                    volume : {$sum: '$volume'}} }]);
        console.log(flow);
        res.status(200).json(flow);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching flow', error });
    }
};

/*
    try {
        await client.connect();
        const db = client.db(DB_NAME);
        const collection = db.collection(flow_collection);

        const pipeline = [
            {
                $group: {
                    _id: "$dex",
                    agg_p_flow: { $sum: "$positive_flow" },
                    agg_n_flow: { $sum: "$negative_flow" },
                    net_flow: { $sum: "$netflow" },
                    volume: { $sum: "$volume" },
                }
            }
        ];
        
        const result = await collection.aggregate(pipeline).toArray();
        return result.map(item => ({ 
            label: item._id, 
            agg_p_flow: item.agg_p_flow,
            agg_n_flow: item.agg_n_flow,
            net_flow: item.net_flow,
            volume: item.volume
        }));
    } finally {
        await client.close();
    }
*/


const getUserGraph = async (req, res) => {
    try {
        // i will have a list of users defined by me as id 
        // this will fetch a graph related to the cluster of wallets
        const { user_id } = req.params;
        if (!mongoose.Types.ObjectId.isValid(user_id)) {
            return res.status(404).json({ message: 'Invalid user ID format' });
        }
        const graph = await UserGraph.findById(user_id);
        if (!graph) {
            return res.status(404).json({ message: 'Graph not found' });
        }
        res.status(200).json(graph);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching graph by ID', error });
    }
};

module.exports = { getDistribution, getFlow };