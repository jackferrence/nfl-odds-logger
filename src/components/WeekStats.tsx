import React from 'react';
import { Pick } from '../types';
import { calculateWeekStats } from '../utils';

interface WeekStatsProps {
  picks: Pick[];
}

const WeekStats: React.FC<WeekStatsProps> = ({ picks }) => {
  const weeks = Array.from(new Set(picks.map(pick => pick.week))).sort((a, b) => a - b);
  const weekStats = weeks.map(week => calculateWeekStats(picks, week));

  if (weekStats.length === 0) {
    return (
      <div className="card">
        <h2>Weekly Performance</h2>
        <div className="empty-state">
          <h3>No picks yet</h3>
          <p>Add picks to see weekly statistics.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Weekly Performance</h2>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #e1e5e9' }}>
              <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Week</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Picks</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Record</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Win Rate</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Net Units</th>
            </tr>
          </thead>
          <tbody>
            {weekStats.map(stat => (
              <tr key={stat.week} style={{ borderBottom: '1px solid #e9ecef' }}>
                <td style={{ padding: '12px', fontWeight: '600' }}>Week {stat.week}</td>
                <td style={{ padding: '12px', textAlign: 'center' }}>{stat.picks}</td>
                <td style={{ padding: '12px', textAlign: 'center' }}>
                  {stat.wins}-{stat.losses}-{stat.pushes}
                </td>
                <td style={{ padding: '12px', textAlign: 'center' }}>
                  {stat.picks > 0 ? `${((stat.wins / stat.picks) * 100).toFixed(1)}%` : '0%'}
                </td>
                <td 
                  style={{ 
                    padding: '12px', 
                    textAlign: 'center', 
                    fontWeight: '600',
                    color: stat.netUnits >= 0 ? '#28a745' : '#dc3545'
                  }}
                >
                  {stat.netUnits >= 0 ? '+' : ''}{stat.netUnits.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default WeekStats;
