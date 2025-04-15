import DistributionChart from '../components/DistributionChart';
import FlowChart from '../components/FlowChart';

const Charts = ({token}) => {
    return (
        <div className = 'charts'>
            <h2> Daily Distribution </h2>
            <DistributionChart token={token}/>
            <FlowChart token={token}/>
        </div>
    )
}

export default Charts;