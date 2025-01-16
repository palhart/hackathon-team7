import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

function CompetitorAnalysis() {
  // Process data for fintech companies
  const competitors = [
    { name: "Revolut", employees: 9200, funding: 1738, traffic: 53454127 },
    { name: "Wise", employees: 4925, funding: 1665, traffic: 130095596 },
    { name: "Chime", employees: 1635, funding: 2292, traffic: 31206766 },
    { name: "Starling", employees: 2277, funding: 1086, traffic: 3516617 },
    { name: "Monzo", employees: 2814, funding: 1737, traffic: 10963289 },
    { name: "N26", employees: 1556, funding: 1719, traffic: 9946288 },
    { name: "Monese", employees: 190, funding: 205, traffic: 560438 },
    { name: "bunq", employees: 576, funding: 422, traffic: 6824137 },
    { name: "Qonto", employees: 1453, funding: 709, traffic: 10336450 },
    { name: "Finom", employees: 399, funding: 108, traffic: 1733630 }
  ];

  const quarterlyTraffic = [
    { quarter: "2024Q1", Revolut: 44996864, Wise: 105217477, Chime: 26874593, Starling: 3687564, Monzo: 9515359, N26: 10007888, Monese: 740946, bunq: 7002136, Qonto: 9038936, Finom: 1283383 },
    { quarter: "2024Q2", Revolut: 44819127, Wise: 117876626, Chime: 26372764, Starling: 3400923, Monzo: 9582490, N26: 10573925, Monese: 657720, bunq: 7135522, Qonto: 8831727, Finom: 1390299 },
    { quarter: "2024Q3", Revolut: 49001065, Wise: 129937193, Chime: 29077656, Starling: 4033578, Monzo: 11176304, N26: 10788831, Monese: 694623, bunq: 7634651, Qonto: 9347201, Finom: 1490439 },
    { quarter: "2024Q4", Revolut: 53454127, Wise: 130095596, Chime: 31206766, Starling: 3516617, Monzo: 10963289, N26: 9946288, Monese: 560438, bunq: 6824137, Qonto: 10336450, Finom: 1733630 }
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