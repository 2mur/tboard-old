import { useEffect, useState} from 'react';
import { ResponsiveContainer, BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const DistributionChart = ({token}) => {
    const [dist, setDist] = useState([]);

    useEffect(() => {
        const fetchDistribution = async () => {
            try {
                const response = await fetch(`/api/data/dist/${token}`); // Replace with your API endpoint
                const result = await response.json();
                setDist(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
    fetchDistribution();
    }, []);

    function CustomTooltip({ payload, label, active }) {
        if (active) {
          return (
            <div className="custom-tooltip">
              <p className="label">{`Bin: $${label}`}</p>
              <p >{`Sell Vol: $${payload[0].value.toFixed(2)}`}</p>
              <p >{`Buy Vol: $${payload[1].value.toFixed(2)}`}</p>
            </div>
          );
        }
      
        return null;
    }

    return (
            <ResponsiveContainer width="60%" height={300}>
                <BarChart
                    data={dist}
                    margin={{
                        top: 5,
                        right: 5,
                        left: 5,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="bin" />
                    <YAxis  />
                    <Legend content = {['sell bins', 'buy bins']}/>
                    <Bar dataKey="sell_bin_volume" name = 'sell bins' fill="#e06666" barSize={20} radius = {[5,5,0,0]} activeBar={<Rectangle fill="#e06666" />}/>
                    <Bar dataKey="buy_bin_volume" name = 'buy bins' fill="#b6d7a8" barSize={20} radius = {[5,5,0,0]} activeBar={<Rectangle fill="#b6d7a8" />}/>
                </BarChart>
            </ResponsiveContainer>
    );
}
//<Tooltip content={<CustomTooltip />} wrapperStyle={{backgroundColor: '#ffcccc'}} />

export default DistributionChart;

