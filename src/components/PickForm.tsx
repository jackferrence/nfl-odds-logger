import React, { useState } from 'react';
import { BetType } from '../types';
import { getCurrentWeek } from '../utils';

interface PickFormProps {
  onAddPick: (pick: Omit<import('../types').Pick, 'id' | 'createdAt'>) => void;
}

const PickForm: React.FC<PickFormProps> = ({ onAddPick }) => {
  const [formData, setFormData] = useState({
    week: getCurrentWeek(),
    date: new Date().toISOString().split('T')[0],
    team1: '',
    team2: '',
    pick: '',
    betType: 'spread' as BetType,
    units: 1,
    odds: undefined as number | undefined,
    notes: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.team1 || !formData.team2 || !formData.pick) {
      alert('Please fill in all required fields');
      return;
    }

    onAddPick({
      ...formData,
      odds: formData.odds || undefined
    });

    // Reset form
    setFormData({
      week: getCurrentWeek(),
      date: new Date().toISOString().split('T')[0],
      team1: '',
      team2: '',
      pick: '',
      betType: 'spread',
      units: 1,
      odds: undefined,
      notes: ''
    });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'week' || name === 'units' || name === 'odds' ? 
        (value === '' ? undefined : Number(value)) : value
    }));
  };

  return (
    <div className="card">
      <h2>Add New Pick</h2>
      <form onSubmit={handleSubmit}>
        <div className="grid grid-2">
          <div className="form-group">
            <label htmlFor="week">Week *</label>
            <input
              type="number"
              id="week"
              name="week"
              className="form-control"
              value={formData.week}
              onChange={handleChange}
              min="1"
              max="18"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="date">Date *</label>
            <input
              type="date"
              id="date"
              name="date"
              className="form-control"
              value={formData.date}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="grid grid-2">
          <div className="form-group">
            <label htmlFor="team1">Team 1 *</label>
            <input
              type="text"
              id="team1"
              name="team1"
              className="form-control"
              value={formData.team1}
              onChange={handleChange}
              placeholder="e.g., Kansas City Chiefs"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="team2">Team 2 *</label>
            <input
              type="text"
              id="team2"
              name="team2"
              className="form-control"
              value={formData.team2}
              onChange={handleChange}
              placeholder="e.g., Buffalo Bills"
              required
            />
          </div>
        </div>

        <div className="grid grid-3">
          <div className="form-group">
            <label htmlFor="pick">Your Pick *</label>
            <input
              type="text"
              id="pick"
              name="pick"
              className="form-control"
              value={formData.pick}
              onChange={handleChange}
              placeholder="e.g., Chiefs -3.5"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="betType">Bet Type *</label>
            <select
              id="betType"
              name="betType"
              className="form-control"
              value={formData.betType}
              onChange={handleChange}
              required
            >
              <option value="spread">Spread</option>
              <option value="moneyline">Moneyline</option>
              <option value="over">Over</option>
              <option value="under">Under</option>
              <option value="prop">Prop</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="units">Units *</label>
            <input
              type="number"
              id="units"
              name="units"
              className="form-control"
              value={formData.units}
              onChange={handleChange}
              min="0.1"
              step="0.1"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="odds">Odds (optional)</label>
          <input
            type="number"
            id="odds"
            name="odds"
            className="form-control"
            value={formData.odds || ''}
            onChange={handleChange}
            placeholder="e.g., -110 or +150"
            step="1"
          />
          <small>Enter as American odds (e.g., -110 for favorite, +150 for underdog)</small>
        </div>

        <div className="form-group">
          <label htmlFor="notes">Notes (optional)</label>
          <textarea
            id="notes"
            name="notes"
            className="form-control"
            value={formData.notes}
            onChange={handleChange}
            placeholder="Any additional notes about this pick..."
            rows={3}
          />
        </div>

        <button type="submit" className="btn">
          Add Pick
        </button>
      </form>
    </div>
  );
};

export default PickForm;
