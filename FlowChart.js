import { useEffect, useState} from 'react';
import { ResponsiveContainer, BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const FlowChart = ({token}) => {

    const [flow, setFlow] = useState([]);

    useEffect(() => {
        const fetchFlow = async () => {
            try {
                const response = await fetch(`/api/data/flow/${token}`); // Replace with your API endpoint
                const result = await response.json();
                setFlow(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchFlow();
    }, []);

    return (
            <ResponsiveContainer width="60%" height={300}>
                <BarChart
                    data={flow}
                    margin={{
                        top: 5,
                        right: 5,
                        left: 5,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="day" />
                    <YAxis  />
                    <Bar dataKey="volume" name = 'volume' fill="#e06666" barSize={20} radius = {[5,5,0,0]} activeBar={<Rectangle fill="#e06666" />}/>
                </BarChart>
            </ResponsiveContainer>
    );
}



export default FlowChart;

