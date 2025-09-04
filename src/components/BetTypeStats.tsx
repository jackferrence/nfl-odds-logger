import React from 'react';
import { Pick } from '../types';
import { calculateBetTypeStats } from '../utils';

interface BetTypeStatsProps {
  picks: Pick[];
}

const BetTypeStats: React.FC<BetTypeStatsProps> = ({ picks }) => {
  const betTypeStats = calculateBetTypeStats(picks);
  const nonEmptyStats = betTypeStats.filter(stat => stat.picks > 0);

  if (nonEmptyStats.length === 0) {
    return (
      <div className="card">
        <h2>Performance by Bet Type</h2>
        <div className="empty-state">
          <h3>No picks yet</h3>
          <p>Add picks to see performance by bet type.</p>
        </div>
      </div>
    );
  }

  const getBetTypeLabel = (betType: string) => {
    const labels: Record<string, string> = {
      spread: 'Spread',
      moneyline: 'Moneyline',
      over: 'Over',
      under: 'Under',
      prop: 'Prop'
    };
    return labels[betType] || betType;
  };

  return (
    <div className="card">
      <h2>Performance by Bet Type</h2>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #e1e5e9' }}>
              <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Bet Type</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Picks</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Record</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Win Rate</th>
              <th style={{ padding: '12px', textAlign: 'center', fontWeight: '600' }}>Net Units</th>
            </tr>
          </thead>
          <tbody>
            {nonEmptyStats.map(stat => (
              <tr key={stat.betType} style={{ borderBottom: '1px solid #e9ecef' }}>
                <td style={{ padding: '12px', fontWeight: '600' }}>
                  {getBetTypeLabel(stat.betType)}
                </td>
                <td style={{ padding: '12px', textAlign: 'center' }}>{stat.picks}</td>
                <td style={{ padding: '12px', textAlign: 'center' }}>
                  {stat.wins}-{stat.losses}-{stat.pushes}
                </td>
                <td style={{ padding: '12px', textAlign: 'center' }}>
                  {stat.winRate.toFixed(1)}%
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

export default BetTypeStats;
