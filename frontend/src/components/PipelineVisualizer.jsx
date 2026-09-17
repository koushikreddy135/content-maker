import React from 'react';
import { Search, FileText, Scale, Tag, CheckCircle2, RotateCcw, ArrowRight, Stethoscope, Sparkles, Share2 } from 'lucide-react';

export default function PipelineVisualizer({ currentNode, history, isRunning }) {
  const revisionCount = history?.job?.total_revisions || 0;
  const evals = history?.critic_evaluations || [];
  const latestEval = evals.length > 0 ? evals[evals.length - 1] : null;

  const agents = [
    { id: 'research', num: '01', name: 'Research', icon: Search, role: 'Web Search & Brief' },
    { id: 'script', num: '02', name: 'Writer', icon: FileText, role: 'Initial Draft v1' },
    { id: 'critic_script', num: '03', name: 'Auditor', icon: Scale, role: 'Retention & Hook Gate' },
    { id: 'script_doctor', num: '03b', name: 'Script Doctor', icon: Stethoscope, role: 'Decoupled Refiner' },
    { id: 'metadata_and_thumbnails', num: '04', name: 'Packaging', icon: Tag, role: 'SEO & Thumbnails' },
    { id: 'repurpose_and_broll', num: '05', name: 'Repurposing', icon: Share2, role: 'B-Roll & Social' },
    { id: 'critic_package', num: '06', name: 'Clearance', icon: CheckCircle2, role: 'Executive Clearance' },
  ];

  const getNodeStatus = (agentId) => {
    if (!isRunning && history?.job?.status === 'approved') return 'completed';
    if (!isRunning && history?.job?.status === 'escalated_to_human') return 'warning';
    
    if (currentNode === agentId) return 'active';
    if (currentNode === 'completed') return 'completed';

    // Highlight script_doctor if revisions took place
    if (agentId === 'script_doctor' && revisionCount > 0) return 'completed';

    return 'pending';
  };

  return (
    <div className="luxe-card" style={{ padding: '20px', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h3 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)' }}>
            ContentMaker Decoupled Multi-Agent Graph
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '12px', marginTop: '1px' }}>
            Tri-Agent Architecture (Writer ➔ Auditor ➔ Script Doctor) eliminating self-evaluation bias
          </p>
        </div>

        {revisionCount > 0 && (
          <div style={{
            background: 'rgba(245, 158, 11, 0.12)',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            padding: '4px 12px',
            borderRadius: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <Stethoscope size={13} color="#f59e0b" />
            <span style={{ fontSize: '12px', fontWeight: '700', color: '#fbbf24' }}>
              Script Doctor Active • Refinement Cycle #{revisionCount}
            </span>
          </div>
        )}
      </div>

      {/* Modern Sequential Nodes */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        gap: '8px'
      }}>
        {agents.map((ag) => {
          const status = getNodeStatus(ag.id);
          const Icon = ag.icon;
          const isActive = status === 'active';
          const isCompleted = status === 'completed';

          return (
            <div
              key={ag.id}
              style={{
                background: isActive
                  ? 'rgba(245, 158, 11, 0.1)'
                  : isCompleted
                  ? 'rgba(16, 185, 129, 0.05)'
                  : 'var(--bg-subtle)',
                border: `1px solid ${isActive ? '#f59e0b' : isCompleted ? 'rgba(16, 185, 129, 0.3)' : 'var(--border-light)'}`,
                borderRadius: '10px',
                padding: '12px 10px',
                textAlign: 'left',
                position: 'relative',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <div style={{
                  width: '26px',
                  height: '26px',
                  borderRadius: '6px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  background: isActive ? '#f59e0b' : isCompleted ? '#10b981' : 'rgba(255,255,255,0.05)',
                  color: isActive ? '#0b0c10' : isCompleted ? '#ffffff' : 'var(--text-muted)'
                }}>
                  <Icon size={13} />
                </div>
                <span style={{ fontSize: '10px', fontWeight: '700', color: 'var(--text-dim)', fontFamily: 'monospace' }}>
                  {ag.num}
                </span>
              </div>

              <h4 style={{ fontSize: '12px', fontWeight: '700', color: isActive ? '#fbbf24' : 'var(--text-primary)', marginBottom: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {ag.name}
              </h4>
              <p style={{ fontSize: '10px', color: 'var(--text-muted)', lineHeight: '1.2', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {ag.role}
              </p>

              <div style={{ marginTop: '6px' }}>
                {isActive && (
                  <span style={{ fontSize: '10px', fontWeight: '700', color: '#fbbf24' }}>
                    Active...
                  </span>
                )}
                {isCompleted && (
                  <span style={{ fontSize: '10px', fontWeight: '700', color: '#10b981', display: 'inline-flex', alignItems: 'center', gap: '2px' }}>
                    <CheckCircle2 size={10} /> Done
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Backward Revision Alert Banner */}
      {latestEval && latestEval.decision === 'REVISE_SCRIPT' && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.1)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          borderRadius: '10px',
          padding: '12px 16px',
          marginTop: '14px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: '6px',
              background: '#ef4444',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff'
            }}>
              <Stethoscope size={16} />
            </div>
            <div>
              <div style={{ fontSize: '12px', fontWeight: '700', color: '#f3f4f6' }}>
                Auditor Flagged Retention Bar ➔ Script Doctor Intervening
              </div>
              <div style={{ fontSize: '12px', color: '#fca5a5', marginTop: '1px' }}>
                {latestEval.summary_feedback} (Self-evaluation bias eliminated by routing to Script Doctor)
              </div>
            </div>
          </div>
          <span style={{ fontSize: '11px', fontWeight: '700', color: '#f59e0b', background: 'rgba(245,158,11,0.15)', padding: '4px 10px', borderRadius: '6px', whiteSpace: 'nowrap' }}>
            Doctor Generating Draft v2
          </span>
        </div>
      )}
    </div>
  );
}

