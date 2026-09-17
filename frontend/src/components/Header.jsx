import React from 'react';
import { Film, ShieldCheck, History, Sparkles } from 'lucide-react';

export default function Header({ onOpenHistory, onOpenExplainability, currentJob }) {
  return (
    <header className="luxe-card" style={{ padding: '14px 22px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 2px 10px rgba(245, 158, 11, 0.35)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <Film size={20} color="#0b0c10" />
        </div>
        
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 style={{ fontSize: '18px', fontWeight: '800', color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
              ContentMaker
            </h1>
            <span style={{
              background: 'var(--accent-gold-subtle)',
              border: '1px solid var(--accent-gold-border)',
              color: 'var(--accent-gold-light)',
              fontSize: '11px',
              fontWeight: '700',
              padding: '2px 8px',
              borderRadius: '6px'
            }}>
              Decoupled Multi-Agent Studio
            </span>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '12px', marginTop: '1px' }}>
            Tri-Agent YouTube Production Engine • Writer ➔ Retention Auditor ➔ Script Doctor
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        {/* Live operational indicator */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          background: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid var(--border-light)',
          padding: '4px 10px',
          borderRadius: '20px'
        }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--status-success)', display: 'inline-block', boxShadow: '0 0 8px var(--status-success)' }} />
          <span style={{ fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)' }}>Graph Active</span>
        </div>

        {currentJob?.final_overall_score && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'var(--status-success-subtle)',
            border: '1px solid var(--status-success-border)',
            padding: '5px 12px',
            borderRadius: '8px'
          }}>
            <ShieldCheck size={14} color="var(--status-success)" />
            <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--status-success)' }}>
              {currentJob.final_overall_score.toFixed(1)} / 5.0
            </span>
          </div>
        )}

        <button onClick={onOpenExplainability} className="btn-clean-ghost" title="View 6-Dimension Evaluation Rubric">
          <ShieldCheck size={14} color="var(--accent-gold-light)" />
          Rubric Scorecard
        </button>

        <button onClick={onOpenHistory} className="btn-clean-ghost">
          <History size={14} color="var(--accent-primary-light)" />
          History
        </button>
      </div>
    </header>
  );
}
