import React from 'react';
import { X, History, ArrowRight } from 'lucide-react';

export default function HistoryModal({ isOpen, onClose, jobs, onSelectJob }) {
  if (!isOpen) return null;

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
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div className="luxe-card" style={{
        width: '100%',
        maxWidth: '620px',
        maxHeight: '80vh',
        overflowY: 'auto',
        padding: '22px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <History size={18} color="var(--accent-gold-light)" />
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)' }}>
              Generation History ({jobs.length})
            </h3>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={18} />
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {jobs.map((j) => (
            <div
              key={j.id}
              onClick={() => {
                onSelectJob(j.id);
                onClose();
              }}
              style={{
                background: 'var(--bg-subtle)',
                border: '1px solid var(--border-light)',
                borderRadius: '10px',
                padding: '12px 14px',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'var(--accent-gold-border)';
                e.currentTarget.style.background = 'var(--bg-card-hover)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-light)';
                e.currentTarget.style.background = 'var(--bg-subtle)';
              }}
            >
              <div>
                <h4 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '3px' }}>
                  {j.topic}
                </h4>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'flex', gap: '10px' }}>
                  <span>ID: {j.id}</span>
                  <span>Revisions: {j.total_revisions}</span>
                  <span>Status: <strong style={{ color: j.status === 'approved' ? 'var(--status-success)' : 'var(--accent-gold)' }}>{j.status}</strong></span>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                {j.final_overall_score && (
                  <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--status-success)' }}>
                    {j.final_overall_score.toFixed(1)} / 5.0
                  </span>
                )}
                <ArrowRight size={14} color="var(--text-dim)" />
              </div>
            </div>
          ))}

          {jobs.length === 0 && (
            <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px 0', fontSize: '13px' }}>
              No previous runs recorded.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
