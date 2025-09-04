import { Pick, SeasonStats, WeekStats, BetTypeStats } from './types';

const STORAGE_KEY = 'nfl-picks-data';

export const savePicks = (picks: Pick[]): void => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(picks));
};

export const loadPicks = (): Pick[] => {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch (error) {
      console.error('Error loading picks:', error);
      return [];
    }
  }
  return [];
};

export const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

export const exportToCSV = (picks: Pick[]): void => {
  if (picks.length === 0) {
    alert('No picks to export');
    return;
  }

  // Create CSV headers
  const headers = [
    'Week',
    'Date',
    'Team 1',
    'Team 2',
    'Pick',
    'Bet Type',
    'Units',
    'Odds',
    'Result',
    'Notes',
    'Created At'
  ];

  // Create CSV rows
  const rows = picks.map(pick => [
    pick.week,
    pick.date,
    pick.team1,
    pick.team2,
    pick.pick,
    pick.betType,
    pick.units,
    pick.odds || '',
    pick.result || 'pending',
    pick.notes || '',
    pick.createdAt
  ]);

  // Combine headers and rows
  const csvContent = [headers, ...rows]
    .map(row => row.map(cell => `"${cell}"`).join(','))
    .join('\n');

  // Create and download file
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `nfl-picks-${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

export const exportStatsToCSV = (picks: Pick[]): void => {
  const seasonStats = calculateSeasonStats(picks);
  const weekStats = Array.from(new Set(picks.map(pick => pick.week)))
    .sort((a, b) => a - b)
    .map(week => calculateWeekStats(picks, week));
  const betTypeStats = calculateBetTypeStats(picks);

  // Season stats
  const seasonHeaders = ['Metric', 'Value'];
  const seasonRows = [
    ['Total Picks', seasonStats.totalPicks],
    ['Wins', seasonStats.wins],
    ['Losses', seasonStats.losses],
    ['Pushes', seasonStats.pushes],
    ['Win Rate', `${seasonStats.winRate.toFixed(1)}%`],
    ['Total Units Wagered', seasonStats.totalUnits],
    ['Units Won', seasonStats.unitsWon],
    ['Units Lost', seasonStats.unitsLost],
    ['Net Units', seasonStats.netUnits],
    ['ROI', `${seasonStats.roi.toFixed(1)}%`]
  ];

  // Week stats
  const weekHeaders = ['Week', 'Picks', 'Wins', 'Losses', 'Pushes', 'Win Rate', 'Units Won', 'Units Lost', 'Net Units'];
  const weekRows = weekStats.map(stat => [
    stat.week,
    stat.picks,
    stat.wins,
    stat.losses,
    stat.pushes,
    stat.picks > 0 ? `${((stat.wins / stat.picks) * 100).toFixed(1)}%` : '0%',
    stat.unitsWon,
    stat.unitsLost,
    stat.netUnits
  ]);

  // Bet type stats
  const betTypeHeaders = ['Bet Type', 'Picks', 'Wins', 'Losses', 'Pushes', 'Win Rate', 'Units Won', 'Units Lost', 'Net Units'];
  const betTypeRows = betTypeStats
    .filter(stat => stat.picks > 0)
    .map(stat => [
      stat.betType,
      stat.picks,
      stat.wins,
      stat.losses,
      stat.pushes,
      `${stat.winRate.toFixed(1)}%`,
      stat.unitsWon,
      stat.unitsLost,
      stat.netUnits
    ]);

  // Combine all data
  const csvContent = [
    'SEASON STATISTICS',
    seasonHeaders.join(','),
    ...seasonRows.map(row => row.map(cell => `"${cell}"`).join(',')),
    '',
    'WEEKLY PERFORMANCE',
    weekHeaders.join(','),
    ...weekRows.map(row => row.map(cell => `"${cell}"`).join(',')),
    '',
    'BET TYPE PERFORMANCE',
    betTypeHeaders.join(','),
    ...betTypeRows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n');

  // Create and download file
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `nfl-stats-${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

export const calculateSeasonStats = (picks: Pick[]): SeasonStats => {
  const completedPicks = picks.filter(pick => pick.result && pick.result !== 'pending');
  
  const wins = completedPicks.filter(pick => pick.result === 'win').length;
  const losses = completedPicks.filter(pick => pick.result === 'loss').length;
  const pushes = completedPicks.filter(pick => pick.result === 'push').length;
  const totalPicks = completedPicks.length;
  
  const unitsWon = completedPicks
    .filter(pick => pick.result === 'win')
    .reduce((sum, pick) => {
      if (pick.odds) {
        // Calculate winnings based on odds
        if (pick.odds > 0) {
          return sum + (pick.units * pick.odds / 100);
        } else {
          return sum + (pick.units * 100 / Math.abs(pick.odds));
        }
      }
      return sum + pick.units; // Default to 1:1 payout
    }, 0);
    
  const unitsLost = completedPicks
    .filter(pick => pick.result === 'loss')
    .reduce((sum, pick) => sum + pick.units, 0);
    
  const totalUnits = completedPicks.reduce((sum, pick) => sum + pick.units, 0);
  const netUnits = unitsWon - unitsLost;
  const winRate = totalPicks > 0 ? (wins / totalPicks) * 100 : 0;
  const roi = totalUnits > 0 ? (netUnits / totalUnits) * 100 : 0;
  
  return {
    totalPicks,
    wins,
    losses,
    pushes,
    winRate,
    totalUnits,
    unitsWon,
    unitsLost,
    netUnits,
    roi
  };
};

export const calculateWeekStats = (picks: Pick[], week: number): WeekStats => {
  const weekPicks = picks.filter(pick => pick.week === week && pick.result && pick.result !== 'pending');
  
  const wins = weekPicks.filter(pick => pick.result === 'win').length;
  const losses = weekPicks.filter(pick => pick.result === 'loss').length;
  const pushes = weekPicks.filter(pick => pick.result === 'push').length;
  
  const unitsWon = weekPicks
    .filter(pick => pick.result === 'win')
    .reduce((sum, pick) => {
      if (pick.odds) {
        if (pick.odds > 0) {
          return sum + (pick.units * pick.odds / 100);
        } else {
          return sum + (pick.units * 100 / Math.abs(pick.odds));
        }
      }
      return sum + pick.units;
    }, 0);
    
  const unitsLost = weekPicks
    .filter(pick => pick.result === 'loss')
    .reduce((sum, pick) => sum + pick.units, 0);
    
  return {
    week,
    picks: weekPicks.length,
    wins,
    losses,
    pushes,
    unitsWon,
    unitsLost,
    netUnits: unitsWon - unitsLost
  };
};

export const calculateBetTypeStats = (picks: Pick[]): BetTypeStats[] => {
  const betTypes = ['spread', 'moneyline', 'over', 'under', 'prop'] as const;
  
  return betTypes.map(betType => {
    const typePicks = picks.filter(pick => 
      pick.betType === betType && pick.result && pick.result !== 'pending'
    );
    
    const wins = typePicks.filter(pick => pick.result === 'win').length;
    const losses = typePicks.filter(pick => pick.result === 'loss').length;
    const pushes = typePicks.filter(pick => pick.result === 'push').length;
    
    const unitsWon = typePicks
      .filter(pick => pick.result === 'win')
      .reduce((sum, pick) => {
        if (pick.odds) {
          if (pick.odds > 0) {
            return sum + (pick.units * pick.odds / 100);
          } else {
            return sum + (pick.units * 100 / Math.abs(pick.odds));
          }
        }
        return sum + pick.units;
      }, 0);
      
    const unitsLost = typePicks
      .filter(pick => pick.result === 'loss')
      .reduce((sum, pick) => sum + pick.units, 0);
      
    return {
      betType,
      picks: typePicks.length,
      wins,
      losses,
      pushes,
      winRate: typePicks.length > 0 ? (wins / typePicks.length) * 100 : 0,
      unitsWon,
      unitsLost,
      netUnits: unitsWon - unitsLost
    };
  });
};

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(amount);
};

export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`;
};

export const getCurrentWeek = (): number => {
  // This is a simplified calculation - you might want to update this based on actual NFL schedule
  const startDate = new Date('2024-09-05'); // NFL season start
  const now = new Date();
  const weeksSinceStart = Math.floor((now.getTime() - startDate.getTime()) / (7 * 24 * 60 * 60 * 1000));
  return Math.max(1, Math.min(18, weeksSinceStart + 1)); // NFL has 18 weeks
};
