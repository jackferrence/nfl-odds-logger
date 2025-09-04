import React, { useState } from 'react';
import { Pick, PickResult } from '../types';

interface PicksListProps {
  picks: Pick[];
  onUpdatePick: (id: string, updates: Partial<Pick>) => void;
  onDeletePick: (id: string) => void;
}

const PicksList: React.FC<PicksListProps> = ({ picks, onUpdatePick, onDeletePick }) => {
  const [filterWeek, setFilterWeek] = useState<number | 'all'>('all');
  const [filterResult, setFilterResult] = useState<PickResult | 'all'>('all');

  const filteredPicks = picks.filter(pick => {
    if (filterWeek !== 'all' && pick.week !== filterWeek) return false;
    if (filterResult !== 'all' && pick.result !== filterResult) return false;
    return true;
  });

  const sortedPicks = [...filteredPicks].sort((a, b) => {
    // Sort by week (descending), then by date (descending)
    if (a.week !== b.week) return b.week - a.week;
    return new Date(b.date).getTime() - new Date(a.date).getTime();
  });

  const weeks = Array.from(new Set(picks.map(pick => pick.week))).sort((a, b) => b - a);

  const handleResultChange = (id: string, result: PickResult) => {
    onUpdatePick(id, { result });
  };

  const handleDelete = (id: string) => {
    if (window.confirm('Are you sure you want to delete this pick?')) {
      onDeletePick(id);
    }
  };

  if (picks.length === 0) {
    return (
      <div className="card">
        <h2>All Picks</h2>
        <div className="empty-state">
          <h3>No picks yet</h3>
          <p>Add your first pick to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>All Picks</h2>
      
      <div className="grid grid-2" style={{ marginBottom: '20px' }}>
        <div className="form-group">
          <label htmlFor="weekFilter">Filter by Week</label>
          <select
            id="weekFilter"
            className="form-control"
            value={filterWeek}
            onChange={(e) => setFilterWeek(e.target.value === 'all' ? 'all' : Number(e.target.value))}
          >
            <option value="all">All Weeks</option>
            {weeks.map(week => (
              <option key={week} value={week}>Week {week}</option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="resultFilter">Filter by Result</label>
          <select
            id="resultFilter"
            className="form-control"
            value={filterResult}
            onChange={(e) => setFilterResult(e.target.value as PickResult | 'all')}
          >
            <option value="all">All Results</option>
            <option value="pending">Pending</option>
            <option value="win">Win</option>
            <option value="loss">Loss</option>
            <option value="push">Push</option>
          </select>
        </div>
      </div>

      {sortedPicks.length === 0 ? (
        <div className="empty-state">
          <h3>No picks match your filters</h3>
          <p>Try adjusting your filter criteria.</p>
        </div>
      ) : (
        <div>
          {sortedPicks.map(pick => (
            <div key={pick.id} className={`pick-item ${pick.result || 'pending'}`}>
              <div className="pick-details">
                <div className="pick-teams">
                  {pick.team1} vs {pick.team2}
                </div>
                <div className="pick-info">
                  Week {pick.week} • {pick.date} • {pick.betType} • {pick.units} unit{pick.units !== 1 ? 's' : ''}
                  {pick.odds && ` • ${pick.odds > 0 ? '+' : ''}${pick.odds}`}
                </div>
                <div className="pick-info">
                  <strong>Pick:</strong> {pick.pick}
                  {pick.notes && ` • ${pick.notes}`}
                </div>
              </div>
              
              <div className="pick-result">
                <select
                  className="form-control"
                  value={pick.result || 'pending'}
                  onChange={(e) => handleResultChange(pick.id, e.target.value as PickResult)}
                  style={{ marginBottom: '8px', minWidth: '100px' }}
                >
                  <option value="pending">Pending</option>
                  <option value="win">Win</option>
                  <option value="loss">Loss</option>
                  <option value="push">Push</option>
                </select>
                
                <button
                  className="btn btn-danger"
                  onClick={() => handleDelete(pick.id)}
                  style={{ fontSize: '12px', padding: '6px 12px' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PicksList;
