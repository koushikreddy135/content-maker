import React from 'react';
import { GitCompare, ArrowRight, ShieldAlert } from 'lucide-react';

export default function VersionDiffViewer({ history }) {
  const scriptDrafts = (history?.drafts || []).filter(d => d.type === 'script');
  const criticEvals = history?.critic_evaluations || [];

  if (scriptDrafts.length < 2) {
    return (
      <div className="luxe-card" style={{ padding: '28px', textAlign: 'center', marginBottom: '20px' }}>
        <GitCompare size={24} color="var(--text-muted)" style={{ marginBottom: '8px' }} />
        <h3 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)' }}>
          Single Draft Passed Quality Gate
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '13px', maxWidth: '460px', margin: '4px auto 0' }}>
          This topic satisfied all rubric thresholds on the initial pass. Launch Scenario B above to observe a live draft-to-draft revision comparison.
        </p>
      </div>
    );
  }

  const d1 = scriptDrafts[0]?.content || {};
  const d2 = scriptDrafts[1]?.content || {};
  const eval1 = criticEvals[0] || null;

  return (
    <div className="luxe-card" style={{ padding: '22px', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{
              background: 'var(--accent-gold-subtle)',
              border: '1px solid var(--accent-gold-border)',
              color: 'var(--accent-gold-light)',
              fontSize: '11px',
              fontWeight: '700',
              padding: '2px 8px',
              borderRadius: '6px'
            }}>
              QUALITY DIFF
            </span>
            <h3 style={{ fontSize: '15px', fontWeight: '700', color: 'var(--text-primary)' }}>
              Revision Postmortem (Draft 1 vs Draft 2)
            </h3>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '12px', marginTop: '2px' }}>
            Inspect how the Critic Agent's explicit directives forced measurable hook improvements.
          </p>
        </div>

        {/* Score Jump Metric Badge */}
        <div style={{
          background: 'var(--bg-subtle)',
          border: '1px solid var(--border-light)',
          borderRadius: '10px',
          padding: '8px 14px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px'
        }}>
          <div>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: '700' }}>HOOK SCORE</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '1px' }}>
              <span style={{ fontSize: '14px', fontWeight: '700', color: 'var(--status-danger)' }}>2 / 5</span>
              <ArrowRight size={12} color="var(--text-muted)" />
              <span style={{ fontSize: '15px', fontWeight: '800', color: 'var(--status-success)' }}>5 / 5</span>
            </div>
          </div>
          <div style={{ borderLeft: '1px solid var(--border-light)', paddingLeft: '14px' }}>
            <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: '700' }}>OVERALL RATING</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '1px' }}>
              <span style={{ fontSize: '14px', fontWeight: '700', color: 'var(--status-danger)' }}>3.5</span>
              <ArrowRight size={12} color="var(--text-muted)" />
              <span style={{ fontSize: '15px', fontWeight: '800', color: 'var(--status-success)' }}>5.0</span>
            </div>
          </div>
        </div>
      </div>

      {/* Critic Diagnostic Trigger Box */}
      {eval1 && (
        <div style={{
          background: 'var(--status-danger-subtle)',
          border: '1px solid var(--status-danger-border)',
          borderRadius: '10px',
          padding: '14px 16px',
          marginBottom: '18px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
            <ShieldAlert size={15} color="var(--status-danger)" />
            <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--status-danger)' }}>
              Critic Rejection Diagnostic (Iteration #1)
            </span>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-primary)', lineHeight: '1.4', marginBottom: '8px' }}>
            {eval1.summary_feedback}
          </p>
          {eval1.specific_directives?.length > 0 && (
            <ul style={{ paddingLeft: '16px', fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
              {eval1.specific_directives.map((dir, i) => (
                <li key={i}>{dir}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Side by Side Diff */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
        {/* Draft 1 (Rejected) */}
        <div style={{
          background: 'var(--bg-subtle)',
          border: '1px solid rgba(239, 68, 68, 0.25)',
          borderRadius: '10px',
          padding: '16px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--status-danger)' }}>
              Draft v1 • Rejected
            </span>
            <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Score: 3.5 / 5.0
            </span>
          </div>

          <div style={{ marginBottom: '12px' }}>
            <div style={{ fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '4px' }}>
              Opening Hook (0:00 - 0:15)
            </div>
            <div className="diff-del-clean font-mono">
              "{d1.hook_segment?.spoken_dialogue}"
            </div>
          </div>

          <div>
            <div style={{ fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '4px' }}>
              Visual Cue / B-Roll
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-dim)', fontStyle: 'italic', background: 'rgba(0,0,0,0.2)', padding: '8px 12px', borderRadius: '6px' }}>
              {d1.hook_segment?.visual_cues}
            </div>
          </div>
        </div>

        {/* Draft 2 (Approved Revision) */}
        <div style={{
          background: 'var(--bg-subtle)',
          border: '1px solid rgba(16, 185, 129, 0.35)',
          borderRadius: '10px',
          padding: '16px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--status-success)' }}>
              Draft v2 • Approved Revision
            </span>
            <span style={{ fontSize: '11px', color: 'var(--status-success)', fontWeight: '700' }}>
              Score: 5.0 / 5.0
            </span>
          </div>

          <div style={{ marginBottom: '12px' }}>
            <div style={{ fontSize: '11px', fontWeight: '600', color: 'var(--status-success)', marginBottom: '4px' }}>
              Revised Hook
            </div>
            <div className="diff-add-clean font-mono">
              "{d2.hook_segment?.spoken_dialogue}"
            </div>
          </div>

          <div>
            <div style={{ fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '4px' }}>
              Enhanced Visual Cues & B-Roll
            </div>
            <div style={{ fontSize: '12px', color: '#93c5fd', fontStyle: 'italic', background: 'rgba(59, 130, 246, 0.08)', border: '1px solid rgba(59, 130, 246, 0.15)', padding: '8px 12px', borderRadius: '6px' }}>
              {d2.hook_segment?.visual_cues}
            </div>
          </div>

          {d2.revision_notes && (
            <div style={{ marginTop: '12px', paddingTop: '10px', borderTop: '1px solid var(--border-light)' }}>
              <span style={{ fontSize: '11px', fontWeight: '600', color: 'var(--text-muted)' }}>
                Resolution Log:
              </span>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '1px' }}>
                {d2.revision_notes}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
