// 스트레칭: 경험치, 기록, 상태 반영 (커스텀 경험치 지원)
exports.stretch = async (req, res) => {
  const client = await pool.connect();
  try {
    const exp_gained = req.body.exp_gained || 5;
    await client.query('BEGIN');
    const petResult = await client.query('SELECT * FROM pets WHERE user_id = $1', [req.userId]);
    if (petResult.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'Pet not found' });
    }
    const pet = petResult.rows[0];
    await client.query(
      `INSERT INTO stretch_records (user_id, pet_id, exp_gained)
       VALUES ($1, $2, $3)`,
      [req.userId, pet.id, exp_gained]
    );
    let newTotalExp = pet.total_exp + exp_gained;
    let newCurrentExp = pet.current_exp + exp_gained;
    let currentStage = pet.current_stage;
    let evolutionInfo = null;
    let expToNextStage = pet.exp_to_next_stage;
    while (newCurrentExp >= expToNextStage && currentStage < 5) {
      const oldStageInfo = PET_STAGES[currentStage];
      newCurrentExp -= expToNextStage;
      currentStage++;
      const newStageInfo = PET_STAGES[currentStage];
      evolutionInfo = {
        from_stage: currentStage - 1,
        to_stage: currentStage,
        from_name: oldStageInfo.name,
        to_name: newStageInfo.name,
        from_emoji: oldStageInfo.emoji,
        to_emoji: newStageInfo.emoji,
        celebration_message: `축하합니다! ${newStageInfo.name}(으)로 진화했습니다!`
      };
      await client.query(
        `INSERT INTO evolution_records 
         (pet_id, from_stage, to_stage, from_stage_name, to_stage_name, total_exp_at_evolution)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [pet.id, currentStage - 1, currentStage, oldStageInfo.name, newStageInfo.name, newTotalExp]
      );
      expToNextStage = newStageInfo.expRequired;
    }
    await client.query(
      `UPDATE pets SET 
        total_exp = $1,
        current_exp = $2,
        current_stage = $3,
        stage_name = $4,
        stage_emoji = $5,
        exp_to_next_stage = $6,
        stretch_count = COALESCE(stretch_count,0) + 1,
        last_stretched_at = NOW(),
        updated_at = NOW()
       WHERE id = $7`,
      [
        newTotalExp,
        newCurrentExp,
        currentStage,
        PET_STAGES[currentStage].name,
        PET_STAGES[currentStage].emoji,
        PET_STAGES[currentStage].expRequired,
        pet.id
      ]
    );
    // 최신 펫 정보 반환
    const updatedPet = (await client.query('SELECT * FROM pets WHERE id = $1', [pet.id])).rows[0];
    await client.query('COMMIT');
    res.json({
      message: `스트레칭 완료! (+${exp_gained} EXP)`,
      exp_gained,
      evolution: evolutionInfo,
      pet: updatedPet
    });
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Stretch error:', error);
    res.status(500).json({ error: 'Failed to stretch', details: error.message });
  } finally {
    client.release();
  }
};

// 일찍 자기: 경험치, 기록, 상태 반영 (커스텀 경험치 지원)
exports.sleepEarly = async (req, res) => {
  const client = await pool.connect();
  try {
    const exp_gained = req.body.exp_gained || 10;
    await client.query('BEGIN');
    const petResult = await client.query('SELECT * FROM pets WHERE user_id = $1', [req.userId]);
    if (petResult.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'Pet not found' });
    }
    const pet = petResult.rows[0];
    await client.query(
      `INSERT INTO sleep_early_records (user_id, pet_id, exp_gained)
       VALUES ($1, $2, $3)`,
      [req.userId, pet.id, exp_gained]
    );
    let newTotalExp = pet.total_exp + exp_gained;
    let newCurrentExp = pet.current_exp + exp_gained;
    let currentStage = pet.current_stage;
    let evolutionInfo = null;
    let expToNextStage = pet.exp_to_next_stage;
    while (newCurrentExp >= expToNextStage && currentStage < 5) {
      const oldStageInfo = PET_STAGES[currentStage];
      newCurrentExp -= expToNextStage;
      currentStage++;
      const newStageInfo = PET_STAGES[currentStage];
      evolutionInfo = {
        from_stage: currentStage - 1,
        to_stage: currentStage,
        from_name: oldStageInfo.name,
        to_name: newStageInfo.name,
        from_emoji: oldStageInfo.emoji,
        to_emoji: newStageInfo.emoji,
        celebration_message: `축하합니다! ${newStageInfo.name}(으)로 진화했습니다!`
      };
      await client.query(
        `INSERT INTO evolution_records 
         (pet_id, from_stage, to_stage, from_stage_name, to_stage_name, total_exp_at_evolution)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [pet.id, currentStage - 1, currentStage, oldStageInfo.name, newStageInfo.name, newTotalExp]
      );
      expToNextStage = newStageInfo.expRequired;
    }
    await client.query(
      `UPDATE pets SET 
        total_exp = $1,
        current_exp = $2,
        current_stage = $3,
        stage_name = $4,
        stage_emoji = $5,
        exp_to_next_stage = $6,
        sleep_early_count = COALESCE(sleep_early_count,0) + 1,
        last_sleep_early_at = NOW(),
        updated_at = NOW()
       WHERE id = $7`,
      [
        newTotalExp,
        newCurrentExp,
        currentStage,
        PET_STAGES[currentStage].name,
        PET_STAGES[currentStage].emoji,
        PET_STAGES[currentStage].expRequired,
        pet.id
      ]
    );
    // 최신 펫 정보 반환
    const updatedPet = (await client.query('SELECT * FROM pets WHERE id = $1', [pet.id])).rows[0];
    await client.query('COMMIT');
    res.json({
      message: `일찍 자기 성공! (+${exp_gained} EXP)`,
      exp_gained,
      evolution: evolutionInfo,
      pet: updatedPet
    });
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Sleep early error:', error);
    res.status(500).json({ error: 'Failed to sleep early', details: error.message });
  } finally {
    client.release();
  }
};
// 물 마시기: 경험치, 기록, 상태 반영
exports.drinkWater = async (req, res) => {
  const client = await pool.connect();
  try {
    const amount_ml = req.body.amount_ml || 200; // 기본 200ml
    const exp_gained = Math.floor(amount_ml / 40); // 200ml당 5exp, 40ml당 1exp

    await client.query('BEGIN');

    // Get current pet
    const petResult = await client.query('SELECT * FROM pets WHERE user_id = $1', [req.userId]);
    if (petResult.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'Pet not found' });
    }
    const pet = petResult.rows[0];

    // 기록 저장
    await client.query(
      `INSERT INTO water_records (user_id, pet_id, amount_ml, exp_gained)
       VALUES ($1, $2, $3, $4)`,
      [req.userId, pet.id, amount_ml, exp_gained]
    );

    // 펫 상태 업데이트
    const newTotalExp = pet.total_exp + exp_gained;
    const newCurrentExp = pet.current_exp + exp_gained;
    let currentStage = pet.current_stage;
    let evolutionInfo = null;
    let expToNextStage = pet.exp_to_next_stage;

    // 진화 체크
    while (newCurrentExp >= expToNextStage && currentStage < 5) {
      const oldStageInfo = PET_STAGES[currentStage];
      newCurrentExp -= expToNextStage;
      currentStage++;
      const newStageInfo = PET_STAGES[currentStage];
      evolutionInfo = {
        from_stage: currentStage - 1,
        to_stage: currentStage,
        from_name: oldStageInfo.name,
        to_name: newStageInfo.name,
        from_emoji: oldStageInfo.emoji,
        to_emoji: newStageInfo.emoji,
        celebration_message: `축하합니다! ${newStageInfo.name}(으)로 진화했습니다!`
      };
      await client.query(
        `INSERT INTO evolution_records 
         (pet_id, from_stage, to_stage, from_stage_name, to_stage_name, total_exp_at_evolution)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [pet.id, currentStage - 1, currentStage, oldStageInfo.name, newStageInfo.name, newTotalExp]
      );
      expToNextStage = newStageInfo.expRequired;
    }

    // water_count, last_watered_at 갱신
    await client.query(
      `UPDATE pets SET 
        total_exp = $1,
        current_exp = $2,
        current_stage = $3,
        stage_name = $4,
        stage_emoji = $5,
        exp_to_next_stage = $6,
        water_count = COALESCE(water_count,0) + 1,
        last_watered_at = NOW(),
        updated_at = NOW()
       WHERE id = $7`,
      [
        newTotalExp,
        newCurrentExp,
        currentStage,
        PET_STAGES[currentStage].name,
        PET_STAGES[currentStage].emoji,
        PET_STAGES[currentStage].expRequired,
        pet.id
      ]
    );

    await client.query('COMMIT');

    res.json({
      message: `물 ${amount_ml}ml 마시기! (+${exp_gained} EXP)`,
      exp_gained,
      evolution: evolutionInfo,
    });
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Drink water error:', error);
    res.status(500).json({ error: 'Failed to drink water', details: error.message });
  } finally {
    client.release();
  }
};
const pool = require('../config/database');

// Pet stage information
const PET_STAGES = {
  1: { name: '신비한 알', emoji: '🥚', expRequired: 1000 },
  2: { name: '작은 병아리', emoji: '🐤', expRequired: 3000 },
  3: { name: '날개 돋는 새', emoji: '🐦', expRequired: 7000 },
  4: { name: '불꽃의 새', emoji: '🔥', expRequired: 15000 },
  5: { name: '황금 불사조', emoji: '✨', expRequired: 999999 }
};

// Convert steps to EXP (10 steps = 1 EXP)
const stepsToExp = (steps) => Math.floor(steps / 10);

// Get pet information
exports.getPet = async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT 
        p.*,
        EXTRACT(DAY FROM (NOW() - p.born_at))::INTEGER as age_days,
        CASE 
          WHEN p.current_stage = 5 THEN true 
          ELSE false 
        END as is_max_stage
       FROM pets p
       WHERE p.user_id = $1`,
      [req.userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Pet not found' });
    }

    const pet = result.rows[0];
    const progressPercentage = pet.exp_to_next_stage > 0 
      ? Math.round((pet.current_exp / pet.exp_to_next_stage) * 100)
      : 100;

    res.json({
      pet: {
        ...pet,
        progress_percentage: progressPercentage
      }
    });

  } catch (error) {
    console.error('Get pet error:', error);
    res.status(500).json({ error: 'Failed to get pet', details: error.message });
  }
};

// Add steps and update pet
exports.addSteps = async (req, res) => {
  const client = await pool.connect();
  
  try {
    const { steps } = req.body;

    if (!steps || steps <= 0) {
      return res.status(400).json({ error: 'Invalid steps amount' });
    }

    await client.query('BEGIN');

    // Get current pet
    const petResult = await client.query(
      'SELECT * FROM pets WHERE user_id = $1',
      [req.userId]
    );

    if (petResult.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'Pet not found' });
    }

    const pet = petResult.rows[0];
    const expGained = stepsToExp(steps);

    // Record steps
    await client.query(
      `INSERT INTO step_records (user_id, pet_id, steps, exp_gained)
       VALUES ($1, $2, $3, $4)`,
      [req.userId, pet.id, steps, expGained]
    );

    // Calculate new values
    let newTotalSteps = pet.total_steps + steps;
    let newTodaySteps = pet.today_steps + steps;
    let newTotalExp = pet.total_exp + expGained;
    let newCurrentExp = pet.current_exp + expGained;
    let currentStage = pet.current_stage;
    let evolutionInfo = null;

    // Check for evolution
    while (newCurrentExp >= pet.exp_to_next_stage && currentStage < 5) {
      const oldStageInfo = PET_STAGES[currentStage];
      
      newCurrentExp -= pet.exp_to_next_stage;
      currentStage++;
      
      const newStageInfo = PET_STAGES[currentStage];

      evolutionInfo = {
        from_stage: currentStage - 1,
        to_stage: currentStage,
        from_name: oldStageInfo.name,
        to_name: newStageInfo.name,
        from_emoji: oldStageInfo.emoji,
        to_emoji: newStageInfo.emoji,
        celebration_message: `축하합니다! ${newStageInfo.name}(으)로 진화했습니다!`
      };

      // Record evolution
      await client.query(
        `INSERT INTO evolution_records 
         (pet_id, from_stage, to_stage, from_stage_name, to_stage_name, total_exp_at_evolution)
         VALUES ($1, $2, $3, $4, $5, $6)`,
        [pet.id, currentStage - 1, currentStage, oldStageInfo.name, newStageInfo.name, newTotalExp]
      );

      pet.exp_to_next_stage = newStageInfo.expRequired;
    }

    // Decrease hunger (1 per 1000 steps)
    const hungerDecrease = Math.floor(steps / 1000);
    const newHunger = Math.max(0, pet.hunger_level - hungerDecrease);

    // Get new stage info
    const stageInfo = PET_STAGES[currentStage];

    // Update pet
    await client.query(
      `UPDATE pets SET
        total_steps = $1,
        today_steps = $2,
        total_exp = $3,
        current_exp = $4,
        current_stage = $5,
        stage_name = $6,
        stage_emoji = $7,
        exp_to_next_stage = $8,
        hunger_level = $9,
        updated_at = NOW()
       WHERE id = $10`,
      [
        newTotalSteps,
        newTodaySteps,
        newTotalExp,
        newCurrentExp,
        currentStage,
        stageInfo.name,
        stageInfo.emoji,
        stageInfo.expRequired,
        newHunger,
        pet.id
      ]
    );

    await client.query('COMMIT');

    res.json({
      pet: {
        today_steps: newTodaySteps,
        total_steps: newTotalSteps,
        total_exp: newTotalExp,
        current_exp: newCurrentExp,
        current_stage: currentStage,
        stage_name: stageInfo.name,
        hunger_level: newHunger
      },
      exp_gained: expGained,
      evolved: evolutionInfo !== null,
      evolution_info: evolutionInfo,
      hunger_decreased: hungerDecrease > 0,
      current_hunger: newHunger
    });

  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Add steps error:', error);
    res.status(500).json({ error: 'Failed to add steps', details: error.message });
  } finally {
    client.release();
  }
};

// Feed pet
exports.feedPet = async (req, res) => {
  const client = await pool.connect();
  
  try {
    const { food_type } = req.body;

    const FOOD_TYPES = {
      berry: { name: '불꽃 베리', emoji: '🍓', hunger: 15, happiness: 5, cost: 0 },
      meat: { name: '신성한 고기', emoji: '🍖', hunger: 40, happiness: 15, cost: 100 },
      golden_fruit: { name: '황금 과일', emoji: '🍑', hunger: 100, happiness: 30, cost: 500 }
    };

    const food = FOOD_TYPES[food_type];
    if (!food) {
      return res.status(400).json({ error: 'Invalid food type' });
    }

    await client.query('BEGIN');

    // Get pet
    const petResult = await client.query(
      'SELECT * FROM pets WHERE user_id = $1',
      [req.userId]
    );

    if (petResult.rows.length === 0) {
      await client.query('ROLLBACK');
      return res.status(404).json({ error: 'Pet not found' });
    }

    const pet = petResult.rows[0];

    // Check if user has enough steps
    if (pet.today_steps < food.cost) {
      await client.query('ROLLBACK');
      return res.status(400).json({ 
        error: 'Not enough steps',
        required: food.cost,
        available: pet.today_steps
      });
    }

    // Calculate new values
    const newHunger = Math.min(100, pet.hunger_level + food.hunger);
    const newHappiness = Math.min(100, pet.happiness_level + food.happiness);
    const newTodaySteps = pet.today_steps - food.cost;

    // Update pet
    await client.query(
      `UPDATE pets SET
        hunger_level = $1,
        happiness_level = $2,
        today_steps = $3,
        last_fed_at = NOW(),
        updated_at = NOW()
       WHERE id = $4`,
      [newHunger, newHappiness, newTodaySteps, pet.id]
    );

    // Record feeding
    await client.query(
      `INSERT INTO feeding_records (user_id, pet_id, food_type, hunger_restored, happiness_gained)
       VALUES ($1, $2, $3, $4, $5)`,
      [req.userId, pet.id, food_type, food.hunger, food.happiness]
    );

    await client.query('COMMIT');

    res.json({
      pet: {
        hunger_level: newHunger,
        happiness_level: newHappiness,
        today_steps: newTodaySteps
      },
      food_effect: {
        name: food.name,
        emoji: food.emoji,
        hunger_restored: food.hunger,
        happiness_gained: food.happiness
      },
      message: `불사조가 ${food.emoji} ${food.name}을(를) 맛있게 먹었어요!`
    });

  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Feed pet error:', error);
    res.status(500).json({ error: 'Failed to feed pet', details: error.message });
  } finally {
    client.release();
  }
};

// Update pet name
exports.updatePetName = async (req, res) => {
  try {
    const { name } = req.body;

    if (!name || name.trim().length === 0) {
      return res.status(400).json({ error: 'Pet name is required' });
    }

    if (name.length > 100) {
      return res.status(400).json({ error: 'Pet name is too long (max 100 characters)' });
    }

    await pool.query(
      'UPDATE pets SET name = $1, updated_at = NOW() WHERE user_id = $2',
      [name.trim(), req.userId]
    );

    res.json({ message: 'Pet name updated successfully', name: name.trim() });

  } catch (error) {
    console.error('Update pet name error:', error);
    res.status(500).json({ error: 'Failed to update pet name', details: error.message });
  }
};

// Get pet status
exports.getPetStatus = async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT 
        p.*,
        (SELECT COUNT(*) FROM feeding_records WHERE pet_id = p.id AND DATE(fed_at) = CURRENT_DATE) as times_fed_today,
        (SELECT SUM(exp_gained) FROM step_records WHERE pet_id = p.id AND record_date = CURRENT_DATE) as exp_gained_today
       FROM pets p
       WHERE p.user_id = $1`,
      [req.userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Pet not found' });
    }

    const pet = result.rows[0];
    
    // Determine status
    let status = 'normal';
    let moodMessage = '좋은 하루예요! 😊';
    const warnings = [];

    if (pet.hunger_level < 30) {
      status = 'hungry';
      moodMessage = '배고파요... 🥺';
      warnings.push('배고픔이 30 이하입니다. 먹이를 주세요!');
    } else if (pet.happiness_level < 50) {
      status = 'sad';
      moodMessage = '심심해요... 😢';
      warnings.push('행복도가 낮습니다. 함께 걸어요!');
    } else if (pet.hunger_level > 80 && pet.happiness_level > 80) {
      status = 'happy';
      moodMessage = '행복해요! 😊';
    }

    if (pet.current_stage === 5) {
      status = 'max';
      moodMessage = '전설이 되었어요! 👑✨';
    }

    // Next evolution info
    const canEvolve = pet.current_stage < 5;
    const expNeeded = canEvolve ? pet.exp_to_next_stage - pet.current_exp : 0;
    const stepsNeeded = expNeeded * 10;

    res.json({
      status,
      mood_message: moodMessage,
      warnings,
      next_evolution: {
        can_evolve: canEvolve,
        stage_name: canEvolve ? PET_STAGES[pet.current_stage + 1].name : '황금 불사조',
        exp_needed: expNeeded,
        steps_needed: stepsNeeded,
        is_max_stage: pet.current_stage === 5
      },
      daily_progress: {
        today_steps: pet.today_steps,
        today_exp: pet.exp_gained_today || 0,
        times_fed: parseInt(pet.times_fed_today) || 0,
        goal_steps: 10000
      }
    });

  } catch (error) {
    console.error('Get pet status error:', error);
    res.status(500).json({ error: 'Failed to get pet status', details: error.message });
  }
};
