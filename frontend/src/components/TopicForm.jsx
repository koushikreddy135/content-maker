import React, { useState } from 'react';
import { Play, Sparkles, RefreshCw, CheckCircle2, Sliders, ArrowRight } from 'lucide-react';

export default function TopicForm({ onSubmit, isRunning }) {
  const [topic, setTopic] = useState("Building Cyclic Multi-Agent Systems with LangGraph");
  const [duration, setDuration] = useState("8-10 mins");
  const [tone, setTone] = useState("authoritative, dynamic, and educational");

  const handleLaunchScenario = (scTopic, scDuration, scTone) => {
    setTopic(scTopic);
    setDuration(scDuration);
    setTone(scTone);
    onSubmit({ topic: scTopic, duration_target: scDuration, tone: scTone });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!topic.trim() || isRunning) return;
    onSubmit({ topic, duration_target: duration, tone });
  };

  return (
    <div className="luxe-card" style={{ padding: '22px', marginBottom: '20px' }}>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
            <label style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Video Topic / Research Hypothesis
            </label>
            <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
              Type any topic or choose a portfolio demo below
            </span>
          </div>

          <div>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Building Cyclic Multi-Agent Systems with LangGraph"
              disabled={isRunning}
              style={{
                width: '100%',
                background: 'var(--bg-input)',
                border: '1px solid var(--border-light)',
                borderRadius: '10px',
                padding: '12px 16px',
                color: 'var(--text-primary)',
                fontSize: '14px',
                fontWeight: '500',
                outline: 'none',
                transition: 'border-color 0.15s ease',
              }}
              onFocus={(e) => e.target.style.borderColor = 'var(--accent-gold)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--border-light)'}
            />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '14px', alignItems: 'flex-end', marginBottom: '18px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '5px' }}>
              Target Duration
            </label>
            <select
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              disabled={isRunning}
              style={{
                width: '100%',
                background: 'var(--bg-subtle)',
                border: '1px solid var(--border-light)',
                borderRadius: '9px',
                padding: '9px 12px',
                color: 'var(--text-primary)',
                fontSize: '13px',
                outline: 'none'
              }}
            >
              <option value="5-7 mins">5–7 mins • High-Velocity Breakdown</option>
              <option value="8-10 mins">8–10 mins • Standard YouTube</option>
              <option value="12-15 mins">12–15 mins • Deep Architectural Masterclass</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '5px' }}>
              Brand Persona & Tone
            </label>
            <select
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              disabled={isRunning}
              style={{
                width: '100%',
                background: 'var(--bg-subtle)',
                border: '1px solid var(--border-light)',
                borderRadius: '9px',
                padding: '9px 12px',
                color: 'var(--text-primary)',
                fontSize: '13px',
                outline: 'none'
              }}
            >
              <option value="authoritative, dynamic, and educational">Authoritative & Practical (Tech Lead)</option>
              <option value="curious, investigative, and counterintuitive">Investigative & Counter-Intuitive (Veritasium Style)</option>
              <option value="sharp, practical, and zero-fluff">Zero-Fluff (Fast Developer Guide)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={isRunning || !topic.trim()}
            className="btn-amber-primary"
            style={{ height: '40px' }}
          >
            {isRunning ? (
              <>
                <RefreshCw size={14} style={{ animation: 'spin 1s linear infinite' }} />
                Pipeline Active...
              </>
            ) : (
              <>
                <Play size={13} fill="#0b0c10" />
                Run Multi-Agent Graph
              </>
            )}
          </button>
        </div>
      </form>

      {/* Demo Scenario Presets */}
      <div style={{
        borderTop: '1px solid var(--border-light)',
        paddingTop: '14px',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        flexWrap: 'wrap'
      }}>
        <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
          Portfolio Demo Presets:
        </span>

        <button
          type="button"
          disabled={isRunning}
          onClick={() => handleLaunchScenario(
            "How to Optimize Next.js App Router for Sub-Second Load Times",
            "8-10 mins",
            "authoritative, dynamic, and educational"
          )}
          className="btn-clean-ghost"
        >
          <CheckCircle2 size={13} color="var(--status-success)" />
          Scenario A: Clean Pass
        </button>

        <button
          type="button"
          disabled={isRunning}
          onClick={() => handleLaunchScenario(
            "Building Cyclic Multi-Agent Systems with LangGraph",
            "8-10 mins",
            "authoritative, dynamic, and educational"
          )}
          className="btn-clean-ghost"
          style={{
            background: 'var(--accent-gold-subtle)',
            borderColor: 'var(--accent-gold-border)',
            color: 'var(--accent-gold-light)'
          }}
        >
          <RefreshCw size={13} />
          Scenario B: Auditor Rejection ➔ Script Doctor Intervention (Zero Self-Evaluation Bias)
        </button>

        <button
          type="button"
          disabled={isRunning}
          onClick={() => handleLaunchScenario(
            "DeepSeek-R1 vs OpenAI o1: The Open Weights Reasoning Revolution",
            "12-15 mins",
            "curious, investigative, and counterintuitive"
          )}
          className="btn-clean-ghost"
        >
          <Sliders size={13} color="var(--accent-primary-light)" />
          Scenario C: Deep Masterclass
        </button>
      </div>
    </div>
  );
}
