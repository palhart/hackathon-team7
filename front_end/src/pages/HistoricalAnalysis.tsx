import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { historicalData } from '../data/mockData';

function HistoricalAnalysis() {
  const headcountData = historicalData.map(item => ({
    quarter: `${item.quarter}Q ${item.year}`,
    headcount: item.Headcount_Count,
    growth: item.Headcount_Growth
  }));

  const financialData = historicalData.map(item => ({
    quarter: `${item.quarter}Q ${item.year}`,
    gmv: item.Financials_GMV / 1000000, // Convert to millions
    sales: item.Financials_Net_Sales / 1000000,
    cac: item.Financials_CAC
  }));

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Historical Analysis</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Headcount Metrics */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Headcount Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={headcountData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="quarter" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="headcount" stroke="#85FA98" name="Headcount" />
              <Line type="monotone" dataKey="growth" stroke="#FF9F9F" name="Growth %" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Financial Metrics */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Financial Performance</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={financialData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="quarter" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="gmv" fill="#85FA98" name="GMV (M)" />
              <Bar dataKey="sales" fill="#82ca9d" name="Net Sales (M)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Department Distribution */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Department Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="quarter" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="tech" stackId="a" fill="#85FA98" name="Tech" />
              <Bar dataKey="sales" stackId="a" fill="#82ca9d" name="Sales" />
              <Bar dataKey="admin" stackId="a" fill="#8884d8" name="Admin" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* CAC Trends */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Customer Acquisition Cost</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={financialData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="quarter" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="cac" stroke="#85FA98" name="CAC ($)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default HistoricalAnalysis;