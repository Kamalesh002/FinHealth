import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#0ea5e9'];

function MetricChart({ type, data, title, height = 250 }) {
    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="chart-tooltip">
                    <p className="tooltip-label">{label}</p>
                    {payload.map((entry, index) => (
                        <p key={index} style={{ color: entry.color }}>
                            {entry.name}: {typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}
                        </p>
                    ))}
                </div>
            );
        }
        return null;
    };

    const renderChart = () => {
        switch (type) {
            case 'line':
                return (
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                        <XAxis
                            dataKey="name"
                            stroke="var(--text-muted)"
                            fontSize={12}
                        />
                        <YAxis
                            stroke="var(--text-muted)"
                            fontSize={12}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke="var(--primary)"
                            strokeWidth={2}
                            dot={{ fill: 'var(--primary)', strokeWidth: 2 }}
                            activeDot={{ r: 6, fill: 'var(--primary-light)' }}
                        />
                        {data[0]?.value2 && (
                            <Line
                                type="monotone"
                                dataKey="value2"
                                stroke="var(--success)"
                                strokeWidth={2}
                                dot={{ fill: 'var(--success)', strokeWidth: 2 }}
                            />
                        )}
                    </LineChart>
                );

            case 'bar':
                return (
                    <BarChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                        <XAxis
                            dataKey="name"
                            stroke="var(--text-muted)"
                            fontSize={12}
                        />
                        <YAxis
                            stroke="var(--text-muted)"
                            fontSize={12}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Bar
                            dataKey="value"
                            fill="var(--primary)"
                            radius={[4, 4, 0, 0]}
                        />
                        {data[0]?.benchmark && (
                            <Bar
                                dataKey="benchmark"
                                fill="var(--text-muted)"
                                radius={[4, 4, 0, 0]}
                            />
                        )}
                    </BarChart>
                );

            case 'pie':
                return (
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={80}
                            paddingAngle={5}
                            dataKey="value"
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip content={<CustomTooltip />} />
                    </PieChart>
                );

            case 'multiBar':
                return (
                    <BarChart data={data} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                        <XAxis type="number" stroke="var(--text-muted)" fontSize={12} />
                        <YAxis
                            type="category"
                            dataKey="name"
                            stroke="var(--text-muted)"
                            fontSize={12}
                            width={100}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Bar dataKey="company" fill="var(--primary)" radius={[0, 4, 4, 0]} />
                        <Bar dataKey="industry" fill="var(--text-muted)" radius={[0, 4, 4, 0]} />
                    </BarChart>
                );

            default:
                return null;
        }
    };

    return (
        <div className="metric-chart">
            {title && <h4 className="chart-title">{title}</h4>}
            <ResponsiveContainer width="100%" height={height}>
                {renderChart()}
            </ResponsiveContainer>

            <style>{`
        .metric-chart {
          background: var(--bg-card);
          border-radius: var(--radius-lg);
          padding: var(--spacing-lg);
          border: 1px solid var(--border);
        }

        .chart-title {
          font-size: var(--font-size-base);
          font-weight: 600;
          margin-bottom: var(--spacing-md);
          color: var(--text-primary);
        }

        .chart-tooltip {
          background: var(--bg-dark);
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: var(--spacing-sm) var(--spacing-md);
          font-size: var(--font-size-sm);
        }

        .tooltip-label {
          font-weight: 600;
          margin-bottom: var(--spacing-xs);
          color: var(--text-primary);
        }
      `}</style>
        </div>
    );
}

export default MetricChart;
