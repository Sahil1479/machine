import api from "../api/client";

const fetchPnL = async () => {
    const res = await api.get('/finance/pnl/');
    return res.data;
}

const Dashboard = () => {
    return (
        <div className="p-8">
            <div>PnL Dashboard</div>
            <div className="mt-4 p-4 border rounded-lg shadow">
                <h2 className="text-xl font-semibold">Summary</h2>
                <p>Total Revenue: ₹pnl.revenue</p>
                <p>Total Expense: ₹pnl.expense</p>
                <p>Net Profit: ₹pnl.profit</p>
            </div>
        </div>
    )
}

export default Dashboard;