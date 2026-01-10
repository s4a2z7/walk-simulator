const pool = require('../config/database');

// Get friend rankings
exports.getRanking = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 10;

    // Get all friends and self
    const result = await pool.query(
      `WITH friend_ids AS (
        SELECT friend_id as user_id 
        FROM friendships 
        WHERE user_id = $1 AND status = 'accepted'
        UNION
        SELECT $1 as user_id
      )
      SELECT 
        u.id as user_id,
        u.username,
        u.display_name,
        u.avatar_emoji,
        p.name as pet_name,
        p.current_stage as pet_stage,
        p.stage_name as pet_stage_name,
        p.stage_emoji as pet_emoji,
        p.total_exp,
        p.total_steps,
        EXTRACT(DAY FROM (NOW() - p.born_at))::INTEGER as age_days,
        CASE WHEN u.id = $1 THEN true ELSE false END as is_me,
        ROW_NUMBER() OVER (ORDER BY p.total_exp DESC, p.total_steps DESC) as rank
      FROM users u
      JOIN pets p ON u.id = p.user_id
      WHERE u.id IN (SELECT user_id FROM friend_ids)
      ORDER BY p.total_exp DESC, p.total_steps DESC
      LIMIT $2`,
      [req.userId, limit]
    );

    res.json({
      rankings: result.rows
    });

  } catch (error) {
    console.error('Get ranking error:', error);
    res.status(500).json({ error: 'Failed to get ranking', details: error.message });
  }
};

// Get global leaderboard (top players)
exports.getLeaderboard = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;

    const result = await pool.query(
      `SELECT 
        u.id as user_id,
        u.username,
        u.display_name,
        u.avatar_emoji,
        p.name as pet_name,
        p.current_stage as pet_stage,
        p.stage_name as pet_stage_name,
        p.stage_emoji as pet_emoji,
        p.total_exp,
        p.total_steps,
        EXTRACT(DAY FROM (NOW() - p.born_at))::INTEGER as age_days,
        CASE WHEN u.id = $1 THEN true ELSE false END as is_me,
        ROW_NUMBER() OVER (ORDER BY p.total_exp DESC, p.total_steps DESC) as rank
      FROM users u
      JOIN pets p ON u.id = p.user_id
      ORDER BY p.total_exp DESC, p.total_steps DESC
      LIMIT $2`,
      [req.userId, limit]
    );

    res.json({
      leaderboard: result.rows
    });

  } catch (error) {
    console.error('Get leaderboard error:', error);
    res.status(500).json({ error: 'Failed to get leaderboard', details: error.message });
  }
};

// Add friend
exports.addFriend = async (req, res) => {
  const client = await pool.connect();
  
  try {
    const { username } = req.body;

    if (!username) {
      return res.status(400).json({ error: 'Username is required' });
    }

    await client.query('BEGIN');

    // Find friend
    const friendResult = await client.query(
      'SELECT id, username, display_name, avatar_emoji FROM users WHERE username = $1',
      [username]
    );

    if (friendResult.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'User not found' });
    }

    const friend = friendResult.rows[0];

    // Can't add yourself
    if (friend.id === req.userId) {
      await client.query('ROLLBACK');
      return res.status(400).json({ error: 'Cannot add yourself as friend' });
    }

    // Check if friendship already exists
    const existingFriendship = await client.query(
      `SELECT id FROM friendships 
       WHERE (user_id = $1 AND friend_id = $2) OR (user_id = $2 AND friend_id = $1)`,
      [req.userId, friend.id]
    );

    if (existingFriendship.rows.length > 0) {
      await client.query('ROLLBACK');
      return res.status(409).json({ error: 'Friendship already exists' });
    }

    // Add friendship (bidirectional)
    await client.query(
      'INSERT INTO friendships (user_id, friend_id, status) VALUES ($1, $2, $3)',
      [req.userId, friend.id, 'accepted']
    );

    await client.query(
      'INSERT INTO friendships (user_id, friend_id, status) VALUES ($1, $2, $3)',
      [friend.id, req.userId, 'accepted']
    );

    await client.query('COMMIT');

    // Get friend's pet info
    const petResult = await client.query(
      `SELECT name, current_stage, stage_name, stage_emoji, total_exp, total_steps
       FROM pets WHERE user_id = $1`,
      [friend.id]
    );

    res.status(201).json({
      message: 'Friend added successfully',
      friend: {
        ...friend,
        pet: petResult.rows[0]
      }
    });

  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Add friend error:', error);
    res.status(500).json({ error: 'Failed to add friend', details: error.message });
  } finally {
    client.release();
  }
};

// Get friends list
exports.getFriends = async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT 
        u.id,
        u.username,
        u.display_name,
        u.avatar_emoji,
        p.name as pet_name,
        p.current_stage as pet_stage,
        p.stage_name as pet_stage_name,
        p.stage_emoji as pet_emoji,
        p.total_exp,
        p.total_steps,
        f.created_at as friend_since
      FROM friendships f
      JOIN users u ON f.friend_id = u.id
      JOIN pets p ON u.id = p.user_id
      WHERE f.user_id = $1 AND f.status = 'accepted'
      ORDER BY p.total_exp DESC`,
      [req.userId]
    );

    res.json({
      friends: result.rows
    });

  } catch (error) {
    console.error('Get friends error:', error);
    res.status(500).json({ error: 'Failed to get friends', details: error.message });
  }
};

// Remove friend
exports.removeFriend = async (req, res) => {
  const client = await pool.connect();
  
  try {
    const { friendshipId } = req.params;

    await client.query('BEGIN');

    // Get friendship details
    const friendship = await client.query(
      'SELECT user_id, friend_id FROM friendships WHERE id = $1',
      [friendshipId]
    );

    if (friendship.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'Friendship not found' });
    }

    const { user_id, friend_id } = friendship.rows[0];

    // Check authorization
    if (user_id !== req.userId) {
      await client.query('ROLLBACK');
      return res.status(403).json({ error: 'Unauthorized' });
    }

    // Delete both directions of friendship
    await client.query(
      'DELETE FROM friendships WHERE (user_id = $1 AND friend_id = $2) OR (user_id = $2 AND friend_id = $1)',
      [user_id, friend_id]
    );

    await client.query('COMMIT');

    res.json({ message: 'Friend removed successfully' });

  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Remove friend error:', error);
    res.status(500).json({ error: 'Failed to remove friend', details: error.message });
  } finally {
    client.release();
  }
};
