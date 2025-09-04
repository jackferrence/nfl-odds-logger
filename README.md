# NFL Picks Tracker

A comprehensive web application to track your NFL picks and units throughout the season. Built with React, TypeScript, and Vite.

## Features

- **Pick Management**: Add, edit, and delete picks with detailed information
- **Unit Tracking**: Track units won/lost with automatic calculations
- **Multiple Bet Types**: Support for spread, moneyline, over/under, and prop bets
- **Odds Integration**: Optional odds input for accurate payout calculations
- **Statistics**: Comprehensive season and weekly statistics
- **Filtering**: Filter picks by week and result
- **Responsive Design**: Works on desktop and mobile devices
- **Local Storage**: Data persists between sessions

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:

```bash
npm install
```

### Running the Application

Start the development server:

```bash
npm run dev
```

The application will open in your browser at `http://localhost:3000`

### Building for Production

To create a production build:

```bash
npm run build
```

## Usage

### Adding Picks

1. Click on the "Add Pick" tab
2. Fill in the required information:
   - **Week**: Current NFL week (1-18)
   - **Date**: Date of the game
   - **Teams**: Home and away teams
   - **Pick**: Your specific pick (e.g., "Chiefs -3.5")
   - **Bet Type**: Spread, moneyline, over, under, or prop
   - **Units**: Amount wagered (can use decimals)
   - **Odds**: Optional American odds for accurate payout calculation
   - **Notes**: Optional additional information

### Managing Picks

1. Go to the "All Picks" tab
2. Use the filters to view specific weeks or results
3. Update pick results using the dropdown (Pending → Win/Loss/Push)
4. Delete picks using the delete button

### Viewing Statistics

- **Overview**: Season summary with key metrics
- **Weekly Performance**: Breakdown by week
- **Bet Type Performance**: Analysis by bet type
- **All Picks**: Complete list with filtering options

## Data Storage

All data is stored locally in your browser's localStorage. This means:
- Data persists between sessions
- Data is private and not shared
- Clearing browser data will remove your picks

## Features in Detail

### Unit Calculations

The app automatically calculates:
- Units won based on odds and bet type
- Net units (units won - units lost)
- ROI (Return on Investment)
- Win rate percentage

### Odds Support

When you enter American odds:
- Positive odds (+150): Win $150 on $100 bet
- Negative odds (-110): Risk $110 to win $100

### Bet Types

- **Spread**: Point spread bets
- **Moneyline**: Straight up winner bets
- **Over/Under**: Total points bets
- **Prop**: Proposition bets

## Customization

You can customize the application by modifying:
- `src/index.css`: Styling and appearance
- `src/utils.ts`: Calculation logic
- `src/types.ts`: Data structures

## Browser Compatibility

This application works in all modern browsers:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **Data not saving**: Check if localStorage is enabled in your browser
2. **Build errors**: Make sure all dependencies are installed
3. **Port conflicts**: The app will automatically find an available port

### Support

If you encounter any issues, check the browser console for error messages.

## License

This project is open source and available under the MIT License.

---

**Happy tracking! 🏈**
