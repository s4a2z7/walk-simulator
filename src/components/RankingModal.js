import React, { useState, useEffect } from 'react';
import { rankingAPI } from '../services/api';

function RankingModal({ onClose, currentUserId }) {
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newFriend, setNewFriend] = useState('');
  const [addingFriend, setAddingFriend] = useState(false);

  useEffect(() => {
    loadRankings();
  }, []);

  const loadRankings = async () => {
    try {
      setLoading(true);
      const response = await rankingAPI.getRanking(20);
      setRankings(response.data.rankings);
      setError('');
    } catch (err) {
      setError('랭킹을 불러올 수 없습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddFriend = async (e) => {
    e.preventDefault();
    if (!newFriend.trim()) return;

    try {
      setAddingFriend(true);
      await rankingAPI.addFriend(newFriend.trim());
      setNewFriend('');
      await loadRankings();
      alert('친구가 추가되었습니다!');
    } catch (err) {
      alert(err.response?.data?.error || '친구 추가에 실패했습니다.');
    } finally {
      setAddingFriend(false);
    }
  };

  const getRankMedal = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `${rank}위`;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-[9998] flex items-center justify-center p-4 animate-fadeIn"
         onClick={onClose}>
      <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden animate-slideUp"
           onClick={(e) => e.stopPropagation()}>
        
        {/* 헤더 */}
        <div className="bg-gradient-to-r from-phoenix-red to-phoenix-gold text-white p-6 flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-black flex items-center gap-2">
              🏆 랭킹
            </h2>
            <p className="text-sm opacity-90 mt-1">친구들과 함께 경쟁해요!</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 rounded-full w-10 h-10 flex items-center justify-center transition"
          >
            ✕
          </button>
        </div>

        {/* 친구 추가 */}
        <div className="p-4 bg-gray-50 border-b">
          <form onSubmit={handleAddFriend} className="flex gap-2">
            <input
              type="text"
              value={newFriend}
              onChange={(e) => setNewFriend(e.target.value)}
              placeholder="친구 사용자명"
              className="flex-1 px-4 py-2 border-2 border-gray-300 rounded-xl focus:border-phoenix-red focus:outline-none"
              disabled={addingFriend}
            />
            <button
              type="submit"
              disabled={addingFriend || !newFriend.trim()}
              className="px-6 py-2 bg-phoenix-red text-white font-bold rounded-xl hover:bg-phoenix-orange transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {addingFriend ? '추가중...' : '친구 추가'}
            </button>
          </form>
        </div>

        {/* 랭킹 리스트 */}
        <div className="overflow-y-auto max-h-96 p-4">
          {loading ? (
            <div className="text-center py-12">
              <div className="text-5xl mb-4 animate-bounce">🔥</div>
              <p className="text-gray-600">로딩 중...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12 text-red-600">
              <p>{error}</p>
              <button 
                onClick={loadRankings}
                className="mt-4 text-sm text-phoenix-red hover:underline"
              >
                다시 시도
              </button>
            </div>
          ) : rankings.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-4xl mb-4">😢</p>
              <p>아직 친구가 없습니다.</p>
              <p className="text-sm mt-2">위에서 친구를 추가해보세요!</p>
            </div>
          ) : (
            <div className="space-y-2">
              {rankings.map((entry) => {
                const isMe = entry.is_me;
                
                return (
                  <div
                    key={entry.user_id}
                    className={`flex items-center gap-4 p-4 rounded-2xl transition ${
                      isMe 
                        ? 'bg-gradient-to-r from-phoenix-gold to-phoenix-orange text-white shadow-lg transform scale-105' 
                        : 'bg-gray-50 hover:bg-gray-100'
                    }`}
                  >
                    {/* 순위 */}
                    <div className="text-2xl font-black w-16 text-center">
                      {getRankMedal(entry.rank)}
                    </div>

                    {/* 펫 */}
                    <div className="text-5xl">
                      {entry.pet_emoji || '🥚'}
                    </div>

                    {/* 정보 */}
                    <div className="flex-1">
                      <div className="font-black text-lg flex items-center gap-2">
                        {entry.display_name || entry.username}
                        {isMe && <span className="text-sm">👈 나</span>}
                      </div>
                      <div className={`text-sm ${isMe ? 'text-white text-opacity-90' : 'text-gray-600'}`}>
                        {entry.pet_stage_name} | {entry.total_steps.toLocaleString()} 걸음
                      </div>
                    </div>

                    {/* EXP */}
                    <div className="text-right">
                      <div className="font-black text-xl">
                        {entry.total_exp.toLocaleString()}
                      </div>
                      <div className={`text-xs ${isMe ? 'text-white text-opacity-75' : 'text-gray-500'}`}>
                        EXP
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* 애니메이션 */}
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        
        @keyframes slideUp {
          from { 
            opacity: 0; 
            transform: translateY(50px); 
          }
          to { 
            opacity: 1; 
            transform: translateY(0); 
          }
        }
      `}</style>
    </div>
  );
}

export default RankingModal;
