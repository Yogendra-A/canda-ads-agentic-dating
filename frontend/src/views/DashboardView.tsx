import React from 'react';
import type { DemoOverview } from '../types';
import { Users, Sparkles, HeartHandshake, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Flame, Compass } from 'lucide-react';

interface Props {
  demo: DemoOverview | null;
  onNavigate: (tab: string, personId?: string, sessionId?: string) => void;
}

export const DashboardView: React.FC<Props> = ({ demo, onNavigate }) => {
  if (!demo) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div className="badge badge-gold pulse-element" style={{ marginBottom: 16 }}>Connecting to Agentic Engine...</div>
        <p style={{ color: 'var(--text-secondary)' }}>Loading system telemetry and precomputed records...</p>
      </div>
    );
  }

  const isDatasetIncomplete = demo.total_people < 25;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
      {/* Alert Banner if Incomplete */}
      {isDatasetIncomplete ? (
        <div style={{
          background: 'rgba(239, 68, 68, 0.12)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          borderRadius: 'var(--radius-md)',
          padding: '16px 20px',
          display: 'flex',
          alignItems: 'center',
          gap: 14,
          color: '#fca5a5'
        }}>
          <AlertTriangle size={24} color="#ef4444" style={{ flexShrink: 0 }} />
          <div>
            <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>Dataset Incomplete Warning</div>
            <div style={{ fontSize: '0.85rem', color: '#f87171' }}>
              The dataset currently contains {demo.total_people} of the mandatory 25 verified public figures. Please visit the Settings / Ingestion tab to import or scrape profiles.
            </div>
          </div>
        </div>
      ) : (
        <div style={{
          background: 'rgba(16, 185, 129, 0.08)',
          border: '1px solid rgba(16, 185, 129, 0.25)',
          borderRadius: 'var(--radius-md)',
          padding: '14px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          color: '#6ee7b7'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <ShieldCheck size={20} color="#10b981" />
            <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>
              Full Demonstration Verified: <strong>{demo.total_people} Real People</strong> loaded with official LinkedIn and public Instagram profiles.
            </span>
          </div>
          <span className="badge badge-emerald">Ready for Inspection</span>
        </div>
      )}

      {/* Hero Welcome & Identity */}
      <div className="glass-panel" style={{ padding: '36px 32px', position: 'relative', overflow: 'hidden' }}>
        <div style={{ maxWidth: 720 }}>
          <div className="badge badge-gold" style={{ marginBottom: 12 }}>
            <Sparkles size={12} /> Autonomous Agentic AI Dating
          </div>
          <h1 style={{ fontSize: '2.4rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: 12, lineHeight: 1.2 }}>
            Where Personal AI Agents <br />
            <span style={{ color: 'var(--accent-gold)' }}>Date & Evaluate Compatibility</span> for Humans.
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', lineHeight: 1.6, marginBottom: 24 }}>
            Each person is represented by an autonomous AI agent configured from verified public LinkedIn and Instagram profiles. 
            Agents conduct observable, multi-turn dating interactions, explore shared philosophies, and compute bidirectional compatibility rankings.
          </p>

          <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
            <button className="btn btn-primary" onClick={() => onNavigate('dating')}>
              <Flame size={16} /> Enter Agent Dating Room
            </button>
            <button className="btn btn-secondary" onClick={() => onNavigate('directory')}>
              <Compass size={16} /> Explore 25 Verified Profiles
            </button>
            <button className="btn btn-secondary" onClick={() => onNavigate('rankings')}>
              <HeartHandshake size={16} /> View Compatibility Matrix
            </button>
          </div>
        </div>
      </div>

      {/* 4 Stat Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 20 }}>
        <div className="glass-panel" style={{ padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 600, textTransform: 'uppercase' }}>Verified People</span>
            <Users size={18} color="var(--accent-gold)" />
          </div>
          <div className="metric-number-gold">{demo.total_people}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: 4 }}>
            {demo.verified_people} with dual verified source links
          </div>
        </div>

        <div className="glass-panel" style={{ padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 600, textTransform: 'uppercase' }}>Profile Analyses</span>
            <CheckCircle2 size={18} color="#34d399" />
          </div>
          <div className="metric-number">{demo.analyzed_profiles}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: 4 }}>
            Evidence-backed behavioral dossiers
          </div>
        </div>

        <div className="glass-panel" style={{ padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 600, textTransform: 'uppercase' }}>Agent Dating Sessions</span>
            <HeartHandshake size={18} color="#fb7185" />
          </div>
          <div className="metric-number" style={{ color: '#fb7185' }}>{demo.completed_dating_sessions}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: 4 }}>
            Observable multi-turn conversations
          </div>
        </div>

        <div className="glass-panel" style={{ padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 600, textTransform: 'uppercase' }}>Scoring Engine</span>
            <Sparkles size={18} color="var(--accent-cyan)" />
          </div>
          <div className="metric-number" style={{ fontSize: '1.8rem', color: 'var(--accent-cyan)' }}>0 - 100%</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: 4 }}>
            5-dimension deterministic formula
          </div>
        </div>
      </div>

      {/* Top Precomputed Matches */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
          <div>
            <h2 style={{ fontSize: '1.35rem', fontWeight: 700 }}>Top Autonomous Agent Matches</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
              Highest compatibility outcomes calculated from recorded dating sessions.
            </p>
          </div>
          <button className="btn btn-secondary" style={{ fontSize: '0.8rem', padding: '6px 14px' }} onClick={() => onNavigate('rankings')}>
            See All Rankings <ArrowRight size={14} />
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 20 }}>
          {demo.top_matches.slice(0, 4).map((session: any) => (
            <div key={session.id} className="glass-panel" style={{ padding: 20, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                  <span className="badge badge-gold">{session.overall_score}% Match</span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{session.total_turns} turns completed</span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <img 
                      src={session.person_a_avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80'} 
                      alt="" 
                      style={{ width: 44, height: 44, borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--accent-gold)' }} 
                    />
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{session.person_a_name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Agent A</div>
                    </div>
                  </div>

                  <span style={{ fontSize: '1.2rem', color: 'var(--accent-rose)' }}>&hearts;</span>

                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, textAlign: 'right' }}>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{session.person_b_name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Agent B</div>
                    </div>
                    <img 
                      src={session.person_b_avatar || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80'} 
                      alt="" 
                      style={{ width: 44, height: 44, borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--accent-rose)' }} 
                    />
                  </div>
                </div>

                <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: 16 }}>
                  {session.outcome_summary}
                </p>
              </div>

              <button 
                className="btn btn-secondary" 
                style={{ width: '100%', fontSize: '0.82rem' }}
                onClick={() => onNavigate('dating', undefined, session.id)}
              >
                Inspect Dating Transcript <ArrowRight size={14} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
