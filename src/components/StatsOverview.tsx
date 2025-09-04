import React from 'react';
import { SeasonStats } from '../types';
import { formatPercentage } from '../utils';

interface StatsOverviewProps {
  stats: SeasonStats;
}

const StatsOverview: React.FC<StatsOverviewProps> = ({ stats }) => {
  return (
    <div className="card">
      <h2>Season Overview</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Picks</h3>
          <div className="value">{stats.totalPicks}</div>
        </div>
        <div className="stat-card">
          <h3>Win Rate</h3>
          <div className="value">{formatPercentage(stats.winRate)}</div>
        </div>
        <div className="stat-card">
          <h3>Record</h3>
          <div className="value">{stats.wins}-{stats.losses}-{stats.pushes}</div>
        </div>
        <div className="stat-card">
          <h3>Net Units</h3>
          <div className="value" style={{ color: stats.netUnits >= 0 ? '#28a745' : '#dc3545' }}>
            {stats.netUnits >= 0 ? '+' : ''}{stats.netUnits.toFixed(2)}
          </div>
        </div>
        <div className="stat-card">
          <h3>ROI</h3>
          <div className="value" style={{ color: stats.roi >= 0 ? '#28a745' : '#dc3545' }}>
            {stats.roi >= 0 ? '+' : ''}{formatPercentage(stats.roi)}
          </div>
        </div>
        <div className="stat-card">
          <h3>Units Won</h3>
          <div className="value" style={{ color: '#28a745' }}>
            +{stats.unitsWon.toFixed(2)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsOverview;
