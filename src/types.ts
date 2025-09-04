export interface Pick {
  id: string;
  week: number;
  date: string;
  team1: string;
  team2: string;
  pick: string;
  betType: BetType;
  units: number;
  odds?: number;
  result?: PickResult;
  notes?: string;
  createdAt: string;
}

export type BetType = 'spread' | 'moneyline' | 'over' | 'under' | 'prop';

export type PickResult = 'win' | 'loss' | 'push' | 'pending';

export interface SeasonStats {
  totalPicks: number;
  wins: number;
  losses: number;
  pushes: number;
  winRate: number;
  totalUnits: number;
  unitsWon: number;
  unitsLost: number;
  netUnits: number;
  roi: number;
}

export interface WeekStats {
  week: number;
  picks: number;
  wins: number;
  losses: number;
  pushes: number;
  unitsWon: number;
  unitsLost: number;
  netUnits: number;
}

export interface BetTypeStats {
  betType: BetType;
  picks: number;
  wins: number;
  losses: number;
  pushes: number;
  winRate: number;
  unitsWon: number;
  unitsLost: number;
  netUnits: number;
}
