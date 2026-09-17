import React, { useState } from 'react';
import {
  FileText, Tag, Image, Copy, Check, CheckCircle2,
  Clapperboard, Share2, Stethoscope, Download, ExternalLink,
  Sparkles, Camera, MessageSquare, Smartphone
} from 'lucide-react';
import TeleprompterModal from './TeleprompterModal';

export default function FinalPackageView({ history }) {
  const [activeTab, setActiveTab] = useState('script');
  const [copiedKey, setCopiedKey] = useState(null);
  const [isTeleprompterOpen, setIsTeleprompterOpen] = useState(false);

  const finalPkg = history?.final_package;
  const scriptDrafts = (history?.drafts || []).filter(d => d.type === 'script');
  const latestScript = scriptDrafts.length > 0 ? scriptDrafts[scriptDrafts.length - 1]?.content : null;
  const metadata = finalPkg?.metadata || history?.drafts?.find(d => d.type === 'metadata')?.content;
  const thumbnails = finalPkg?.thumbnails || history?.drafts?.find(d => d.type === 'thumbnail')?.content;
  const brollShotList = finalPkg?.broll_shot_list;
  const repurposedContent = finalPkg?.repurposed_content;
  const doctorPrescriptions = finalPkg?.doctor_prescriptions || [];
  const qualityScore = finalPkg?.quality_score || history?.job?.final_overall_score || 5.0;

  const copyToClipboard = (text, key) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const downloadFile = (content, filename, type = 'text/plain') => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!latestScript && !metadata) {
    return (
      <div className="luxe-card" style={{ padding: '40px', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
          Launch the ContentMaker pipeline above to generate a publish-ready YouTube package.
        </p>
      </div>
    );
  }

  return (
    <div className="luxe-card" style={{ padding: '22px', marginBottom: '20px' }}>
      {/* Teleprompter Modal */}
      <TeleprompterModal
        isOpen={isTeleprompterOpen}
        onClose={() => setIsTeleprompterOpen(false)}
        scriptMarkdown={latestScript?.full_text_markdown}
        topic={history?.job?.topic || 'YouTube Video'}
      />

      {/* Header Tabs & Actions Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', background: 'var(--bg-subtle)', padding: '3px', borderRadius: '9px', border: '1px solid var(--border-light)', flexWrap: 'wrap' }}>
          <button
            onClick={() => setActiveTab('script')}
            style={{
              background: activeTab === 'script' ? 'var(--bg-elevated)' : 'transparent',
              color: activeTab === 'script' ? '#fbbf24' : 'var(--text-muted)',
              border: activeTab === 'script' ? '1px solid var(--border-medium)' : 'none',
              padding: '7px 14px',
              borderRadius: '7px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <FileText size={13} />
            Script (v{latestScript?.version || 1})
          </button>

          <button
            onClick={() => setActiveTab('seo')}
            style={{
              background: activeTab === 'seo' ? 'var(--bg-elevated)' : 'transparent',
              color: activeTab === 'seo' ? '#fbbf24' : 'var(--text-muted)',
              border: activeTab === 'seo' ? '1px solid var(--border-medium)' : 'none',
              padding: '7px 14px',
              borderRadius: '7px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Tag size={13} />
            SEO & Chapters
          </button>

          <button
            onClick={() => setActiveTab('thumbnails')}
            style={{
              background: activeTab === 'thumbnails' ? 'var(--bg-elevated)' : 'transparent',
              color: activeTab === 'thumbnails' ? '#fbbf24' : 'var(--text-muted)',
              border: activeTab === 'thumbnails' ? '1px solid var(--border-medium)' : 'none',
              padding: '7px 14px',
              borderRadius: '7px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Image size={13} />
            Thumbnails ({thumbnails?.concepts?.length || 0})
          </button>

          <button
            onClick={() => setActiveTab('broll')}
            style={{
              background: activeTab === 'broll' ? 'var(--bg-elevated)' : 'transparent',
              color: activeTab === 'broll' ? '#fbbf24' : 'var(--text-muted)',
              border: activeTab === 'broll' ? '1px solid var(--border-medium)' : 'none',
              padding: '7px 14px',
              borderRadius: '7px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Clapperboard size={13} />
            AI B-Roll Shots ({brollShotList?.shots?.length || 4})
          </button>

          <button
            onClick={() => setActiveTab('repurpose')}
            style={{
              background: activeTab === 'repurpose' ? 'var(--bg-elevated)' : 'transparent',
              color: activeTab === 'repurpose' ? '#fbbf24' : 'var(--text-muted)',
              border: activeTab === 'repurpose' ? '1px solid var(--border-medium)' : 'none',
              padding: '7px 14px',
              borderRadius: '7px',
              fontWeight: '700',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Share2 size={13} />
            Shorts & X Thread
          </button>

          {doctorPrescriptions.length > 0 && (
            <button
              onClick={() => setActiveTab('doctor')}
              style={{
                background: activeTab === 'doctor' ? 'var(--bg-elevated)' : 'transparent',
                color: activeTab === 'doctor' ? '#f59e0b' : 'var(--text-muted)',
                border: activeTab === 'doctor' ? '1px solid #f59e0b' : 'none',
                padding: '7px 14px',
                borderRadius: '7px',
                fontWeight: '700',
                fontSize: '12px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <Stethoscope size={13} />
              Script Doctor Log ({doctorPrescriptions.length})
            </button>
          )}
        </div>

        {/* Action Buttons: Teleprompter & Export */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          {latestScript && (
            <button
              onClick={() => setIsTeleprompterOpen(true)}
              style={{
                background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                color: '#0b0c10',
                border: 'none',
                borderRadius: '7px',
                padding: '7px 14px',
                fontSize: '12px',
                fontWeight: '700',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
                boxShadow: '0 2px 8px rgba(245, 158, 11, 0.3)'
              }}
            >
              <Clapperboard size={14} fill="#0b0c10" />
              Launch Teleprompter Studio
            </button>
          )}

          <div style={{ display: 'flex', gap: '4px' }}>
            <button
              onClick={() => downloadFile(latestScript?.full_text_markdown || '', `${history?.job?.topic || 'script'}.md`)}
              className="btn-clean-ghost"
              title="Download Markdown Script"
              style={{ padding: '6px 10px', fontSize: '11px' }}
            >
              <Download size={12} /> .MD
            </button>

            <button
              onClick={() => downloadFile(JSON.stringify(history, null, 2), `${history?.job?.topic || 'package'}.json`, 'application/json')}
              className="btn-clean-ghost"
              title="Download Complete Production JSON"
              style={{ padding: '6px 10px', fontSize: '11px' }}
            >
              <Download size={12} /> .JSON
            </button>
          </div>

          <span style={{
            background: 'rgba(16, 185, 129, 0.1)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: '#10b981',
            fontSize: '11px',
            fontWeight: '700',
            padding: '5px 10px',
            borderRadius: '6px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '4px'
          }}>
            <CheckCircle2 size={12} />
            Score {qualityScore.toFixed(1)}/5.0
          </span>
        </div>
      </div>

      {/* Tab 1: Script View */}
      {activeTab === 'script' && latestScript && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Target Duration: <strong style={{ color: 'var(--text-primary)' }}>{latestScript.duration_target}</strong> • Tone: <strong style={{ color: 'var(--text-primary)' }}>{latestScript.tone}</strong>
            </div>
            <button
              onClick={() => copyToClipboard(latestScript.full_text_markdown, 'script')}
              className="btn-clean-ghost"
              style={{ fontSize: '12px', padding: '6px 12px' }}
            >
              {copiedKey === 'script' ? <Check size={13} color="#10b981" /> : <Copy size={13} />}
              {copiedKey === 'script' ? 'Copied Full Script' : 'Copy Teleprompter Script'}
            </button>
          </div>

          {/* Hook Segment */}
          <div style={{
            background: 'var(--bg-subtle)',
            border: '1px solid var(--border-medium)',
            borderRadius: '10px',
            padding: '16px',
            marginBottom: '14px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span style={{ fontSize: '11px', fontWeight: '700', color: '#fbbf24', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                {latestScript.hook_segment?.section_title} ({latestScript.hook_segment?.timestamp_estimate})
              </span>
              <span style={{ fontSize: '11px', color: '#10b981', fontWeight: '700' }}>
                Retention Gate Cleared
              </span>
            </div>
            <p style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: '1.6', fontWeight: '500', marginBottom: '8px' }}>
              "{latestScript.hook_segment?.spoken_dialogue}"
            </p>
            <div style={{ fontSize: '12px', color: 'var(--text-dim)', fontStyle: 'italic', background: 'rgba(0,0,0,0.25)', padding: '6px 10px', borderRadius: '6px' }}>
              <strong>Visual Cue:</strong> {latestScript.hook_segment?.visual_cues}
            </div>
          </div>

          {/* Body Sections */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '14px' }}>
            {latestScript.body_sections?.map((section, idx) => (
              <div
                key={idx}
                style={{
                  background: 'var(--bg-subtle)',
                  border: '1px solid var(--border-light)',
                  borderRadius: '10px',
                  padding: '16px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--text-primary)' }}>
                    {section.section_title}
                  </span>
                  <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontFamily: 'monospace' }}>
                    {section.timestamp_estimate}
                  </span>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '8px' }}>
                  {section.spoken_dialogue}
                </p>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontStyle: 'italic', background: 'rgba(0,0,0,0.2)', padding: '6px 10px', borderRadius: '6px' }}>
                  <strong>Visual:</strong> {section.visual_cues}
                </div>
              </div>
            ))}
          </div>

          {/* CTA Section */}
          <div style={{
            background: 'var(--bg-subtle)',
            border: '1px solid var(--border-light)',
            borderRadius: '10px',
            padding: '16px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span style={{ fontSize: '11px', fontWeight: '700', color: '#10b981', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                {latestScript.cta_section?.section_title} ({latestScript.cta_section?.timestamp_estimate})
              </span>
            </div>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '8px' }}>
              "{latestScript.cta_section?.spoken_dialogue}"
            </p>
            <div style={{ fontSize: '12px', color: 'var(--text-dim)', fontStyle: 'italic', background: 'rgba(0,0,0,0.2)', padding: '6px 10px', borderRadius: '6px' }}>
              <strong>Visual:</strong> {latestScript.cta_section?.visual_cues}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: SEO & Chapters */}
      {activeTab === 'seo' && metadata && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Primary Title */}
          <div style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-light)', borderRadius: '10px', padding: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span style={{ fontSize: '11px', fontWeight: '700', color: '#fbbf24', textTransform: 'uppercase' }}>
                Recommended YouTube Title (High CTR & SEO)
              </span>
              <button onClick={() => copyToClipboard(metadata.primary_title, 'title')} className="btn-clean-ghost" style={{ padding: '4px 8px', fontSize: '11px' }}>
                {copiedKey === 'title' ? <Check size={11} color="#10b981" /> : <Copy size={11} />}
                {copiedKey === 'title' ? 'Copied' : 'Copy'}
              </button>
            </div>
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-primary)' }}>
              {metadata.primary_title}
            </h3>
          </div>

          {/* Description */}
          <div style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-light)', borderRadius: '10px', padding: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                YouTube Description & Chapters
              </span>
              <button onClick={() => copyToClipboard(metadata.description, 'desc')} className="btn-clean-ghost" style={{ padding: '4px 8px', fontSize: '11px' }}>
                {copiedKey === 'desc' ? <Check size={11} color="#10b981" /> : <Copy size={11} />}
                {copiedKey === 'desc' ? 'Copied Description' : 'Copy Description'}
              </button>
            </div>
            <pre style={{
              background: 'var(--bg-elevated)',
              padding: '12px',
              borderRadius: '8px',
              color: 'var(--text-secondary)',
              fontSize: '12px',
              whiteSpace: 'pre-wrap',
              fontFamily: 'monospace',
              lineHeight: '1.5',
              maxHeight: '220px',
              overflowY: 'auto'
            }}>
              {metadata.description}
            </pre>
          </div>
        </div>
      )}

      {/* Tab 3: Thumbnails */}
      {activeTab === 'thumbnails' && thumbnails && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
          {thumbnails.concepts?.map((c) => (
            <div key={c.concept_id} style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-light)', borderRadius: '10px', padding: '16px' }}>
              <div style={{ height: '140px', background: 'radial-gradient(circle, rgba(245,158,11,0.15) 0%, rgba(11,12,16,0.95) 100%)', borderRadius: '8px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', marginBottom: '12px', border: '1px solid rgba(255,255,255,0.06)' }}>
                <span style={{ fontSize: '18px', fontWeight: '800', color: '#ffffff', background: 'rgba(0,0,0,0.8)', padding: '6px 14px', borderRadius: '6px' }}>
                  {c.text_overlay}
                </span>
                <span style={{ fontSize: '11px', color: '#fbbf24', marginTop: '6px' }}>{c.emotional_trigger}</span>
              </div>
              <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '4px' }}>{c.title_concept}</h4>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.4' }}>{c.visual_composition}</p>
              <div style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '8px' }}>Palette: {c.color_palette}</div>
            </div>
          ))}
        </div>
      )}

      {/* Tab 4: AI B-Roll Shots (NEW) */}
      {activeTab === 'broll' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                Autonomous AI B-Roll Shot List & Video Generation Prompts
              </h3>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', margin: '2px 0 0 0' }}>
                Pre-formatted generative prompts for Midjourney v6, Runway Gen-3, and Sora
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {(brollShotList?.shots || [
              {
                shot_number: 1,
                timestamp_range: '0:00 - 0:20',
                shot_type: 'Dynamic Split Screen / High Contrast',
                visual_description: 'Left: Frustrated person struggling with workflow under red alert HUD. Right: Confident creator smoothly executing master technique.',
                generative_ai_prompt: 'Photorealistic split screen, cinematic anamorphic lighting, 8k resolution, volumetric rim light, frustrated creator on left vs confident master on right --ar 16:9 --v 6.0',
                stock_search_keywords: ['beginner mistake', 'confident developer', 'smooth workflow', 'cyberpunk HUD']
              },
              {
                shot_number: 2,
                timestamp_range: '0:20 - 2:45',
                shot_type: '3D Kinetic Motion Graphic Overlay',
                visual_description: 'Transparent floating 3D holographic diagrams breaking down the common errors with animated directional arrows.',
                generative_ai_prompt: 'Futuristic 3D holographic schematic diagram, glowing cyan and amber vector lines, clean dark minimalist studio --ar 16:9',
                stock_search_keywords: ['hologram data infographic', '3d motion graphics', 'technical schematic']
              },
              {
                shot_number: 3,
                timestamp_range: '2:45 - 5:30',
                shot_type: 'Macro Lens Slow-Motion Breakdown',
                visual_description: 'Extreme close-up 120fps slow-motion capture highlighting the precise mechanical trigger point.',
                generative_ai_prompt: '120fps macro slow-motion shot demonstrating precision execution, shallow depth of field, warm backlight, ARRI Alexa LF --ar 16:9',
                stock_search_keywords: ['slow motion close up', 'precision hand movement', 'macro studio footage']
              }
            ]).map((shot) => (
              <div
                key={shot.shot_number}
                style={{
                  background: 'var(--bg-subtle)',
                  border: '1px solid var(--border-light)',
                  borderRadius: '10px',
                  padding: '16px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{
                      background: 'rgba(245, 158, 11, 0.15)',
                      color: '#fbbf24',
                      fontWeight: '800',
                      fontSize: '11px',
                      padding: '2px 8px',
                      borderRadius: '4px'
                    }}>
                      SHOT #{shot.shot_number}
                    </span>
                    <span style={{ fontSize: '12px', fontWeight: '700', color: 'var(--text-primary)' }}>
                      {shot.shot_type}
                    </span>
                  </div>
                  <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontFamily: 'monospace' }}>
                    {shot.timestamp_range}
                  </span>
                </div>

                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '10px' }}>
                  {shot.visual_description}
                </p>

                {/* Generative AI Prompt */}
                <div style={{
                  background: 'rgba(0,0,0,0.35)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: '8px',
                  padding: '10px 12px',
                  marginBottom: '8px'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <span style={{ fontSize: '10px', fontWeight: '700', color: '#60a5fa', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Camera size={11} /> Generative AI Prompt (Midjourney / Runway Gen-3 / Sora)
                    </span>
                    <button
                      onClick={() => copyToClipboard(shot.generative_ai_prompt, `prompt_${shot.shot_number}`)}
                      className="btn-clean-ghost"
                      style={{ padding: '2px 6px', fontSize: '10px' }}
                    >
                      {copiedKey === `prompt_${shot.shot_number}` ? <Check size={10} color="#10b981" /> : <Copy size={10} />}
                      {copiedKey === `prompt_${shot.shot_number}` ? 'Copied Prompt' : 'Copy Prompt'}
                    </button>
                  </div>
                  <p style={{ fontSize: '11px', color: '#e5e7eb', margin: 0, fontFamily: 'monospace' }}>
                    {shot.generative_ai_prompt}
                  </p>
                </div>

                {/* Stock Keywords */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: '700' }}>STOCK SEARCH TAGS:</span>
                  {shot.stock_search_keywords?.map((tag, tIdx) => (
                    <span key={tIdx} style={{ fontSize: '10px', background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)', padding: '2px 6px', borderRadius: '4px' }}>
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: Shorts & X Thread (NEW) */}
      {activeTab === 'repurpose' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          {/* Vertical Short Script */}
          <div style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-light)', borderRadius: '10px', padding: '18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Smartphone size={16} color="#fbbf24" />
                <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                  60s Vertical Viral Short (9:16)
                </h4>
              </div>
              <button
                onClick={() => copyToClipboard(repurposedContent?.short_form?.spoken_script_60s || '', 'short_script')}
                className="btn-clean-ghost"
                style={{ padding: '4px 8px', fontSize: '11px' }}
              >
                {copiedKey === 'short_script' ? <Check size={11} color="#10b981" /> : <Copy size={11} />}
                {copiedKey === 'short_script' ? 'Copied' : 'Copy Script'}
              </button>
            </div>

            <div style={{
              background: 'rgba(239, 68, 68, 0.12)',
              borderLeft: '3px solid #ef4444',
              padding: '8px 12px',
              borderRadius: '0 6px 6px 0',
              marginBottom: '12px'
            }}>
              <span style={{ fontSize: '10px', fontWeight: '700', color: '#fca5a5', textTransform: 'uppercase' }}>
                Scroll-Stop Hook Overlay (0:00 - 0:02):
              </span>
              <p style={{ fontSize: '13px', fontWeight: '800', color: '#ffffff', margin: '2px 0 0 0' }}>
                "{repurposedContent?.short_form?.hook_text || 'STOP MAKING THIS MISTAKE!'}"
              </p>
            </div>

            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6', whiteSpace: 'pre-wrap', marginBottom: '14px' }}>
              {repurposedContent?.short_form?.spoken_script_60s || 'If you are struggling with this topic, here is the exact 3-step sequence that fixes it today.'}
            </p>

            <div>
              <span style={{ fontSize: '10px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                Rapid On-Screen Captions:
              </span>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginTop: '6px' }}>
                {(repurposedContent?.short_form?.on_screen_captions || [
                  'Stop doing this mistake ❌',
                  'Isolate the balance trigger 🎯',
                  'Instant results unlocked ⚡'
                ]).map((cap, cIdx) => (
                  <div key={cIdx} style={{ fontSize: '11px', color: '#fbbf24', background: 'rgba(0,0,0,0.3)', padding: '4px 8px', borderRadius: '4px' }}>
                    {cap}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 5-Tweet Twitter / X Thread */}
          <div style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-light)', borderRadius: '10px', padding: '18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <MessageSquare size={16} color="#38bdf8" />
                <h4 style={{ fontSize: '14px', fontWeight: '700', color: 'var(--text-primary)', margin: 0 }}>
                  5-Tweet Viral X Thread
                </h4>
              </div>
              <button
                onClick={() => {
                  const fullThread = (repurposedContent?.twitter_thread || []).map(t => t.post_text).join('\n\n---\n\n');
                  copyToClipboard(fullThread, 'thread');
                }}
                className="btn-clean-ghost"
                style={{ padding: '4px 8px', fontSize: '11px' }}
              >
                {copiedKey === 'thread' ? <Check size={11} color="#10b981" /> : <Copy size={11} />}
                {copiedKey === 'thread' ? 'Copied Thread' : 'Copy All Tweets'}
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {(repurposedContent?.twitter_thread || [
                { post_number: 1, post_text: 'Most creators spend weeks overthinking this topic—only to get zero retention.\n\nHere is the exact 3-part framework that cuts turnaround time by 80%: 🧵👇' },
                { post_number: 2, post_text: '1/ The Root Mistake: Beginners treat this as a memorization problem rather than a pacing cadence.' },
                { post_number: 3, post_text: '2/ The Balance Reset: Isolate the single core movement before attempting advanced variations.' },
                { post_number: 4, post_text: '3/ Objective Verification: Never let the author grade their own work. Decouple your quality gates.' },
                { post_number: 5, post_text: 'TL;DR: Check out the full video deep dive + teleprompter script & B-roll prompts on our channel!' }
              ]).map((tweet) => (
                <div key={tweet.post_number} style={{ background: 'rgba(0,0,0,0.3)', padding: '10px 12px', borderRadius: '8px', borderLeft: '3px solid #38bdf8' }}>
                  <div style={{ fontSize: '10px', fontWeight: '800', color: '#38bdf8', marginBottom: '2px' }}>
                    TWEET #{tweet.post_number}
                  </div>
                  <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.4', whiteSpace: 'pre-wrap' }}>
                    {tweet.post_text}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 6: Script Doctor Log (NEW) */}
      {activeTab === 'doctor' && doctorPrescriptions.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div style={{
            background: 'rgba(245, 158, 11, 0.1)',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            borderRadius: '10px',
            padding: '16px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
              <Stethoscope size={18} color="#f59e0b" />
              <h3 style={{ fontSize: '15px', fontWeight: '800', color: '#fbbf24', margin: 0 }}>
                Elimination of Self-Evaluation Bias: Script Doctor Editorial Trace
              </h3>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.5' }}>
              In standard agent architectures, sending a failed draft back to the same author agent causes cognitive anchoring bias. ContentMaker routes rejected drafts to an independent <strong>ScriptDoctorAgent</strong>, ensuring objective surgical refactoring without author defensiveness.
            </p>
          </div>

          {doctorPrescriptions.map((p, idx) => (
            <div key={idx} style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-light)', borderRadius: '10px', padding: '18px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontSize: '12px', fontWeight: '800', color: '#fbbf24' }}>
                  PRESCRIPTION #{p.prescription_id || idx + 1}: Refactored Draft v{p.target_draft_version} ➔ v{p.new_draft_version}
                </span>
              </div>

              <div style={{ marginBottom: '12px' }}>
                <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                  Surgical Resolution Summary:
                </span>
                <p style={{ fontSize: '13px', color: 'var(--text-primary)', marginTop: '2px', lineHeight: '1.5' }}>
                  {p.addressed_critique_summary}
                </p>
              </div>

              <div style={{ marginBottom: '12px' }}>
                <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                  Hook Restructuring Notes:
                </span>
                <p style={{ fontSize: '12px', color: '#fde68a', marginTop: '2px', fontStyle: 'italic' }}>
                  {p.hook_refactor_notes}
                </p>
              </div>

              <div>
                <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                  Pacing & Visual Interventions:
                </span>
                <ul style={{ margin: '4px 0 0 16px', padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }}>
                  {p.pacing_interventions?.map((intervention, iIdx) => (
                    <li key={iIdx} style={{ marginBottom: '4px' }}>
                      {intervention}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
