import React, { useState } from 'react';
import type { Person } from '../types';
import { Search, ExternalLink, ShieldCheck, Sparkles, HeartHandshake, Eye, Globe, Share2, Filter } from 'lucide-react';

interface Props {
  people: Person[];
  onSelectPerson: (personId: string) => void;
  onStartDate: (personId: string) => void;
}

export const DirectoryView: React.FC<Props> = ({ people, onSelectPerson, onStartDate }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [methodFilter, setMethodFilter] = useState('all');

  const filtered = people.filter(p => {
    const matchesSearch = 
      p.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (p.headline && p.headline.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (p.bio && p.bio.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (p.analysis?.interests && p.analysis.interests.some(i => i.toLowerCase().includes(searchTerm.toLowerCase())));

    const matchesMethod = 
      methodFilter === 'all' || p.collection_method === methodFilter;

    return matchesSearch && matchesMethod;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Top Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>Verified People Directory</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Showing {filtered.length} of {people.length} real people with public profiles and active AI agents.
          </p>
        </div>

        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          {/* Search Input */}
          <div style={{ position: 'relative', minWidth: 260 }}>
            <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: 12, top: 12 }} />
            <input
              type="text"
              placeholder="Search by name, hobby, topic..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '9px 12px 9px 36px',
                background: 'rgba(23, 27, 36, 0.8)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                color: '#fff',
                fontSize: '0.88rem',
                outline: 'none'
              }}
            />
          </div>

          {/* Filter Dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <Filter size={16} color="var(--text-muted)" />
            <select
              value={methodFilter}
              onChange={e => setMethodFilter(e.target.value)}
              style={{
                padding: '9px 14px',
                background: 'rgba(23, 27, 36, 0.8)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                color: '#fff',
                fontSize: '0.88rem',
                outline: 'none'
              }}
            >
              <option value="all">All Provenance</option>
              <option value="verified_seed">Verified Seed Data</option>
              <option value="apify_scrape">Apify Scraped</option>
              <option value="manual_import">Manual Import</option>
            </select>
          </div>
        </div>
      </div>

      {/* Grid of People */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 20 }}>
        {filtered.map(person => {
          const confidencePercent = person.analysis ? Math.round(person.analysis.confidence_score * 100) : 85;

          return (
            <div key={person.id} className="glass-panel" style={{ padding: 22, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                {/* Header: Avatar, Name, Verification badge */}
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: 14, marginBottom: 14 }}>
                  <img
                    src={person.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80'}
                    alt={person.display_name}
                    style={{
                      width: 56,
                      height: 56,
                      borderRadius: '50%',
                      objectFit: 'cover',
                      border: '2px solid var(--border-highlight)',
                      flexShrink: 0
                    }}
                  />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
                      <h3 style={{ fontSize: '1.05rem', fontWeight: 700, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {person.display_name}
                      </h3>
                      {person.is_verified && (
                        <span title="Verified Real Public Figure">
                          <ShieldCheck size={16} color="#34d399" />
                        </span>
                      )}
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.3, maxHeight: 34, overflow: 'hidden' }}>
                      {person.headline || 'Public Creator & Thinker'}
                    </div>
                  </div>
                </div>

                {/* Source Links */}
                <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
                  <a
                    href={person.linkedin_url}
                    target="_blank"
                    rel="noreferrer"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 4,
                      fontSize: '0.75rem',
                      color: '#38bdf8',
                      textDecoration: 'none',
                      background: 'rgba(14, 165, 233, 0.1)',
                      padding: '4px 10px',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid rgba(14, 165, 233, 0.2)'
                    }}
                  >
                    <Globe size={12} /> LinkedIn <ExternalLink size={10} />
                  </a>
                  <a
                    href={person.instagram_url}
                    target="_blank"
                    rel="noreferrer"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 4,
                      fontSize: '0.75rem',
                      color: '#fb7185',
                      textDecoration: 'none',
                      background: 'rgba(244, 63, 94, 0.1)',
                      padding: '4px 10px',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid rgba(244, 63, 94, 0.2)'
                    }}
                  >
                    <Share2 size={12} /> Instagram <ExternalLink size={10} />
                  </a>
                </div>

                {/* Profile Summary */}
                <p style={{
                  fontSize: '0.84rem',
                  color: 'var(--text-secondary)',
                  lineHeight: 1.5,
                  marginBottom: 14,
                  display: '-webkit-box',
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden'
                }}>
                  {person.analysis?.summary || person.bio || 'Public figure with active agent modeling enabled.'}
                </p>

                {/* Verified Interests Tags */}
                {person.analysis?.interests && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 16 }}>
                    {person.analysis.interests.slice(0, 3).map((interest, idx) => (
                      <span key={idx} className="badge badge-gold" style={{ fontSize: '0.68rem' }}>
                        {interest}
                      </span>
                    ))}
                    {person.analysis.hobbies && person.analysis.hobbies[0] && (
                      <span className="badge badge-emerald" style={{ fontSize: '0.68rem' }}>
                        {person.analysis.hobbies[0]}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Card Footer */}
              <div style={{ paddingTop: 14, borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <Sparkles size={13} color="var(--accent-gold)" />
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Agent Confidence: <strong style={{ color: '#fff' }}>{confidencePercent}%</strong>
                  </span>
                </div>

                <div style={{ display: 'flex', gap: 8 }}>
                  <button
                    className="btn btn-secondary"
                    style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                    onClick={() => onSelectPerson(person.id)}
                    title="View Evidence & Full Analysis"
                  >
                    <Eye size={13} /> Dossier
                  </button>
                  <button
                    className="btn btn-primary"
                    style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                    onClick={() => onStartDate(person.id)}
                    title="Simulate Date with this Agent"
                  >
                    <HeartHandshake size={13} /> Date
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
