const pool = require('../config/database');

// Get today's statistics
exports.getTodayStats = async (req, res) => {
  try {
    const today = new Date().toISOString().split('T')[0];

    // Get pet current status
    const petResult = await pool.query(
      `SELECT 
        today_steps,
        hunger_level,
        happiness_level
       FROM pets
       WHERE user_id = $1`,
      [req.userId]
    );

    if (petResult.rows.length === 0) {
      return res.status(404).json({ error: 'Pet not found' });
    }

    const pet = petResult.rows[0];

    // Get today's EXP gained
    const expResult = await pool.query(
      `SELECT COALESCE(SUM(exp_gained), 0) as total_exp
       FROM step_records
       WHERE user_id = $1 AND record_date = $2`,
      [req.userId, today]
    );

    // Get feeding count
    const feedingResult = await pool.query(
      `SELECT COUNT(*) as times_fed
       FROM feeding_records
       WHERE user_id = $1 AND DATE(fed_at) = $2`,
      [req.userId, today]
    );

    const goalSteps = 10000;
    const goalReached = pet.today_steps >= goalSteps;
    const progressPercentage = Math.min(100, Math.round((pet.today_steps / goalSteps) * 100));

    res.json({
      date: today,
      today_steps: pet.today_steps,
      exp_gained_today: parseInt(expResult.rows[0].total_exp),
      times_fed: parseInt(feedingResult.rows[0].times_fed),
      hunger_level: pet.hunger_level,
      happiness_level: pet.happiness_level,
      achievement: {
        reached_goal: goalReached,
        goal_steps: goalSteps,
        progress_percentage: progressPercentage
      }
    });

  } catch (error) {
    console.error('Get today stats error:', error);
    res.status(500).json({ error: 'Failed to get today stats', details: error.message });
  }
};

// Get history statistics
exports.getHistory = async (req, res) => {
  try {
    const days = parseInt(req.query.days) || 7;
    
    // Calculate start date
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    // Get daily step records
    const result = await pool.query(
      `SELECT 
        record_date as date,
        SUM(steps) as steps,
        SUM(exp_gained) as exp_gained
       FROM step_records
       WHERE user_id = $1 
         AND record_date >= $2 
         AND record_date <= $3
       GROUP BY record_date
       ORDER BY record_date DESC`,
      [
        req.userId, 
        startDate.toISOString().split('T')[0],
        endDate.toISOString().split('T')[0]
      ]
    );

    // Add goal_reached flag
    const goalSteps = 10000;
    const history = result.rows.map(row => ({
      date: row.date,
      steps: parseInt(row.steps),
      exp_gained: parseInt(row.exp_gained),
      goal_reached: parseInt(row.steps) >= goalSteps
    }));

    // Calculate summary
    const totalSteps = history.reduce((sum, day) => sum + day.steps, 0);
    const averageDailySteps = history.length > 0 ? Math.round(totalSteps / history.length) : 0;
    const daysWithGoal = history.filter(day => day.goal_reached).length;
    const goalAchievementRate = history.length > 0 ? Math.round((daysWithGoal / history.length) * 100) : 0;

    // Get total from pet table
    const petResult = await pool.query(
      'SELECT total_steps FROM pets WHERE user_id = $1',
      [req.userId]
    );

    res.json({
      history,
      summary: {
        total_steps: petResult.rows[0]?.total_steps || 0,
        average_daily_steps: averageDailySteps,
        days_tracked: history.length,
        goal_achievement_rate: goalAchievementRate
      }
    });

  } catch (error) {
    console.error('Get history error:', error);
    res.status(500).json({ error: 'Failed to get history', details: error.message });
  }
};

// Get evolution history
exports.getEvolutionHistory = async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT 
        from_stage,
        to_stage,
        from_stage_name,
        to_stage_name,
        total_exp_at_evolution,
        evolved_at
       FROM evolution_records er
       JOIN pets p ON er.pet_id = p.id
       WHERE p.user_id = $1
       ORDER BY evolved_at DESC`,
      [req.userId]
    );

    res.json({
      evolutions: result.rows
    });

  } catch (error) {
    console.error('Get evolution history error:', error);
    res.status(500).json({ error: 'Failed to get evolution history', details: error.message });
  }
};

// Get feeding history
exports.getFeedingHistory = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 20;

    const result = await pool.query(
      `SELECT 
        food_type,
        hunger_restored,
        happiness_gained,
        fed_at
       FROM feeding_records fr
       JOIN pets p ON fr.pet_id = p.id
       WHERE p.user_id = $1
       ORDER BY fed_at DESC
       LIMIT $2`,
      [req.userId, limit]
    );

    res.json({
      feedings: result.rows
    });

  } catch (error) {
    console.error('Get feeding history error:', error);
    res.status(500).json({ error: 'Failed to get feeding history', details: error.message });
  }
};
