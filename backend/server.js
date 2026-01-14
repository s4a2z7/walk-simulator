require('dotenv').config();
const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const cron = require('node-cron');
const pool = require('./config/database');

// Import routes
const authRoutes = require('./routes/auth');
const petRoutes = require('./routes/pet');
const rankingRoutes = require('./routes/ranking');
const statisticsRoutes = require('./routes/statistics');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3001',
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});

app.use('/api/', limiter);

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Phoenix Pet Backend is running',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/pet', petRoutes);
app.use('/api/ranking', rankingRoutes);
app.use('/api/statistics', statisticsRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    error: 'Route not found',
    path: req.path 
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// Daily reset cron job (runs at midnight)
cron.schedule('0 0 * * *', async () => {
  console.log('⏰ Running daily reset...');
  
  try {
    await pool.query(`
      UPDATE pets SET
        today_steps = 0,
        hunger_level = GREATEST(hunger_level - 10, 0),
        happiness_level = GREATEST(happiness_level - 5, 0),
        updated_at = NOW()
    `);
    
    console.log('✅ Daily reset completed successfully');
  } catch (error) {
    console.error('❌ Daily reset failed:', error);
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════╗
║   🔥 Phoenix Pet Backend Server 🔥       ║
║                                           ║
║   Port: ${PORT}                          ║
║   Environment: ${process.env.NODE_ENV || 'development'}            ║
║   Database: PostgreSQL                    ║
║                                           ║
║   API Endpoints:                          ║
║   - POST   /api/auth/register             ║
║   - POST   /api/auth/login                ║
║   - GET    /api/pet                       ║
║   - POST   /api/pet/steps                 ║
║   - POST   /api/pet/feed                  ║
║   - GET    /api/ranking                   ║
║   - GET    /api/statistics/today          ║
║                                           ║
║   Status: ✅ Running                      ║
╚═══════════════════════════════════════════╝
  `);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM signal received: closing HTTP server');
  await pool.end();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('SIGINT signal received: closing HTTP server');
  await pool.end();
  process.exit(0);
});

module.exports = app;
