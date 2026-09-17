import React from 'react';
import { X, ShieldCheck } from 'lucide-react';

export default function ExplainabilityDrawer({ isOpen, onClose, history }) {
  if (!isOpen) return null;

  const evals = history?.critic_evaluations || [];
  const latestEval = evals.length > 0 ? evals[evals.length - 1] : null;
  const rubric = latestEval?.rubric_scores || latestEval?.rubric;

  const dimensions = [
    { key: 'hook_strength', label: 'Hook Strength (0-15s)', desc: 'Curiosity gap, no throat-clearing, high stakes contrast' },
    { key: 'clarity_and_flow', label: 'Clarity & Logical Flow', desc: 'Narrative structure, intuitive transitions, digestible concepts' },
    { key: 'pacing_and_engagement', label: 'Pacing & B-Roll Cues', desc: 'Visual cue density, retention resets, pattern interrupts' },
    { key: 'seo_keyword_alignment', label: 'SEO Keyword Alignment', desc: 'Natural search keyword integration across script & metadata' },
    { key: 'thumbnail_click_worthiness', label: 'Thumbnail Click-Worthiness', desc: 'High visual contrast, 2-4 punchy words, emotional trigger' },
    { key: 'brand_and_tone_fit', label: 'Brand & Authority Fit', desc: 'Educational credibility, dynamic delivery, zero fluff' }
  ];

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(6px)',
      display: 'flex',
      justifyContent: 'flex-end',
      zIndex: 1000
    }}>
      <div style={{
        width: '100%',
        maxWidth: '520px',
        background: 'var(--bg-card)',
        borderLeft: '1px solid var(--border-light)',
        height: '100%',
        overflowY: 'auto',
        padding: '24px',
        boxShadow: 'var(--shadow-float)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldCheck size={18} color="var(--accent-gold-light)" />
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)' }}>
              Evaluation Rubric Scorecard
            </h3>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={18} />
          </button>
        </div>

        <p style={{ color: 'var(--text-muted)', fontSize: '13px', lineHeight: '1.5', marginBottom: '18px' }}>
          Auditable quality-gating scores. Every dimension is evaluated on a 1–5 scale with required line justifications and a minimum 4.0 passing bar.
        </p>

        {/* Decision Summary */}
        {latestEval && (
          <div style={{
            background: latestEval.decision === 'APPROVED' ? 'var(--status-success-subtle)' : 'var(--status-danger-subtle)',
            border: `1px solid ${latestEval.decision === 'APPROVED' ? 'var(--status-success-border)' : 'var(--status-danger-border)'}`,
            borderRadius: '10px',
            padding: '14px',
            marginBottom: '20px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
              <span style={{ fontSize: '12px', fontWeight: '700', color: latestEval.decision === 'APPROVED' ? 'var(--status-success)' : 'var(--status-danger)' }}>
                Decision: {latestEval.decision}
              </span>
              <span style={{ fontSize: '14px', fontWeight: '800', color: 'var(--text-primary)' }}>
                {latestEval.overall_score?.toFixed(1)} / 5.0
              </span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
              {latestEval.summary_feedback}
            </p>
          </div>
        )}

        {/* 6 Dimensions List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {dimensions.map((dim) => {
            const scoreObj = rubric ? rubric[dim.key] : null;
            const score = scoreObj?.score || 5;
            const justification = scoreObj?.justification || 'Validated against channel standards.';
            const isFailing = score < 3;

            return (
              <div
                key={dim.key}
                style={{
                  background: 'var(--bg-subtle)',
                  border: '1px solid var(--border-light)',
                  borderRadius: '10px',
                  padding: '12px 14px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <span style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-primary)' }}>
                    {dim.label}
                  </span>
                  <span style={{
                    fontSize: '12px',
                    fontWeight: '700',
                    color: isFailing ? 'var(--status-danger)' : score === 5 ? 'var(--status-success)' : 'var(--accent-gold-light)'
                  }}>
                    {score} / 5
                  </span>
                </div>

                {/* Progress bar */}
                <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.06)', borderRadius: '2px', marginBottom: '6px', overflow: 'hidden' }}>
                  <div style={{
                    width: `${(score / 5) * 100}%`,
                    height: '100%',
                    background: isFailing ? 'var(--status-danger)' : score === 5 ? 'var(--status-success)' : 'var(--accent-gold)',
                    borderRadius: '2px'
                  }} />
                </div>

                <p style={{ fontSize: '11px', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                  {justification}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
