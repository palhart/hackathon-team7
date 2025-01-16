import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { BarChart3, Users, Menu } from 'lucide-react';
import HistoricalAnalysis from './pages/HistoricalAnalysis';
import CompetitorAnalysis from './pages/CompetitorAnalysis';

function App() {
  const [sidebarOpen, setSidebarOpen] = React.useState(true);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex">
        {/* Sidebar */}
        <div className={`bg-white shadow-lg ${sidebarOpen ? 'w-64' : 'w-20'} transition-all duration-300`}>
          <div className="p-4 flex items-center justify-between">
            <h1 className={`text-xl font-bold text-[#85FA98] ${!sidebarOpen && 'hidden'}`}>Venture Vision</h1>
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 hover:bg-gray-100 rounded">
              <Menu size={20} />
            </button>
          </div>
          <nav className="mt-8">
            <Link to="/" className="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-100">
              <BarChart3 size={20} />
              {sidebarOpen && <span className="ml-3">Historical Analysis</span>}
            </Link>
            <Link to="/competitor" className="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-100">
              <Users size={20} />
              {sidebarOpen && <span className="ml-3">Competitor Analysis</span>}
            </Link>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-x-hidden">
          <Routes>
            <Route path="/" element={<HistoricalAnalysis />} />
            <Route path="/competitor" element={<CompetitorAnalysis />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;