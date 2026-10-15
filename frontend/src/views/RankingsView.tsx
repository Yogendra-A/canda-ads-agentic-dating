import React, { useState, useEffect } from 'react';
import type { Person, RankingItem } from '../types';
import { fetchRankings } from '../api';
import { HeartHandshake, ArrowRight, BookOpen } from 'lucide-react';

interface Props {
  people: Person[];
  onViewProfile: (personId: string) => void;
  onOpenDatingSession: (sessionId: string) => void;
}

export const RankingsView: React.FC<Props> = ({ people, onViewProfile, onOpenDatingSession }) => {
  const [selectedPersonId, setSelectedPersonId] = useState<string>(people[0]?.id || '');
  const [rankings, setRankings] = useState<RankingItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedPersonId) {
      loadRankings(selectedPersonId);
    }
  }, [selectedPersonId]);

  const loadRankings = async (personId: string) => {
    setLoading(true);
    try {
      const data = await fetchRankings(personId);
      setRankings(data.rankings);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const selectedPerson = people.find(p => p.id === selectedPersonId);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Header and Person Switcher */}
      <div className="glass-panel" style={{ padding: 26 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16, marginBottom: 18 }}>
          <div>
            <h1 style={{ fontSize: '1.6rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: 10 }}>
              <HeartHandshake size={24} color="var(--accent-gold)" /> Personalized Compatibility Matrix
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
              Select any verified person to inspect bidirectional compatibility rankings computed by autonomous agents.
            </p>
          </div>

          <div style={{ minWidth: 280 }}>
            <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: 6, fontWeight: 600 }}>
              SELECT PERSON TO INSPECT RANKINGS:
            </label>
            <select
              value={selectedPersonId}
              onChange={e => setSelectedPersonId(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 14px',
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-active)',
                borderRadius: 'var(--radius-md)',
                color: '#fff',
                fontSize: '0.92rem',
                fontWeight: 700,
                outline: 'none'
              }}
            >
              {people.map(p => (
                <option key={p.id} value={p.id}>
                  {p.display_name} ({p.headline ? p.headline.slice(0, 35) : 'Public Profile'}...)
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Selected Person Snapshot */}
        {selectedPerson && (
          <div style={{
            background: 'rgba(0,0,0,0.25)',
            padding: 16,
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 12
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <img
                src={selectedPerson.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80'}
                alt=""
                style={{ width: 48, height: 48, borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--accent-gold)' }}
              />
              <div>
                <div style={{ fontWeight: 700, fontSize: '1rem', color: '#fff' }}>{selectedPerson.display_name}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{selectedPerson.headline}</div>
              </div>
            </div>

            <button className="btn btn-secondary" style={{ fontSize: '0.78rem' }} onClick={() => onViewProfile(selectedPerson.id)}>
              View Dossier & Evidence
            </button>
          </div>
        )}
      </div>

      {/* Formula Explanation Accordion / Callout */}
      <div style={{
        background: 'rgba(23, 27, 36, 0.5)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: '16px 20px',
        display: 'flex',
        alignItems: 'center',
        gap: 14
      }}>
        <BookOpen size={20} color="var(--accent-gold)" style={{ flexShrink: 0 }} />
        <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
          <strong style={{ color: '#fff' }}>Deterministic Formula:</strong> Compatibility = (Shared Interests &times; 30%) + (Lifestyle Harmony &times; 25%) + (Communication Resonance &times; 20%) + (Mutual Curiosity &times; 15%) + (Data Confidence &times; 10%). 
          All scores are normalized from 0 to 100%. Missing data reduces confidence rather than hallucinating attributes.
        </div>
      </div>

      {/* Rankings List */}
      <div className="glass-panel" style={{ padding: 26 }}>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: 18 }}>
          Ranked Candidates for {selectedPerson?.display_name} ({rankings.length} matches)
        </h2>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px 20px' }}>
            <div className="badge badge-gold pulse-element">Computing Match Matrix...</div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {rankings.map(item => (
              <div
                key={item.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '16px 20px',
                  background: 'rgba(0, 0, 0, 0.25)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-subtle)',
                  transition: 'all 0.2s ease',
                  flexWrap: 'wrap',
                  gap: 14
                }}
              >
                {/* Left: Rank, Avatar, Name, Headline */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                  <div style={{
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    background: item.rank === 1 ? 'linear-gradient(135deg, #f59e0b, #d97706)' : 'rgba(255, 255, 255, 0.08)',
                    color: item.rank === 1 ? '#000' : '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 800,
                    fontSize: '0.85rem'
                  }}>
                    #{item.rank}
                  </div>

                  <img
                    src={item.candidate_avatar || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=80'}
                    alt=""
                    style={{ width: 48, height: 48, borderRadius: '50%', objectFit: 'cover' }}
                  />

                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.98rem', color: '#fff', marginBottom: 2 }}>
                      {item.candidate_name}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', maxWidth: 400, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {item.candidate_headline || 'Public Creator'}
                    </div>
                    {/* Primary compatibility factors */}
                    <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 4 }}>
                      {item.primary_factors.map((factor, fIdx) => (
                        <span key={fIdx} style={{ fontSize: '0.7rem', color: 'var(--accent-gold)', background: 'rgba(245, 158, 11, 0.1)', padding: '2px 8px', borderRadius: 4 }}>
                          {factor}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Right: Score and Action Buttons */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--accent-gold)' }}>
                      {item.score}%
                    </div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Mutual Match</div>
                  </div>

                  <div style={{ display: 'flex', gap: 8 }}>
                    <button
                      className="btn btn-secondary"
                      style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                      onClick={() => onViewProfile(item.candidate_person_id)}
                    >
                      Dossier
                    </button>
                    {item.dating_session_id && (
                      <button
                        className="btn btn-primary"
                        style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                        onClick={() => onOpenDatingSession(item.dating_session_id!)}
                      >
                        Transcript <ArrowRight size={12} />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
