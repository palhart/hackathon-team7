import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

function CompetitorAnalysis() {
  // Process data for fintech companies
  const competitors = [
    { name: "Company1", employees: 9200, funding: 1738, traffic: 53454127 },
    { name: "Company2", employees: 4925, funding: 1665, traffic: 130095596 },
    { name: "Company3", employees: 1635, funding: 2292, traffic: 31206766 },
    { name: "Company4", employees: 2277, funding: 1086, traffic: 3516617 },
    { name: "Company5", employees: 2814, funding: 1737, traffic: 10963289 },
    { name: "Company6", employees: 1556, funding: 1719, traffic: 9946288 },
    { name: "Company7", employees: 190, funding: 205, traffic: 560438 },
    { name: "Company8", employees: 576, funding: 422, traffic: 6824137 },
    { name: "Company9", employees: 1453, funding: 709, traffic: 10336450 },
    { name: "Company10", employees: 399, funding: 108, traffic: 1733630 }
  ];

  const quarterlyTraffic = [
    { quarter: "2024Q1", Company1: 44996864, Company2: 105217477, Company3: 26874593, Company4: 3687564, Company5: 9515359, Company6: 10007888, Company7: 740946, Company8: 7002136, Company9: 9038936, Company10: 1283383 },
    { quarter: "2024Q2", Company1: 44819127, Company2: 117876626, Company3: 26372764, Company4: 3400923, Company5: 9582490, Company6: 10573925, Company7: 657720, Company8: 7135522, Company9: 8831727, Company10: 1390299 },
    { quarter: "2024Q3", Company1: 49001065, Company2: 129937193, Company3: 29077656, Company4: 4033578, Company5: 11176304, Company6: 10788831, Company7: 694623, Company8: 7634651, Company9: 9347201, Company10: 1490439 },
    { quarter: "2024Q4", Company1: 53454127, Company2: 130095596, Company3: 31206766, Company4: 3516617, Company5: 10963289, Company6: 9946288, Company7: 560438, Company8: 6824137, Company9: 10336450, Company10: 1733630 }
  ];

  // Calculate market share based on latest quarter traffic
  const totalTraffic = competitors.reduce((sum, item) => sum + item.traffic, 0);
  const marketShareData = competitors.map(item => ({
    name: item.name,
    value: (item.traffic / totalTraffic) * 100
  }));

  // Colors for consistent company representation
  const COLORS = ['#85FA98', '#FF9F9F', '#FFD700', '#87CEEB', '#FFA500', '#98FB98', '#DDA0DD', '#F0E68C', '#87CEFA', '#FFA07A'];

  // Process quarterly traffic data for the line chart
  const processedTrafficData = quarterlyTraffic.map(quarter => {
    const processed = { quarter: quarter.quarter };
    Object.keys(quarter).forEach(key => {
      if (key !== 'quarter') {
        processed[key] = quarter[key] / 1000000; // Convert to millions
      }
    });
    return processed;
  });

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Fintech Competitor Analysis</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Web Traffic Market Share */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Market Share by Web Traffic</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={marketShareData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
              >
                {marketShareData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Web Traffic Evolution */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Web Traffic Evolution (Millions of Visits)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={processedTrafficData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="quarter" />
              <YAxis />
              <Tooltip />
              <Legend />
              {competitors.map((company, index) => (
                <Line
                  key={company.name}
                  type="monotone"
                  dataKey={company.name}
                  stroke={COLORS[index % COLORS.length]}
                  strokeWidth={2}
                  dot={{ fill: COLORS[index % COLORS.length] }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Employee Count vs Funding */}
        <div className="bg-white p-6 rounded-lg shadow-md col-span-2">
          <h2 className="text-xl font-semibold mb-4">Employees vs Funding</h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={competitors} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="name" width={100} />
              <Tooltip 
                content={({ payload }) => {
                  if (!payload || !payload[0]) return null;
                  const data = payload[0].payload;
                  return (
                    <div className="bg-white p-2 border border-gray-200 shadow-sm">
                      <p className="font-semibold">{data.name}</p>
                      <p>Employees: {data.employees.toLocaleString()}</p>
                      <p>Funding: ${data.funding.toLocaleString()}M</p>
                    </div>
                  );
                }}
              />
              <Legend />
              <Bar dataKey="employees" name="Total Employees" fill="#85FA98" stackId="a">
                {competitors.map((comp, index) => (
                  <Cell key={`employee-cell-${comp.name}-${index}`} fill="#85FA98" />
                ))}
              </Bar>
              <Bar dataKey="funding" name="Funding ($M)" fill="#FF9F9F" stackId="b">
                {competitors.map((comp, index) => (
                  <Cell key={`funding-cell-${comp.name}-${index}`} fill="#FF9F9F" />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default CompetitorAnalysis;