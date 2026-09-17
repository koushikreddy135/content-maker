import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, X, FlipHorizontal, Type, Clock, Sliders, Volume2 } from 'lucide-react';

export default function TeleprompterModal({ isOpen, onClose, scriptMarkdown, topic }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [scrollSpeed, setScrollSpeed] = useState(40); // pixels per second
  const [fontSize, setFontSize] = useState(28); // px
  const [isMirrored, setIsMirrored] = useState(false);
  const [wpm, setWpm] = useState(140);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  const scrollRef = useRef(null);
  const animationFrameRef = useRef(null);
  const lastTimeRef = useRef(null);

  // Calculate word count and estimated speaking duration
  const plainText = scriptMarkdown ? scriptMarkdown.replace(/#+\s*/g, '').replace(/\*+/g, '').replace(/_+/g, '') : '';
  const wordCount = plainText ? plainText.trim().split(/\s+/).length : 0;
  const totalMinutesEstimated = (wordCount / (wpm || 140)).toFixed(1);

  // Keyboard shortcut: Spacebar to toggle Play/Pause, Esc to close
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault();
        setIsPlaying((prev) => !prev);
      } else if (e.code === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Autoscroll logic using requestAnimationFrame for butter-smooth 60fps scrolling
  useEffect(() => {
    if (!isPlaying) {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      lastTimeRef.current = null;
      return;
    }

    const step = (currentTime) => {
      if (lastTimeRef.current != null) {
        const delta = (currentTime - lastTimeRef.current) / 1000;
        if (scrollRef.current) {
          scrollRef.current.scrollTop += scrollSpeed * delta;
        }
      }
      lastTimeRef.current = currentTime;
      animationFrameRef.current = requestAnimationFrame(step);
    };

    animationFrameRef.current = requestAnimationFrame(step);

    return () => {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
    };
  }, [isPlaying, scrollSpeed]);

  // Elapsed read timer
  useEffect(() => {
    let timer;
    if (isPlaying) {
      timer = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isPlaying]);

  const handleReset = () => {
    setIsPlaying(false);
    setElapsedSeconds(0);
    if (scrollRef.current) {
      scrollRef.current.scrollTop = 0;
    }
  };

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(8, 9, 12, 0.98)',
      backdropFilter: 'blur(16px)',
      zIndex: 10000,
      display: 'flex',
      flexDirection: 'column',
      fontFamily: 'var(--font-sans, "Plus Jakarta Sans", sans-serif)',
      color: '#ffffff'
    }}>
      {/* Top Floating Control Bar */}
      <div style={{
        padding: '14px 28px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: 'rgba(15, 17, 23, 0.9)',
        zIndex: 2
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
            width: '32px',
            height: '32px',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#000',
            fontWeight: '800',
            fontSize: '14px'
          }}>
            <Volume2 size={18} />
          </div>
          <div>
            <h2 style={{ fontSize: '15px', fontWeight: '800', margin: 0, color: '#f3f4f6' }}>
              ContentMaker Teleprompter Studio
            </h2>
            <p style={{ fontSize: '12px', color: '#9ca3af', margin: 0 }}>
              {topic} • {wordCount} words (~{totalMinutesEstimated} mins read)
            </p>
          </div>
        </div>

        {/* Playback Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            style={{
              background: isPlaying ? '#ef4444' : '#f59e0b',
              color: '#0b0c10',
              border: 'none',
              borderRadius: '30px',
              padding: '8px 22px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontWeight: '700',
              fontSize: '14px',
              cursor: 'pointer',
              boxShadow: '0 2px 10px rgba(245, 158, 11, 0.3)'
            }}
          >
            {isPlaying ? <Pause size={16} fill="#0b0c10" /> : <Play size={16} fill="#0b0c10" />}
            {isPlaying ? 'PAUSE (Space)' : 'START SCROLL (Space)'}
          </button>

          <button
            onClick={handleReset}
            title="Reset to Top"
            style={{
              background: 'rgba(255, 255, 255, 0.08)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#d1d5db',
              borderRadius: '8px',
              padding: '8px 12px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              cursor: 'pointer'
            }}
          >
            <RotateCcw size={14} /> Reset
          </button>

          {/* Speed slider */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(255,255,255,0.05)', padding: '6px 12px', borderRadius: '8px' }}>
            <Sliders size={14} color="#9ca3af" />
            <span style={{ fontSize: '11px', fontWeight: '700', color: '#9ca3af', textTransform: 'uppercase' }}>Speed:</span>
            <input
              type="range"
              min="15"
              max="120"
              value={scrollSpeed}
              onChange={(e) => setScrollSpeed(Number(e.target.value))}
              style={{ width: '90px', accentColor: '#f59e0b', cursor: 'pointer' }}
            />
            <span style={{ fontSize: '12px', fontWeight: '700', color: '#fbbf24', minWidth: '32px' }}>{scrollSpeed}</span>
          </div>

          {/* Font Size Buttons */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'rgba(255,255,255,0.05)', padding: '4px 8px', borderRadius: '8px' }}>
            <Type size={14} color="#9ca3af" />
            <button
              onClick={() => setFontSize((prev) => Math.max(18, prev - 4))}
              style={{ background: 'transparent', border: 'none', color: '#fff', padding: '2px 6px', cursor: 'pointer', fontWeight: '700' }}
            >
              A-
            </button>
            <span style={{ fontSize: '11px', color: '#fbbf24' }}>{fontSize}px</span>
            <button
              onClick={() => setFontSize((prev) => Math.min(48, prev + 4))}
              style={{ background: 'transparent', border: 'none', color: '#fff', padding: '2px 6px', cursor: 'pointer', fontWeight: '700' }}
            >
              A+
            </button>
          </div>

          {/* Mirror Toggle */}
          <button
            onClick={() => setIsMirrored(!isMirrored)}
            title="Mirror for Beamsplitter Teleprompter Glass"
            style={{
              background: isMirrored ? '#3b82f6' : 'rgba(255,255,255,0.08)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#fff',
              borderRadius: '8px',
              padding: '8px 12px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              cursor: 'pointer',
              fontSize: '12px',
              fontWeight: '600'
            }}
          >
            <FlipHorizontal size={14} /> {isMirrored ? 'Mirrored (ON)' : 'Mirror'}
          </button>

          {/* Timer Display */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#10b981', fontWeight: '700', fontSize: '13px' }}>
            <Clock size={15} />
            <span>{formatTime(elapsedSeconds)}</span>
          </div>

          {/* Close Button */}
          <button
            onClick={onClose}
            style={{
              background: 'rgba(255, 255, 255, 0.08)',
              border: 'none',
              color: '#9ca3af',
              borderRadius: '50%',
              width: '32px',
              height: '32px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
          >
            <X size={18} />
          </button>
        </div>
      </div>

      {/* Center Prompt Eyeline Guide Indicator */}
      <div style={{
        position: 'absolute',
        top: '40%',
        left: 0,
        right: 0,
        height: '3px',
        background: 'linear-gradient(90deg, transparent 0%, rgba(245, 158, 11, 0.7) 20%, rgba(245, 158, 11, 0.7) 80%, transparent 100%)',
        pointerEvents: 'none',
        zIndex: 5,
        boxShadow: '0 0 10px rgba(245, 158, 11, 0.5)'
      }} />

      {/* Main Teleprompter Text Container */}
      <div
        ref={scrollRef}
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '240px 18% 400px 18%',
          fontSize: `${fontSize}px`,
          lineHeight: '1.7',
          fontWeight: '600',
          transform: isMirrored ? 'scaleX(-1)' : 'none',
          transition: 'transform 0.2s ease',
          userSelect: 'none'
        }}
      >
        <div style={{ maxWidth: '820px', margin: '0 auto' }}>
          {scriptMarkdown ? (
            scriptMarkdown.split('\n\n').map((para, idx) => {
              if (para.startsWith('# ')) {
                return (
                  <h1 key={idx} style={{ color: '#f59e0b', fontSize: `${fontSize * 1.3}px`, marginBottom: '24px', textAlign: 'center', borderBottom: '2px solid rgba(245,158,11,0.3)', paddingBottom: '16px' }}>
                    {para.replace('# ', '')}
                  </h1>
                );
              }
              if (para.startsWith('## ')) {
                return (
                  <h2 key={idx} style={{ color: '#60a5fa', fontSize: `${fontSize * 1.1}px`, marginTop: '36px', marginBottom: '14px', letterSpacing: '-0.01em' }}>
                    {para.replace('## ', '')}
                  </h2>
                );
              }
              if (para.includes('**Visual:**') || para.includes('*Visual Cue:*')) {
                return (
                  <div key={idx} style={{
                    background: 'rgba(245, 158, 11, 0.12)',
                    borderLeft: '4px solid #f59e0b',
                    padding: '8px 14px',
                    fontSize: `${fontSize * 0.75}px`,
                    color: '#fde68a',
                    borderRadius: '0 8px 8px 0',
                    margin: '16px 0',
                    fontStyle: 'italic'
                  }}>
                    {para}
                  </div>
                );
              }
              return (
                <p key={idx} style={{ marginBottom: '24px', color: '#f9fafb' }}>
                  {para}
                </p>
              );
            })
          ) : (
            <p style={{ textAlign: 'center', color: '#6b7280' }}>No script available for teleprompter.</p>
          )}
        </div>
      </div>
    </div>
  );
}
