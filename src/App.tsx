import React, { useState, useEffect } from 'react';
import { Pick } from './types';
import { loadPicks, savePicks, calculateSeasonStats, exportToCSV, exportStatsToCSV } from './utils';
import Header from './components/Header';
import StatsOverview from './components/StatsOverview';
import PickForm from './components/PickForm';
import PicksList from './components/PicksList';
import WeekStats from './components/WeekStats';
import BetTypeStats from './components/BetTypeStats';

function App() {
  const [picks, setPicks] = useState<Pick[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'add' | 'picks' | 'stats'>('overview');

  useEffect(() => {
    const savedPicks = loadPicks();
    setPicks(savedPicks);
  }, []);

  const addPick = (newPick: Omit<Pick, 'id' | 'createdAt'>) => {
    const pick: Pick = {
      ...newPick,
      id: Date.now().toString(),
      createdAt: new Date().toISOString()
    };
    const updatedPicks = [...picks, pick];
    setPicks(updatedPicks);
    savePicks(updatedPicks);
  };

  const updatePick = (id: string, updates: Partial<Pick>) => {
    const updatedPicks = picks.map(pick => 
      pick.id === id ? { ...pick, ...updates } : pick
    );
    setPicks(updatedPicks);
    savePicks(updatedPicks);
  };

  const deletePick = (id: string) => {
    const updatedPicks = picks.filter(pick => pick.id !== id);
    setPicks(updatedPicks);
    savePicks(updatedPicks);
  };

  const handleExportPicks = () => {
    exportToCSV(picks);
  };

  const handleExportStats = () => {
    exportStatsToCSV(picks);
  };

  const seasonStats = calculateSeasonStats(picks);

  return (
    <div className="container">
      <Header />
      
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'add' ? 'active' : ''}`}
          onClick={() => setActiveTab('add')}
        >
          Add Pick
        </button>
        <button 
          className={`tab ${activeTab === 'picks' ? 'active' : ''}`}
          onClick={() => setActiveTab('picks')}
        >
          All Picks
        </button>
        <button 
          className={`tab ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          Statistics
        </button>
      </div>

      {/* Export buttons */}
      {picks.length > 0 && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h2>Export Data</h2>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            <button 
              className="btn btn-secondary"
              onClick={handleExportPicks}
            >
              📊 Export Picks to CSV
            </button>
            <button 
              className="btn btn-secondary"
              onClick={handleExportStats}
            >
              📈 Export Statistics to CSV
            </button>
          </div>
          <p style={{ marginTop: '10px', fontSize: '0.9rem', color: '#666' }}>
            Download your picks and statistics as CSV files for backup or analysis in Excel/Google Sheets.
          </p>
        </div>
      )}

      {activeTab === 'overview' && (
        <div>
          <StatsOverview stats={seasonStats} />
          <div className="grid grid-2">
            <WeekStats picks={picks} />
            <BetTypeStats picks={picks} />
          </div>
        </div>
      )}

      {activeTab === 'add' && (
        <PickForm onAddPick={addPick} />
      )}

      {activeTab === 'picks' && (
        <PicksList 
          picks={picks} 
          onUpdatePick={updatePick}
          onDeletePick={deletePick}
        />
      )}

      {activeTab === 'stats' && (
        <div className="grid grid-2">
          <WeekStats picks={picks} />
          <BetTypeStats picks={picks} />
        </div>
      )}
    </div>
  );
}

export default App;
