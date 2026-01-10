import React, { useEffect, useRef, useState } from 'react';

const BGMController = () => {
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [volume, setVolume] = useState(0.3);

  // 컴포넌트 마운트 시 BGM 자동 재생
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    // 오디오 설정
    audio.volume = volume;
    audio.loop = true;

    // 자동 재생 시도
    const playAudio = () => {
      audio.play().catch(err => {
        console.log('자동 재생 실패 (사용자 상호작용 필요):', err);
        // 사용자 상호작용 후 재생하도록 설정
        const handleUserInteraction = () => {
          audio.play();
          document.removeEventListener('click', handleUserInteraction);
        };
        document.addEventListener('click', handleUserInteraction);
      });
    };

    playAudio();

    // 정리
    return () => {
      audio.pause();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 음량 변경
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);

  // 재생/일시정지 토글
  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      audio.play();
      setIsPlaying(true);
    }
  };

  return (
    <>
      {/* 숨겨진 오디오 요소 */}
      <audio
        ref={audioRef}
        src="/audio/bgm.wav"
        loop
        preload="auto"
      />

      {/* BGM 컨트롤 UI */}
      <div className="fixed bottom-6 left-6 bg-white bg-opacity-90 rounded-xl shadow-lg p-4 flex items-center gap-4 z-40 hover:bg-opacity-100 transition-all">
        {/* 재생/일시정지 버튼 */}
        <button
          onClick={togglePlayPause}
          className="text-2xl hover:scale-110 transition-transform"
          title={isPlaying ? '일시정지' : '재생'}
        >
          {isPlaying ? '🔊' : '🔇'}
        </button>

        {/* 음량 슬라이더 */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">🎵</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={(e) => setVolume(parseFloat(e.target.value))}
            className="w-24 h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer accent-blue-500"
            title="음량 조절"
          />
          <span className="text-xs text-gray-600 w-8 text-right">
            {Math.round(volume * 100)}%
          </span>
        </div>
      </div>
    </>
  );
};

export default BGMController;
