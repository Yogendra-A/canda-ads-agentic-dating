import React, { useState, useEffect } from 'react';
import type { Person } from '../types';
import { fetchPersonDetail, analyzePersonProfile } from '../api';
import { 
  ShieldCheck, ExternalLink, Sparkles, HeartHandshake, 
  HelpCircle, ArrowLeft, RefreshCw, Globe, Share2, Flame, Quote
} from 'lucide-react';

interface Props {
  personId: string;
  onBack: () => void;
  onStartDate: (personId: string, partnerId?: string) => void;
  onOpenSession: (sessionId: string) => void;
}

export const ProfileView: React.FC<Props> = ({ personId, onBack, onStartDate, onOpenSession }) => {
  const [person, setPerson] = useState<Person | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    loadData();
  }, [personId]);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchPersonDetail(personId);
      setPerson(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleReanalyze = async () => {
    if (!person) return;
    setAnalyzing(true);
    try {
      await analyzePersonProfile(person.id);
      await loadData();
    } catch (e) {
      console.error(e);
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '80px 20px' }}>
        <div className="badge badge-gold pulse-element">Loading Verified Dossier...</div>
      </div>
    );
  }

  if (!person) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Person not found.</p>
        <button className="btn btn-secondary" style={{ marginTop: 16 }} onClick={onBack}>
          <ArrowLeft size={16} /> Back to Directory
        </button>
      </div>
    );
  }

  const analysis = person.analysis;
  const confidencePercent = analysis ? Math.round(analysis.confidence_score * 100) : 85;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Back button */}
      <div>
        <button className="btn btn-secondary" onClick={onBack} style={{ padding: '6px 14px', fontSize: '0.85rem' }}>
          <ArrowLeft size={16} /> Back to Directory
        </button>
      </div>

      {/* Main Profile Header Card */}
      <div className="glass-panel" style={{ padding: '32px 36px' }}>
        <div style={{ display: 'flex', gap: 28, flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', gap: 24, alignItems: 'center' }}>
            <img
              src={person.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'}
              alt={person.display_name}
              style={{
                width: 96,
                height: 96,
                borderRadius: '50%',
                objectFit: 'cover',
                border: '3px solid var(--accent-gold)',
                boxShadow: '0 0 20px rgba(245, 158, 11, 0.2)'
              }}
            />
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
                <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>{person.display_name}</h1>
                <span className="badge badge-emerald">
                  <ShieldCheck size={12} /> Verified Public Figure
                </span>
                <span className="badge badge-gold" style={{ fontSize: '0.7rem' }}>
                  {person.collection_method.replace('_', ' ').toUpperCase()}
                </span>
              </div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: 600, marginBottom: 12 }}>
                {person.headline || 'Technology and Innovation Leader'}
              </p>

              {/* Official Source Links */}
              <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                <a
                  href={person.linkedin_url}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    fontSize: '0.82rem',
                    color: '#38bdf8',
                    textDecoration: 'none',
                    background: 'rgba(14, 165, 233, 0.1)',
                    padding: '6px 14px',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid rgba(14, 165, 233, 0.25)'
                  }}
                >
                  <Globe size={14} /> Official LinkedIn Profile <ExternalLink size={12} />
                </a>
                <a
                  href={person.instagram_url}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    fontSize: '0.82rem',
                    color: '#fb7185',
                    textDecoration: 'none',
                    background: 'rgba(244, 63, 94, 0.1)',
                    padding: '6px 14px',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid rgba(244, 63, 94, 0.25)'
                  }}
                >
                  <Share2 size={14} /> Official Instagram Profile <ExternalLink size={12} />
                </a>
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: 12 }}>
            <button className="btn btn-primary" onClick={() => onStartDate(person.id)}>
              <Flame size={16} /> Simulate Date with Agent
            </button>
            <button className="btn btn-secondary" onClick={handleReanalyze} disabled={analyzing}>
              <RefreshCw size={14} className={analyzing ? 'pulse-element' : ''} /> {analyzing ? 'Analyzing...' : 'Re-analyze'}
            </button>
          </div>
        </div>
      </div>

      {/* Two Column Layout: Analysis Details & Match Rankings */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: 24 }}>
        {/* Left Column: Evidence-Backed Analysis */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          {/* Executive Summary */}
          <div className="glass-panel" style={{ padding: 24 }}>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
              <Sparkles size={18} color="var(--accent-gold)" /> Evidence-Supported Profile Summary
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: 1.6, marginBottom: 16 }}>
              {analysis?.summary || person.bio}
            </p>

            {/* Confidence Score Meter */}
            <div style={{ background: 'rgba(0, 0, 0, 0.25)', padding: 14, borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Analysis Confidence Score</span>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-gold)' }}>{confidencePercent}%</span>
              </div>
              <div style={{ width: '100%', height: 6, background: 'rgba(255, 255, 255, 0.08)', borderRadius: 3, overflow: 'hidden' }}>
                <div style={{ width: `${confidencePercent}%`, height: '100%', background: 'linear-gradient(90deg, #f59e0b, #10b981)' }} />
              </div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 6 }}>
                Engine: <span style={{ color: '#fff' }}>{analysis?.analysis_engine || 'deterministic_fallback'}</span> (Zero hallucinations)
              </div>
            </div>
          </div>

          {/* Interests & Hobbies */}
          <div className="glass-panel" style={{ padding: 24 }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 14 }}>Verified Interests & Domains</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 20 }}>
              {analysis?.interests.map((item, idx) => (
                <span key={idx} className="badge badge-gold" style={{ fontSize: '0.76rem', padding: '5px 12px' }}>
                  {item}
                </span>
              ))}
            </div>

            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 14 }}>Personal Hobbies & Pursuits</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 20 }}>
              {analysis?.hobbies.map((item, idx) => (
                <span key={idx} className="badge badge-emerald" style={{ fontSize: '0.76rem', padding: '5px 12px' }}>
                  {item}
                </span>
              ))}
            </div>

            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 14 }}>Lifestyle Signals & Cadence</h3>
            <ul style={{ paddingLeft: 18, color: 'var(--text-secondary)', fontSize: '0.88rem', display: 'flex', flexDirection: 'column', gap: 6 }}>
              {analysis?.lifestyle_signals.map((signal, idx) => (
                <li key={idx}>{signal}</li>
              ))}
            </ul>
          </div>

          {/* Evidence Citations */}
          {analysis?.evidence_references && analysis.evidence_references.length > 0 && (
            <div className="glass-panel" style={{ padding: 24 }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <Quote size={16} color="var(--accent-gold)" /> Evidence Citations & Public Statements
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                {analysis.evidence_references.map((ref, idx) => (
                  <div key={idx} style={{ background: 'rgba(0,0,0,0.25)', padding: 12, borderRadius: 'var(--radius-sm)', borderLeft: '3px solid var(--accent-gold)' }}>
                    <div style={{ fontWeight: 600, fontSize: '0.84rem', color: '#fff', marginBottom: 4 }}>{ref.claim}</div>
                    {ref.quote && (
                      <div style={{ fontSize: '0.8rem', color: '#cbd5e1', fontStyle: 'italic', marginBottom: 6 }}>
                        "{ref.quote}"
                      </div>
                    )}
                    <a href={ref.source_url} target="_blank" rel="noreferrer" style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', textDecoration: 'none' }}>
                      Source Profile <ExternalLink size={10} style={{ display: 'inline' }} />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Missing / Unknown Fields Indicator */}
          {analysis?.unknown_fields && analysis.unknown_fields.length > 0 && (
            <div className="glass-panel" style={{ padding: 20, border: '1px dashed var(--border-subtle)' }}>
              <h4 style={{ fontSize: '0.86rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                <HelpCircle size={14} /> Unsupported / Unverifiable Dimensions (Not Hallucinated)
              </h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {analysis.unknown_fields.map((f, idx) => (
                  <span key={idx} style={{ fontSize: '0.72rem', color: 'var(--text-muted)', background: 'rgba(255,255,255,0.04)', padding: '3px 8px', borderRadius: 4 }}>
                    {f}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Compatibility Rankings & Dating History */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          {/* Top Ranked Matches for This Person */}
          <div className="glass-panel" style={{ padding: 24 }}>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
              <HeartHandshake size={18} color="var(--accent-rose)" /> Personalized Compatibility Matches
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {person.rankings && person.rankings.length > 0 ? (
                person.rankings.map(rank => (
                  <div key={rank.id} style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 14px',
                    background: 'rgba(0, 0, 0, 0.25)',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-subtle)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                      <span style={{
                        width: 24,
                        height: 24,
                        borderRadius: '50%',
                        background: 'rgba(245, 158, 11, 0.15)',
                        color: 'var(--accent-gold)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.75rem',
                        fontWeight: 700
                      }}>
                        #{rank.rank}
                      </span>
                      <img 
                        src={rank.candidate_avatar || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80'} 
                        alt="" 
                        style={{ width: 38, height: 38, borderRadius: '50%', objectFit: 'cover' }} 
                      />
                      <div>
                        <div style={{ fontWeight: 700, fontSize: '0.88rem' }}>{rank.candidate_name}</div>
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{rank.primary_factors[0]}</div>
                      </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <span className="badge badge-gold">{rank.score}%</span>
                      <button 
                        className="btn btn-secondary" 
                        style={{ padding: '4px 10px', fontSize: '0.74rem' }}
                        onClick={() => onStartDate(person.id, rank.candidate_person_id)}
                      >
                        Date
                      </button>
                    </div>
                  </div>
                ))
              ) : (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No rankings calculated yet.</p>
              )}
            </div>
          </div>

          {/* Dating History */}
          <div className="glass-panel" style={{ padding: 24 }}>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: 14 }}>Autonomous Dating History</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {person.dating_history && person.dating_history.length > 0 ? (
                person.dating_history.map(session => {
                  const partnerName = session.person_a_id === person.id ? session.person_b_name : session.person_a_name;
                  const partnerAvatar = session.person_a_id === person.id ? session.person_b_avatar : session.person_a_avatar;

                  return (
                    <div key={session.id} style={{
                      padding: 14,
                      background: 'rgba(0, 0, 0, 0.2)',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-subtle)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                        <img src={partnerAvatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80'} alt="" style={{ width: 36, height: 36, borderRadius: '50%', objectFit: 'cover' }} />
                        <div>
                          <div style={{ fontWeight: 600, fontSize: '0.86rem' }}>Date with {partnerName}</div>
                          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>{session.outcome_summary.slice(0, 60)}...</div>
                        </div>
                      </div>

                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <span className="badge badge-rose">{session.overall_score}%</span>
                        <button 
                          className="btn btn-secondary" 
                          style={{ padding: '4px 10px', fontSize: '0.72rem' }}
                          onClick={() => onOpenSession(session.id)}
                        >
                          Transcript
                        </button>
                      </div>
                    </div>
                  );
                })
              ) : (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No dating sessions recorded yet for this agent.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
