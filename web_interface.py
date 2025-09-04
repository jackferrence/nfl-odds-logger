#!/usr/bin/env python3
"""
NFL Odds Logger - Web Interface
Provides a clean dashboard for viewing odds data with line movement graphs
"""

import os
import json
import glob
import pandas as pd
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import pytz

app = Flask(__name__)

# HTML Template with improved formatting and interactive graphs
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NFL Odds Logger Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 { 
            font-size: 2.5rem; 
            margin-bottom: 10px; 
        }
        .header p { 
            font-size: 1.1rem; 
            opacity: 0.9; 
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card { 
            background: white; 
            padding: 25px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #667eea;
        }
        .stat-value { 
            font-size: 2rem; 
            font-weight: bold; 
            color: #667eea; 
            margin-bottom: 5px; 
        }
        .stat-label { 
            color: #666; 
            font-size: 0.9rem; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
        }
        .status { 
            padding: 15px 20px; 
            border-radius: 8px; 
            margin-bottom: 30px; 
            font-weight: 500;
        }
        .status.running { 
            background: #d4edda; 
            color: #155724; 
            border: 1px solid #c3e6cb; 
        }
        .refresh-btn { 
            background: #667eea; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            border-radius: 6px; 
            cursor: pointer; 
            margin-bottom: 30px; 
            font-size: 1rem;
            transition: background 0.3s;
        }
        .refresh-btn:hover { 
            background: #5a6fd8; 
        }
        .games-container {
            display: grid;
            gap: 25px;
            margin-bottom: 30px;
        }
        .game-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .game-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        .game-card.expanded {
            transform: none;
        }
        .game-header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .game-actions {
            display: flex;
            gap: 10px;
        }
        .graph-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.2s;
        }
        .graph-btn:hover {
            background: #5a6fd8;
        }
        .game-teams {
            font-size: 1.3rem;
            font-weight: bold;
        }
        .game-time {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        .game-content {
            padding: 20px;
        }
        .game-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .bet-type-section {
            margin-bottom: 25px;
        }
        .bet-type-title {
            font-size: 1.1rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #ecf0f1;
        }
        .bookmakers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        .bookmaker-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 3px solid #667eea;
        }
        .bookmaker-name {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .odds-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }
        .odds-row:last-child {
            border-bottom: none;
        }
        .team-name {
            font-weight: 500;
            color: #495057;
        }
        .odds-value {
            font-weight: bold;
            color: #667eea;
        }
        .point-value {
            color: #6c757d;
            font-size: 0.9rem;
        }
        .game-details {
            display: none;
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }
        .game-details.expanded {
            display: block;
        }
        .graph-tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        .graph-tab {
            padding: 12px 24px;
            background: none;
            border: none;
            cursor: pointer;
            font-weight: 500;
            color: #6c757d;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
        }
        .graph-tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        .graph-tab:hover {
            color: #495057;
        }
        .graph-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .graph-placeholder {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-style: italic;
        }
        .last-updated {
            text-align: center;
            color: #6c757d;
            font-size: 0.9rem;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }
        .no-data {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-style: italic;
        }
        .expand-icon {
            margin-left: 10px;
            transition: transform 0.3s;
        }
        .expand-icon.expanded {
            transform: rotate(180deg);
        }
        .odds-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        .bet-column {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 3px solid #667eea;
        }
        .bet-header {
            font-size: 1rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 2px solid #ecf0f1;
            text-align: center;
        }
        .bookmaker-row {
            margin-bottom: 10px;
            padding: 8px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }
        .bookmaker-name {
            font-weight: bold;
            color: #495057;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .odds-display {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 0;
            font-size: 0.9rem;
        }
        .team-name {
            font-weight: 500;
            color: #495057;
            flex: 1;
        }
        .odds-values {
            text-align: right;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        .odds-value {
            font-weight: bold;
            color: #667eea;
            font-size: 0.9rem;
        }
        .point-value {
            color: #6c757d;
            font-size: 0.8rem;
            margin-top: 2px;
        }
        .no-odds {
            text-align: center;
            padding: 15px;
            color: #6c757d;
            font-style: italic;
            font-size: 0.9rem;
        }
        .movement-section {
            background: #e8f4fd;
            border-radius: 6px;
            padding: 10px;
            margin-bottom: 15px;
            border-left: 3px solid #17a2b8;
        }
        .movement-bookmaker {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .movement-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0;
            border-bottom: 1px solid #dee2e6;
            font-size: 0.85rem;
        }
        .movement-row:last-child {
            border-bottom: none;
        }
        .movement-row.moved-up {
            background: rgba(40, 167, 69, 0.1);
            border-left: 2px solid #28a745;
        }
        .movement-row.moved-down {
            background: rgba(220, 53, 69, 0.1);
            border-left: 2px solid #dc3545;
        }
        .movement-team {
            font-weight: 500;
            color: #495057;
            flex: 1;
        }
        .movement-odds {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .current-odds {
            font-weight: bold;
            color: #667eea;
            font-size: 0.85rem;
        }
        .movement-arrow {
            font-size: 0.75rem;
            color: #6c757d;
        }
        .previous-odds {
            font-size: 0.75rem;
            color: #6c757d;
        }
        .point-display {
            font-size: 0.75rem;
            color: #6c757d;
        }
        .point-up {
            color: #28a745;
            font-weight: bold;
        }
        .point-down {
            color: #dc3545;
            font-weight: bold;
        }
        .main-tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #e9ecef;
        }
        .main-tab {
            padding: 15px 30px;
            background: none;
            border: none;
            cursor: pointer;
            font-weight: 500;
            color: #6c757d;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
            font-size: 1rem;
        }
        .main-tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        .main-tab:hover {
            color: #495057;
        }
        .main-content {
            min-height: 400px;
        }
        .data-files-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            padding: 30px;
        }
        .data-section {
            margin-bottom: 40px;
        }
        .data-section h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }
        .file-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .file-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 3px solid #667eea;
            transition: transform 0.2s;
        }
        .file-card:hover {
            transform: translateY(-2px);
        }
        .file-name {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        .file-info {
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }
        .file-actions {
            display: flex;
            gap: 10px;
        }
        .file-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
            text-decoration: none;
            display: inline-block;
        }
        .file-btn.download {
            background: #667eea;
            color: white;
        }
        .file-btn.download:hover {
            background: #5a6fd8;
        }
        .file-btn.view {
            background: #28a745;
            color: white;
        }
        .file-btn.view:hover {
            background: #218838;
        }
        .no-files {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-style: italic;
        }

    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏈 NFL Odds Logger Dashboard</h1>
            <p>Real-time odds tracking and line movement analysis</p>
        </div>
        
        <div class="status running">
            ✅ Service is running - Last updated: {{ last_update }}
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{{ total_games }}</div>
                <div class="stat-label">Active Games</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ total_odds }}</div>
                <div class="stat-label">Total Odds</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ api_calls }}</div>
                <div class="stat-label">API Calls This Month</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ remaining_calls }}</div>
                <div class="stat-label">Remaining Calls</div>
            </div>
        </div>
        
        <div class="main-tabs">
            <button class="main-tab active" onclick="showMainTab('games')">Games & Odds</button>
            <button class="main-tab" onclick="showMainTab('data')">Data Files</button>
        </div>
        
        <div class="main-content" id="games-content">
            <div class="games-container">
                {{ games_html|safe }}
            </div>
        </div>
        
        <div class="main-content" id="data-content" style="display: none;">
            <div class="data-files-container">
                {{ data_files_html|safe }}
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/download/latest" class="refresh-btn" style="text-decoration: none; display: inline-block;">
                📥 Download Latest CSV
            </a>
        </div>
    </div>

    <script>
        // Toggle main tabs
        function showMainTab(tabName) {
            // Hide all main content
            const contents = document.querySelectorAll('.main-content');
            const tabs = document.querySelectorAll('.main-tab');
            
            contents.forEach(content => content.style.display = 'none');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected content and activate tab
            document.getElementById(`${tabName}-content`).style.display = 'block';
            event.target.classList.add('active');
        }

        // Toggle game expansion
        function toggleGame(gameId) {
            const gameCard = document.getElementById(`game-${gameId}`);
            const gameDetails = document.getElementById(`details-${gameId}`);
            const expandIcon = document.getElementById(`expand-${gameId}`);
            
            if (gameDetails.classList.contains('expanded')) {
                gameDetails.classList.remove('expanded');
                gameCard.classList.remove('expanded');
                expandIcon.classList.remove('expanded');
                expandIcon.textContent = '▼';
            } else {
                gameDetails.classList.add('expanded');
                gameCard.classList.add('expanded');
                expandIcon.classList.add('expanded');
                expandIcon.textContent = '▲';
                
                // Load graphs if not already loaded
                if (!gameDetails.dataset.graphsLoaded) {
                    loadGameGraphs(gameId);
                    gameDetails.dataset.graphsLoaded = 'true';
                }
            }
        }

        // Toggle graph tabs
        function showGraphTab(gameId, tabName, event) {
            // Prevent the click from bubbling up to the game card
            event.stopPropagation();
            
            // Hide all tabs
            const tabs = document.querySelectorAll(`[data-game="${gameId}"] .graph-tab`);
            const contents = document.querySelectorAll(`[data-game="${gameId}"] .graph-content`);
            
            tabs.forEach(tab => tab.classList.remove('active'));
            contents.forEach(content => content.style.display = 'none');
            
            // Show selected tab
            document.getElementById(`tab-${gameId}-${tabName}`).classList.add('active');
            document.getElementById(`content-${gameId}-${tabName}`).style.display = 'block';
        }

        // Load game graphs
        function loadGameGraphs(gameId) {
            fetch(`/api/game/${gameId}/graphs`)
                .then(response => response.json())
                .then(data => {
                    if (data.spreads) createSpreadChart(gameId, data.spreads);
                    if (data.moneyline_favorite) createMoneylineFavoriteChart(gameId, data.moneyline_favorite);
                    if (data.moneyline_underdog) createMoneylineUnderdogChart(gameId, data.moneyline_underdog);
                    if (data.totals) createTotalsChart(gameId, data.totals);
                })
                .catch(error => {
                    console.error('Error loading graphs:', error);
                    document.getElementById(`content-${gameId}-spreads`).innerHTML = 
                        '<div class="graph-placeholder">Error loading line movement data</div>';
                });
        }

        // Create spread chart with improved display
        function createSpreadChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-spreads`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                
                if (data[bookmaker] && data[bookmaker].length > 0) {
                    datasets.push({
                        label: bookmaker,
                        data: data[bookmaker].map(point => point.point),
                        borderColor: color,
                        backgroundColor: color + '20',
                        tension: 0.1,
                        pointRadius: 3,
                        pointHoverRadius: 5
                    });
                }
            });

            // Get time labels from the first bookmaker with data
            const firstBookmaker = Object.keys(data)[0];
            const timeLabels = data[firstBookmaker]?.map(point => point.time) || [];

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: timeLabels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Point Spread Movement (Higher = Favorite, Lower = Underdog)'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            reverse: false,
                            title: {
                                display: true,
                                text: 'Point Spread'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }

        // Create moneyline favorite chart
        function createMoneylineFavoriteChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-moneyline-favorite`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                
                if (data[bookmaker] && data[bookmaker].length > 0) {
                    datasets.push({
                        label: bookmaker,
                        data: data[bookmaker].map(point => point.price),
                        borderColor: color,
                        backgroundColor: color + '20',
                        tension: 0.1,
                        pointRadius: 3,
                        pointHoverRadius: 5
                    });
                }
            });

            // Get time labels from the first bookmaker with data
            const firstBookmaker = Object.keys(data)[0];
            const timeLabels = data[firstBookmaker]?.map(point => point.time) || [];

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: timeLabels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Moneyline Favorite Movement'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            reverse: false,
                            title: {
                                display: true,
                                text: 'Favorite Odds'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }

        // Create moneyline underdog chart
        function createMoneylineUnderdogChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-moneyline-underdog`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                
                if (data[bookmaker] && data[bookmaker].length > 0) {
                    datasets.push({
                        label: bookmaker,
                        data: data[bookmaker].map(point => point.price),
                        borderColor: color,
                        backgroundColor: color + '20',
                        tension: 0.1,
                        pointRadius: 3,
                        pointHoverRadius: 5
                    });
                }
            });

            // Get time labels from the first bookmaker with data
            const firstBookmaker = Object.keys(data)[0];
            const timeLabels = data[firstBookmaker]?.map(point => point.time) || [];

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: timeLabels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Moneyline Underdog Movement'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            reverse: false,
                            title: {
                                display: true,
                                text: 'Underdog Odds'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }

        // Create moneyline chart
        function createMoneylineChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-moneyline`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                
                if (data[bookmaker] && data[bookmaker].length > 0) {
                    datasets.push({
                        label: bookmaker,
                        data: data[bookmaker].map(point => point.price),
                        borderColor: color,
                        backgroundColor: color + '20',
                        tension: 0.1,
                        pointRadius: 3,
                        pointHoverRadius: 5
                    });
                }
            });

            // Get time labels from the first bookmaker with data
            const firstBookmaker = Object.keys(data)[0];
            const timeLabels = data[firstBookmaker]?.map(point => point.time) || [];

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: timeLabels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Moneyline Movement'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            title: {
                                display: true,
                                text: 'Odds'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }

        // Create totals chart
        function createTotalsChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-totals`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                datasets.push({
                    label: bookmaker,
                    data: data[bookmaker].map(point => point.point),
                    borderColor: color,
                    backgroundColor: color + '20',
                    tension: 0.1,
                    pointRadius: 3,
                    pointHoverRadius: 5
                });
            });

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data[Object.keys(data)[0]]?.map(point => point.time) || [],
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Total Points Movement'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            title: {
                                display: true,
                                text: 'Total Points'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }
    </script>
</body>
</html>
"""

def format_timestamp(timestamp_str):
    """Convert ISO timestamp to readable format"""
    try:
        # Parse the timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        # Convert to local timezone (you can change this)
        local_tz = pytz.timezone('America/New_York')
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime("%B %d, %Y at %I:%M %p ET")
    except:
        return timestamp_str

def format_game_time(commence_time):
    """Format game start time"""
    try:
        # Parse the commence time
        dt = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
        # Convert to local timezone
        local_tz = pytz.timezone('America/New_York')
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime("%A, %B %d at %I:%M %p ET")
    except:
        return commence_time

def format_time_for_chart(timestamp_str):
    """Format timestamp for chart display"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        local_tz = pytz.timezone('America/New_York')
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime("%m/%d %H:%M")
    except:
        return timestamp_str

def organize_data_by_games(df):
    """Organize odds data by games"""
    games = {}
    
    for _, row in df.iterrows():
        game_id = row['game_id']
        home_team = row['home_team']
        away_team = row['away_team']
        commence_time = row['commence_time']
        bookmaker = row['bookmaker']
        market = row['market']
        outcome_name = row['outcome_name']
        price = row['price']
        point = row['point']
        timestamp = row['timestamp']
        
        if game_id not in games:
            games[game_id] = {
                'home_team': home_team,
                'away_team': away_team,
                'commence_time': commence_time,
                'bookmakers': {},
                'historical_data': {}
            }
        
        if bookmaker not in games[game_id]['bookmakers']:
            games[game_id]['bookmakers'][bookmaker] = {}
        
        if market not in games[game_id]['bookmakers'][bookmaker]:
            games[game_id]['bookmakers'][bookmaker][market] = []
        
        games[game_id]['bookmakers'][bookmaker][market].append({
            'outcome_name': outcome_name,
            'price': price,
            'point': point
        })
        
        # Store historical data for graphs
        if bookmaker not in games[game_id]['historical_data']:
            games[game_id]['historical_data'][bookmaker] = {}
        
        if market not in games[game_id]['historical_data'][bookmaker]:
            games[game_id]['historical_data'][bookmaker][market] = []
        
        games[game_id]['historical_data'][bookmaker][market].append({
            'timestamp': timestamp,
            'outcome_name': outcome_name,
            'price': price,
            'point': point
        })
    
    return games

def generate_games_html(games):
    """Generate HTML for games display with interactive graphs"""
    if not games:
        return '<div class="no-data">No games data available yet. The logger will start collecting data soon.</div>'
    
    html_parts = []
    
    for game_id, game_data in games.items():
        # Game header
        game_html = f'''
        <div class="game-card" id="game-{game_id}">
            <div class="game-header">
                <div class="game-teams">{game_data['away_team']} @ {game_data['home_team']}</div>
                <div class="game-time">{format_game_time(game_data['commence_time'])}</div>
                <div class="game-actions">
                    <button class="graph-btn" onclick="toggleGame('{game_id}')">📊 View Graphs</button>
                </div>
            </div>
            <div class="game-content">
                <div class="odds-grid">
        '''
        
        # Get previous odds for movement comparison
        previous_odds = get_previous_odds(game_id, game_data['bookmakers'])
        
        # Create columns for each bet type
        bet_types = ['spreads', 'h2h', 'totals']
        bet_type_labels = ['Point Spread', 'Moneyline', 'Total']
        
        for i, (bet_type, label) in enumerate(zip(bet_types, bet_type_labels)):
            game_html += f'<div class="bet-column">'
            game_html += f'<div class="bet-header">{label}</div>'
            
            # Get all bookmakers for this bet type
            bookmakers_for_type = {}
            for bookmaker, markets in game_data['bookmakers'].items():
                if bet_type in markets:
                    bookmakers_for_type[bookmaker] = markets[bet_type]
            
            if bookmakers_for_type:
                # Calculate movement for this bet type
                movement_data = calculate_movement(game_data['bookmakers'], previous_odds, bet_type)
                movement_html = format_movement_display(movement_data, bet_type)
                
                if movement_html:
                    game_html += f'<div class="movement-section">{movement_html}</div>'
                
                for bookmaker, odds in bookmakers_for_type.items():
                    game_html += f'<div class="bookmaker-row">'
                    game_html += f'<div class="bookmaker-name">{bookmaker}</div>'
                    
                    # Display odds for this bookmaker
                    for odd in odds:
                        team_name = odd['outcome_name']
                        price = odd['price']
                        point = odd['point']
                        
                        # Format price
                        if price > 0:
                            price_display = f"+{price}"
                        else:
                            price_display = str(price)
                        
                        # Format point (for spreads/totals)
                        point_display = ""
                        if pd.notna(point) and point != "":
                            if bet_type == 'totals':
                                point_display = f"O/U {point}"
                            else:
                                point_display = f"({point})"
                        
                        game_html += f'''
                        <div class="odds-display">
                            <span class="team-name">{team_name}</span>
                            <div class="odds-values">
                                <span class="odds-value">{price_display}</span>
                                <span class="point-value">{point_display}</span>
                            </div>
                        </div>
                        '''
                    
                    game_html += '</div>'  # Close bookmaker-row
            else:
                game_html += '<div class="no-odds">No data</div>'
            
            game_html += '</div>'  # Close bet-column
        
        game_html += '</div>'  # Close odds-grid
        game_html += '</div>'  # Close game-content
        
        # Add expandable details section with graphs
        game_html += f'''
        <div class="game-details" id="details-{game_id}" data-game="{game_id}">
            <div class="graph-tabs">
                <button class="graph-tab active" id="tab-{game_id}-spreads" onclick="showGraphTab('{game_id}', 'spreads', event)">
                    Point Spreads
                </button>
                <button class="graph-tab" id="tab-{game_id}-moneyline-favorite" onclick="showGraphTab('{game_id}', 'moneyline-favorite', event)">
                    ML Favorite
                </button>
                <button class="graph-tab" id="tab-{game_id}-moneyline-underdog" onclick="showGraphTab('{game_id}', 'moneyline-underdog', event)">
                    ML Underdog
                </button>
                <button class="graph-tab" id="tab-{game_id}-totals" onclick="showGraphTab('{game_id}', 'totals', event)">
                    Totals
                </button>
            </div>
            
            <div class="graph-content" id="content-{game_id}-spreads" style="display: block;">
                <div class="graph-container">
                    <canvas id="chart-{game_id}-spreads"></canvas>
                </div>
            </div>
            
            <div class="graph-content" id="content-{game_id}-moneyline-favorite" style="display: none;">
                <div class="graph-container">
                    <canvas id="chart-{game_id}-moneyline-favorite"></canvas>
                </div>
            </div>
            
            <div class="graph-content" id="content-{game_id}-moneyline-underdog" style="display: none;">
                <div class="graph-container">
                    <canvas id="chart-{game_id}-moneyline-underdog"></canvas>
                </div>
            </div>
            
            <div class="graph-content" id="content-{game_id}-totals" style="display: none;">
                <div class="graph-container">
                    <canvas id="chart-{game_id}-totals"></canvas>
                </div>
            </div>
        </div>
        '''
        
        game_html += '</div>'  # Close game-card
        html_parts.append(game_html)
    
    return '\n'.join(html_parts)

def generate_data_files_html():
    """Generate HTML for data files view"""
    # Get all CSV files
    csv_files = glob.glob("*.csv")
    
    if not csv_files:
        return '<div class="no-files">No data files found yet. Start collecting data to see files here.</div>'
    
    html_parts = []
    
    # Daily files section
    if csv_files:
        html_parts.append('<div class="data-section">')
        html_parts.append('<h3>📅 Daily Data Files</h3>')
        html_parts.append('<div class="file-grid">')
        
        for csv_file in sorted(csv_files, reverse=True):
            try:
                file_size = os.path.getsize(csv_file)
                file_time = datetime.fromtimestamp(os.path.getctime(csv_file))
                
                html_parts.append(f'''
                <div class="file-card">
                    <div class="file-name">{csv_file}</div>
                    <div class="file-info">
                        📊 Size: {file_size:,} bytes<br>
                        📅 Created: {file_time.strftime('%Y-%m-%d %H:%M:%S')}
                    </div>
                    <div class="file-actions">
                        <a href="/download/file/{csv_file}" class="file-btn download">📥 Download</a>
                        <a href="/view/file/{csv_file}" class="file-btn view">👁️ View</a>
                    </div>
                </div>
                ''')
            except:
                continue
        
        html_parts.append('</div>')
        html_parts.append('</div>')
    
    return '\n'.join(html_parts)

def save_game_specific_data(df):
    """Save data to game-specific CSV files for permanent storage"""
    if df is None or df.empty:
        return
    
    # Create games directory if it doesn't exist
    games_dir = "games"
    if not os.path.exists(games_dir):
        os.makedirs(games_dir)
    
    # Group data by game_id
    for game_id in df['game_id'].unique():
        game_data = df[df['game_id'] == game_id]
        
        if not game_data.empty:
            # Get game info for filename
            home_team = game_data['home_team'].iloc[0]
            away_team = game_data['away_team'].iloc[0]
            commence_time = game_data['commence_time'].iloc[0]
            
            # Parse commence time for date
            try:
                game_date = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
                date_str = game_date.strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            # Create filename: games/YYYY-MM-DD_away_home_gameid.csv
            safe_away = away_team.replace(' ', '_').replace('&', 'and')
            safe_home = home_team.replace(' ', '_').replace('&', 'and')
            filename = f"{date_str}_{safe_away}_at_{safe_home}_{game_id}.csv"
            filepath = os.path.join(games_dir, filename)
            
            # Append to existing file or create new one
            if os.path.exists(filepath):
                # Append new data to existing file
                game_data.to_csv(filepath, mode='a', header=False, index=False)
            else:
                # Create new file with headers
                game_data.to_csv(filepath, index=False)
            
            print(f"💾 Saved game data: {filename}")

def get_historical_data_for_game(game_id):
    """Get historical data for a specific game from all CSV files"""
    csv_files = glob.glob("nfl_odds_*.csv")
    if not csv_files:
        return None
    
    all_data = []
    
    for csv_file in sorted(csv_files):
        try:
            df = pd.read_csv(csv_file)
            game_data = df[df['game_id'] == game_id]
            if not game_data.empty:
                all_data.append(game_data)
        except:
            continue
    
    if not all_data:
        return None
    
    # Combine all data and sort by timestamp
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('timestamp')
    
    return combined_df

def organize_graph_data(df, game_id):
    """Organize data for graph display"""
    if df is None or df.empty:
        return None
    
    # Filter for the specific game
    game_data = df[df['game_id'] == game_id]
    if game_data.empty:
        return None
    
    # Get home and away team names
    home_team = game_data['home_team'].iloc[0]
    away_team = game_data['away_team'].iloc[0]
    
    # Organize by market type
    spreads_data = {}
    moneyline_favorite_data = {}
    moneyline_underdog_data = {}
    totals_data = {}
    
    # Track unique timestamps for proper time progression
    all_timestamps = []
    
    for _, row in game_data.iterrows():
        bookmaker = row['bookmaker']
        market = row['market']
        timestamp = row['timestamp']
        outcome_name = row['outcome_name']
        price = row['price']
        point = row['point']
        
        # Store timestamp for later processing
        all_timestamps.append(timestamp)
        
        if market == 'spreads':
            if bookmaker not in spreads_data:
                spreads_data[bookmaker] = []
            
            # For spreads, use the point value as the main line
            if pd.notna(point) and point != "":
                spreads_data[bookmaker].append({
                    'timestamp': timestamp,
                    'point': float(point),
                    'team': outcome_name
                })
        
        elif market == 'h2h':
            # Separate favorite and underdog moneyline data
            if price < 0:  # Favorite (negative odds)
                if bookmaker not in moneyline_favorite_data:
                    moneyline_favorite_data[bookmaker] = []
                moneyline_favorite_data[bookmaker].append({
                    'timestamp': timestamp,
                    'price': price,
                    'team': outcome_name
                })
            else:  # Underdog (positive odds)
                if bookmaker not in moneyline_underdog_data:
                    moneyline_underdog_data[bookmaker] = []
                moneyline_underdog_data[bookmaker].append({
                    'timestamp': timestamp,
                    'price': price,
                    'team': outcome_name
                })
        
        elif market == 'totals':
            if bookmaker not in totals_data:
                totals_data[bookmaker] = []
            totals_data[bookmaker].append({
                'timestamp': timestamp,
                'point': float(point) if pd.notna(point) and point != "" else None,
                'price': price,
                'outcome': outcome_name
            })
    
    # Sort timestamps and create time labels
    unique_timestamps = sorted(list(set(all_timestamps)))
    time_labels = [format_time_for_chart(ts) for ts in unique_timestamps]
    
    # Process each data type to ensure proper time progression
    def process_data_for_time(data_dict):
        processed = {}
        for bookmaker, data_points in data_dict.items():
            # Sort by timestamp and create time-indexed data
            sorted_data = sorted(data_points, key=lambda x: x['timestamp'])
            processed[bookmaker] = []
            
            for i, data_point in enumerate(sorted_data):
                processed[bookmaker].append({
                    'time': time_labels[i] if i < len(time_labels) else time_labels[-1],
                    'point': data_point.get('point'),
                    'price': data_point.get('price'),
                    'team': data_point.get('team'),
                    'outcome': data_point.get('outcome')
                })
        return processed
    
    return {
        'spreads': process_data_for_time(spreads_data) if spreads_data else None,
        'moneyline_favorite': process_data_for_time(moneyline_favorite_data) if moneyline_favorite_data else None,
        'moneyline_underdog': process_data_for_time(moneyline_underdog_data) if moneyline_underdog_data else None,
        'totals': process_data_for_time(totals_data) if totals_data else None,
        'labels': time_labels
    }

def get_previous_odds(game_id, current_data):
    """Get previous odds for comparison"""
    csv_files = glob.glob("nfl_odds_*.csv")
    if not csv_files:
        return None
    
    # Sort files by date (oldest first) and get the second most recent
    sorted_files = sorted(csv_files, key=os.path.getctime)
    if len(sorted_files) < 2:
        return None
    
    previous_file = sorted_files[-2]  # Second most recent file
    
    try:
        df = pd.read_csv(previous_file)
        game_data = df[df['game_id'] == game_id]
        if game_data.empty:
            return None
        
        # Organize previous data similar to current data
        previous_odds = {}
        for _, row in game_data.iterrows():
            bookmaker = row['bookmaker']
            market = row['market']
            outcome_name = row['outcome_name']
            price = row['price']
            point = row['point']
            
            if bookmaker not in previous_odds:
                previous_odds[bookmaker] = {}
            
            if market not in previous_odds[bookmaker]:
                previous_odds[bookmaker][market] = []
            
            previous_odds[bookmaker][market].append({
                'outcome_name': outcome_name,
                'price': price,
                'point': point
            })
        
        return previous_odds
    except:
        return None

def calculate_movement(current_odds, previous_odds, bet_type):
    """Calculate the movement between current and previous odds"""
    if not previous_odds:
        return None
    
    movements = {}
    
    for bookmaker in current_odds:
        if bookmaker not in previous_odds:
            continue
            
        if bet_type not in current_odds[bookmaker] or bet_type not in previous_odds[bookmaker]:
            continue
        
        current_data = current_odds[bookmaker][bet_type]
        previous_data = previous_odds[bookmaker][bet_type]
        
        movements[bookmaker] = []
        
        for current_odd in current_data:
            team_name = current_odd['outcome_name']
            current_price = current_odd['price']
            current_point = current_odd['point']
            
            # Find matching previous odd
            previous_odd = None
            for prev in previous_data:
                if prev['outcome_name'] == team_name:
                    previous_odd = prev
                    break
            
            if previous_odd:
                prev_price = previous_odd['price']
                prev_point = previous_odd['point']
                
                # Calculate price movement
                price_change = current_price - prev_price
                price_change_pct = ((current_price - prev_price) / abs(prev_price)) * 100 if prev_price != 0 else 0
                
                # Calculate point movement (for spreads/totals)
                point_change = None
                if pd.notna(current_point) and pd.notna(prev_point) and current_point != "" and prev_point != "":
                    point_change = float(current_point) - float(prev_point)
                
                movements[bookmaker].append({
                    'team': team_name,
                    'current_price': current_price,
                    'previous_price': prev_price,
                    'price_change': price_change,
                    'price_change_pct': price_change_pct,
                    'current_point': current_point,
                    'previous_point': prev_point,
                    'point_change': point_change
                })
            else:
                # New team/line
                movements[bookmaker].append({
                    'team': team_name,
                    'current_price': current_price,
                    'previous_price': None,
                    'price_change': None,
                    'price_change_pct': None,
                    'current_point': current_point,
                    'previous_point': None,
                    'point_change': None
                })
    
    return movements

def format_movement_display(movement_data, bet_type):
    """Format movement data for display"""
    if not movement_data:
        return ""
    
    html_parts = []
    
    for bookmaker, movements in movement_data.items():
        html_parts.append(f'<div class="movement-bookmaker">{bookmaker}</div>')
        
        for movement in movements:
            team = movement['team']
            current_price = movement['current_price']
            previous_price = movement['previous_price']
            price_change = movement['price_change']
            price_change_pct = movement['price_change_pct']
            current_point = movement['current_point']
            previous_point = movement['previous_point']
            point_change = movement['point_change']
            
            # Format current price
            if current_price > 0:
                current_price_display = f"+{current_price}"
            else:
                current_price_display = str(current_price)
            
            # Format previous price
            if previous_price is not None:
                if previous_price > 0:
                    previous_price_display = f"+{previous_price}"
                else:
                    previous_price_display = str(previous_price)
            else:
                previous_price_display = "NEW"
            
            # Format point display
            point_display = ""
            if pd.notna(current_point) and current_point != "":
                if bet_type == 'totals':
                    point_display = f"O/U {current_point}"
                else:
                    point_display = f"({current_point})"
            
            # Determine movement direction and color
            movement_class = "no-change"
            movement_arrow = "→"
            
            if price_change is not None:
                if price_change > 0:
                    movement_class = "moved-up"
                    movement_arrow = "↗"
                elif price_change < 0:
                    movement_class = "moved-down"
                    movement_arrow = "↘"
            
            # Point movement for spreads/totals
            point_movement_display = ""
            if point_change is not None:
                if point_change > 0:
                    point_movement_display = f" <span class='point-up'>+{point_change:.1f}</span>"
                elif point_change < 0:
                    point_movement_display = f" <span class='point-down'>{point_change:.1f}</span>"
            
            html_parts.append(f'''
            <div class="movement-row {movement_class}">
                <div class="movement-team">{team}</div>
                <div class="movement-odds">
                    <span class="current-odds">{current_price_display}</span>
                    <span class="movement-arrow">{movement_arrow}</span>
                    <span class="previous-odds">{previous_price_display}</span>
                    <span class="point-display">{point_display}</span>
                    {point_movement_display}
                </div>
            </div>
            ''')
    
    return '\n'.join(html_parts)

def get_latest_csv_file():
    """Get the most recent CSV file"""
    csv_files = glob.glob("nfl_odds_*.csv")
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getctime)

def get_usage_stats():
    """Get API usage statistics"""
    try:
        if os.path.exists("api_usage.json"):
            with open("api_usage.json", "r") as f:
                data = json.load(f)
            
            now = datetime.now()
            current_month = now.strftime("%Y-%m")
            
            current_month_calls = [
                call for call in data["calls"]
                if call["date"].startswith(current_month)
            ]
            
            calls_this_month = len(current_month_calls)
            remaining = 500 - calls_this_month
            usage_percent = (calls_this_month / 500) * 100
            
            return {
                "calls": calls_this_month,
                "limit": 500,
                "remaining": remaining,
                "usage_percent": usage_percent
            }
    except:
        pass
    
    return {"calls": 0, "limit": 500, "remaining": 500, "usage_percent": 0}

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Get latest CSV file
    latest_file = get_latest_csv_file()
    
    if latest_file:
        try:
            # Read the latest CSV
            df = pd.read_csv(latest_file)
            
            # Organize data by games
            games = organize_data_by_games(df)
            
            # Generate games HTML
            games_html = generate_games_html(games)
            
            # Generate data files HTML
            data_files_html = generate_data_files_html()
            
            # Calculate stats
            total_games = len(games)
            total_odds = len(df)
            
            last_update = format_timestamp(datetime.fromtimestamp(os.path.getctime(latest_file)).isoformat())
            
        except Exception as e:
            total_games = 0
            total_odds = 0
            games_html = f'<div class="no-data">Error reading data: {str(e)}</div>'
            last_update = "Unknown"
    else:
        total_games = 0
        total_odds = 0
        games_html = '<div class="no-data">No data available yet. The logger will start collecting data soon.</div>'
        last_update = "No data"
    
    # Get usage stats
    usage_stats = get_usage_stats()
    
    return render_template_string(HTML_TEMPLATE,
        total_games=total_games,
        total_odds=total_odds,
        api_calls=usage_stats["calls"],
        remaining_calls=usage_stats["remaining"],
        games_html=games_html,
        data_files_html=data_files_html, # Pass data_files_html to the template
        last_update=last_update
    )

@app.route('/api/game/<game_id>/graphs')
def game_graphs(game_id):
    """API endpoint for game graph data"""
    try:
        # Get historical data for the game
        historical_df = get_historical_data_for_game(game_id)
        
        if historical_df is None:
            return jsonify({'error': 'No data found for this game'})
        
        # Organize data for graphs
        graph_data = organize_graph_data(historical_df, game_id)
        
        return jsonify(graph_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats"""
    latest_file = get_latest_csv_file()
    usage_stats = get_usage_stats()
    
    stats = {
        "total_games": 0,
        "total_odds": 0,
        "api_calls": usage_stats["calls"],
        "remaining_calls": usage_stats["remaining"],
        "usage_percent": usage_stats["usage_percent"],
        "last_update": "No data"
    }
    
    if latest_file:
        try:
            df = pd.read_csv(latest_file)
            games = organize_data_by_games(df)
            stats["total_games"] = len(games)
            stats["total_odds"] = len(df)
            stats["last_update"] = datetime.fromtimestamp(os.path.getctime(latest_file)).isoformat()
        except:
            pass
    
    return jsonify(stats)

@app.route('/download/latest')
def download_latest():
    """Download the latest CSV file"""
    latest_file = get_latest_csv_file()
    if latest_file:
        from flask import send_file
        return send_file(latest_file, as_attachment=True)
    else:
        return "No data available", 404

@app.route('/download/file/<filename>')
def download_specific_file(filename):
    """Download a specific CSV file"""
    filepath = os.path.join(".", filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return "File not found", 404

@app.route('/view/file/<filename>')
def view_specific_file(filename):
    """View a specific CSV file in the browser"""
    filepath = os.path.join(".", filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        return render_template_string(f"<pre>{content}</pre>")
    else:
        return "File not found", 404

if __name__ == '__main__':
    # Install required packages
    import subprocess
    import sys
    
    try:
        import flask
        import pandas
        import pytz
    except ImportError:
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "pandas", "pytz"])
    
    print("🌐 Starting web interface...")
    # Use Railway's PORT environment variable, default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    print(f"📊 Dashboard will be available at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
