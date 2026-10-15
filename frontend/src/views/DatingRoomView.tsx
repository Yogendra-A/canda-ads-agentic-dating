import React, { useState, useEffect } from 'react';
import type { Person, DatingSession } from '../types';
import { runDatingSession, fetchDatingSessions, fetchDatingSessionDetail } from '../api';
import { 
  Flame, HeartHandshake, ShieldAlert, 
  MessageSquare, Brain, CheckCircle2
} from 'lucide-react';

interface Props {
  people: Person[];
  initialPersonAId?: string;
  initialPersonBId?: string;
  initialSessionId?: string;
  onViewProfile: (personId: string) => void;
}

export const DatingRoomView: React.FC<Props> = ({ 
  people, 
  initialPersonAId, 
  initialPersonBId, 
  initialSessionId,
  onViewProfile
}) => {
  const [selectedPersonA, setSelectedPersonA] = useState<string>(initialPersonAId || people[0]?.id || '');
  const [selectedPersonB, setSelectedPersonB] = useState<string>(initialPersonBId || people[1]?.id || '');
  const [turnsCount, setTurnsCount] = useState<number>(6);
  const [currentSession, setCurrentSession] = useState<DatingSession | null>(null);
  const [recentSessions, setRecentSessions] = useState<DatingSession[]>([]);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    loadRecentSessions();
  }, []);

  useEffect(() => {
    if (initialSessionId) {
      loadSpecificSession(initialSessionId);
    } else if (recentSessions.length > 0 && !currentSession) {
      loadSpecificSession(recentSessions[0].id);
    }
  }, [initialSessionId, recentSessions]);

  const loadRecentSessions = async () => {
    try {
      const sessions = await fetchDatingSessions();
      setRecentSessions(sessions);
    } catch (e) {
      console.error(e);
    }
  };

  const loadSpecificSession = async (sessionId: string) => {
    try {
      const detail = await fetchDatingSessionDetail(sessionId);
      setCurrentSession(detail);
      setSelectedPersonA(detail.person_a_id);
      setSelectedPersonB(detail.person_b_id);
    } catch (e) {
      console.error(e);
    }
  };

  const handleStartSimulation = async () => {
    if (selectedPersonA === selectedPersonB) {
      setErrorMsg("Please select two different agents to simulate a date.");
      return;
    }
    setErrorMsg(null);
    setIsRunning(true);
    try {
      const session = await runDatingSession(selectedPersonA, selectedPersonB, turnsCount);
      setCurrentSession(session);
      await loadRecentSessions();
    } catch (e: any) {
      setErrorMsg(e.message || "Simulation failed.");
    } finally {
      setIsRunning(false);
    }
  };

  const personA = people.find(p => p.id === selectedPersonA);
  const personB = people.find(p => p.id === selectedPersonB);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* 1. Mandatory Disclaimer Banner */}
      <div style={{
        background: 'rgba(244, 63, 94, 0.08)',
        border: '1px solid rgba(244, 63, 94, 0.25)',
        borderRadius: 'var(--radius-md)',
        padding: '14px 20px',
        display: 'flex',
        alignItems: 'center',
        gap: 12
      }}>
        <ShieldAlert size={20} color="#fb7185" style={{ flexShrink: 0 }} />
        <div style={{ fontSize: '0.84rem', color: '#fda4af', lineHeight: 1.5 }}>
          <strong>SIMULATED AI AGENT INTERACTION:</strong> Every conversation in this room is generated autonomously by AI agents modeling public professional profile data. 
          Conversations represent simulated heuristic compatibility and do <em>not</em> represent real messages sent or received by real individuals.
        </div>
      </div>

      {/* 2. Top Controls & Precomputed Sessions Quick Picker */}
      <div className="glass-panel" style={{ padding: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16, marginBottom: 20 }}>
          <div>
            <h1 style={{ fontSize: '1.6rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: 10 }}>
              <HeartHandshake size={24} color="var(--accent-rose)" /> Autonomous Agent Dating Room
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
              Select any two agents to run a live observable multi-turn date, or inspect precomputed sessions below.
            </p>
          </div>

          {/* Turns length selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Dialogue Depth:</span>
            <select
              value={turnsCount}
              onChange={e => setTurnsCount(Number(e.target.value))}
              style={{
                padding: '6px 12px',
                background: 'rgba(0,0,0,0.4)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                color: '#fff',
                fontSize: '0.82rem'
              }}
            >
              <option value={4}>4 Turns (Quick Spark)</option>
              <option value={6}>6 Turns (Standard Date)</option>
              <option value={8}>8 Turns (Deep Dialogue)</option>
            </select>
          </div>
        </div>

        {/* Agent Selectors Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: 20, alignItems: 'center', marginBottom: 20 }}>
          {/* Agent A Selector */}
          <div style={{ background: 'rgba(0,0,0,0.3)', padding: 16, borderRadius: 'var(--radius-md)', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--accent-gold)', fontWeight: 700 }}>AGENT A (INITIATOR)</span>
              {personA && (
                <button 
                  onClick={() => onViewProfile(personA.id)} 
                  style={{ background: 'none', border: 'none', color: 'var(--text-muted)', fontSize: '0.72rem', cursor: 'pointer', textDecoration: 'underline' }}
                >
                  View Dossier
                </button>
              )}
            </div>
            <select
              value={selectedPersonA}
              onChange={e => setSelectedPersonA(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                color: '#fff',
                fontSize: '0.9rem',
                fontWeight: 600,
                outline: 'none'
              }}
            >
              {people.map(p => (
                <option key={p.id} value={p.id}>{p.display_name} — {p.headline ? p.headline.slice(0, 40) : ''}...</option>
              ))}
            </select>
          </div>

          {/* VS Badge */}
          <div style={{ textAlign: 'center' }}>
            <div style={{
              width: 44,
              height: 44,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(244, 63, 94, 0.2))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid var(--border-highlight)',
              color: 'var(--accent-rose)',
              fontWeight: 800,
              fontSize: '1rem'
            }}>
              &hearts;
            </div>
          </div>

          {/* Agent B Selector */}
          <div style={{ background: 'rgba(0,0,0,0.3)', padding: 16, borderRadius: 'var(--radius-md)', border: '1px solid rgba(244, 63, 94, 0.3)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--accent-rose)', fontWeight: 700 }}>AGENT B (RESPONDER)</span>
              {personB && (
                <button 
                  onClick={() => onViewProfile(personB.id)} 
                  style={{ background: 'none', border: 'none', color: 'var(--text-muted)', fontSize: '0.72rem', cursor: 'pointer', textDecoration: 'underline' }}
                >
                  View Dossier
                </button>
              )}
            </div>
            <select
              value={selectedPersonB}
              onChange={e => setSelectedPersonB(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                color: '#fff',
                fontSize: '0.9rem',
                fontWeight: 600,
                outline: 'none'
              }}
            >
              {people.map(p => (
                <option key={p.id} value={p.id}>{p.display_name} — {p.headline ? p.headline.slice(0, 40) : ''}...</option>
              ))}
            </select>
          </div>
        </div>

        {errorMsg && (
          <div style={{ color: '#f87171', fontSize: '0.85rem', marginBottom: 14 }}>
            {errorMsg}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <button
            className="btn btn-primary"
            style={{ padding: '12px 32px', fontSize: '0.95rem' }}
            onClick={handleStartSimulation}
            disabled={isRunning}
          >
            <Flame size={18} /> {isRunning ? 'Agents Are Conversing...' : 'Start Autonomous Agent Date'}
          </button>
        </div>

        {/* Precomputed Sessions Quick Bar */}
        {recentSessions.length > 0 && (
          <div style={{ marginTop: 24, paddingTop: 18, borderTop: '1px solid var(--border-subtle)' }}>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', display: 'block', marginBottom: 10 }}>
              Precomputed Completed Demonstrations ({recentSessions.length} ready):
            </span>
            <div style={{ display: 'flex', gap: 10, overflowX: 'auto', paddingBottom: 6 }}>
              {recentSessions.map(session => (
                <button
                  key={session.id}
                  onClick={() => loadSpecificSession(session.id)}
                  style={{
                    background: currentSession?.id === session.id ? 'rgba(245, 158, 11, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                    border: currentSession?.id === session.id ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-sm)',
                    padding: '6px 12px',
                    color: currentSession?.id === session.id ? '#fff' : 'var(--text-secondary)',
                    fontSize: '0.75rem',
                    cursor: 'pointer',
                    whiteSpace: 'nowrap',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6
                  }}
                >
                  <span>{session.person_a_name?.split(' ')[0]} & {session.person_b_name?.split(' ')[0]}</span>
                  <span className="badge badge-gold" style={{ fontSize: '0.65rem', padding: '1px 6px' }}>{session.overall_score}%</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 3. Session Output: Score Breakdown & Turn Dialogue */}
      {currentSession && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          {/* Compatibility Verdict & Score Breakdown Card */}
          <div className="glass-panel" style={{ padding: 28 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16, marginBottom: 20 }}>
              <div>
                <span className="badge badge-emerald" style={{ marginBottom: 6 }}>
                  <CheckCircle2 size={12} /> Dating Session Concluded
                </span>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>
                  Compatibility Outcome: <span style={{ color: 'var(--accent-gold)' }}>{currentSession.overall_score}%</span>
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', marginTop: 4 }}>
                  {currentSession.outcome_summary}
                </p>
              </div>

              {/* Score breakdown metrics */}
              <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 14px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Shared Interests</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--accent-gold)' }}>{currentSession.breakdown.shared_interests}%</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 14px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Lifestyle Harmony</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#34d399' }}>{currentSession.breakdown.lifestyle_harmony}%</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 14px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Communication</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#38bdf8' }}>{currentSession.breakdown.communication_resonance}%</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.3)', padding: '8px 14px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Mutual Curiosity</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fb7185' }}>{currentSession.breakdown.mutual_curiosity}%</div>
                </div>
              </div>
            </div>
          </div>

          {/* Observable Multi-Turn Dialogue Stream */}
          <div className="glass-panel" style={{ padding: 28 }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 20, display: 'flex', alignItems: 'center', gap: 8 }}>
              <MessageSquare size={18} color="var(--accent-gold)" /> Observable Turn-by-Turn Agent Transcript ({currentSession.turns.length} turns)
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
              {currentSession.turns.map(turn => {
                const isSpeakerA = turn.speaker_id === currentSession.person_a_id;
                const speakerName = turn.speaker_name || (isSpeakerA ? currentSession.person_a_name : currentSession.person_b_name);
                const speakerAvatar = isSpeakerA ? currentSession.person_a_avatar : currentSession.person_b_avatar;

                return (
                  <div
                    key={turn.id}
                    className={`speech-bubble ${isSpeakerA ? 'bubble-left' : 'bubble-right'}`}
                  >
                    {/* Speaker Header */}
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <img
                          src={speakerAvatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=80&q=80'}
                          alt=""
                          style={{ width: 28, height: 28, borderRadius: '50%', objectFit: 'cover' }}
                        />
                        <span style={{ fontWeight: 700, fontSize: '0.88rem', color: isSpeakerA ? 'var(--accent-gold)' : 'var(--accent-rose)' }}>
                          {speakerName}
                        </span>
                        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                          Turn #{turn.turn_index}
                        </span>
                      </div>
                      <span className="badge badge-gold" style={{ fontSize: '0.66rem' }}>
                        {turn.turn_sentiment}
                      </span>
                    </div>

                    {/* Spoken Message */}
                    <div style={{ color: '#f1f5f9', fontSize: '0.92rem', lineHeight: 1.55 }}>
                      "{turn.message}"
                    </div>

                    {/* Internal Cognitive Reasoning (Agent's internal reflection) */}
                    <div className="reasoning-box">
                      <div style={{ display: 'flex', alignItems: 'center', gap: 5, marginBottom: 2, fontWeight: 600, color: 'var(--accent-gold)' }}>
                        <Brain size={12} /> Agent Internal Reasoning:
                      </div>
                      {turn.internal_reasoning}
                    </div>

                    {/* Detected Compatibility Signals */}
                    {turn.compatibility_signals && turn.compatibility_signals.length > 0 && (
                      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 8 }}>
                        {turn.compatibility_signals.map((signal, sIdx) => (
                          <span key={sIdx} style={{ fontSize: '0.68rem', color: '#94a3b8', background: 'rgba(255,255,255,0.06)', padding: '2px 8px', borderRadius: 4 }}>
                            &bull; {signal}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
