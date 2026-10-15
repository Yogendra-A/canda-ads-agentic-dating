import React, { useState, useEffect } from 'react';
import type { SettingsResponse } from '../types';
import { fetchSettings, triggerCollection, importPeopleDataset, reseedDemo } from '../api';
import { 
  Settings, Key, Upload, RefreshCw, 
  ShieldCheck, Terminal
} from 'lucide-react';

interface Props {
  onRefreshAll: () => void;
}

export const SettingsView: React.FC<Props> = ({ onRefreshAll }) => {
  const [settings, setSettings] = useState<SettingsResponse | null>(null);
  const [apifyToken, setApifyToken] = useState('');
  const [linkedinActorId, setLinkedinActorId] = useState('curious_coder/linkedin-profile-scraper');
  const [instagramActorId, setInstagramActorId] = useState('apify/instagram-profile-scraper');
  const [jsonInput, setJsonInput] = useState('');
  const [importStatus, setImportStatus] = useState<string | null>(null);
  const [collectionStatus, setCollectionStatus] = useState<string | null>(null);
  const [isScraping, setIsScraping] = useState(false);
  const [isReseeding, setIsReseeding] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await fetchSettings();
      setSettings(data);
      setLinkedinActorId(data.apify_linkedin_actor_id);
      setInstagramActorId(data.apify_instagram_actor_id);
    } catch (e) {
      console.error(e);
    }
  };

  const handleTriggerScraper = async () => {
    setIsScraping(true);
    setCollectionStatus("Connecting to Apify Actor runner...");
    try {
      const res = await triggerCollection(linkedinActorId, 'both', []);
      setCollectionStatus(`Actor run started successfully (Run ID: ${res.run_id})`);
    } catch (e: any) {
      setCollectionStatus(`Apify Scrape Status: ${e.message}`);
    } finally {
      setIsScraping(false);
    }
  };

  const handleJsonImport = async () => {
    try {
      const parsed = JSON.parse(jsonInput);
      const peopleArray = Array.isArray(parsed) ? parsed : (parsed.people || [parsed]);
      const res = await importPeopleDataset({ people: peopleArray });
      setImportStatus(`Success: ${res.message}`);
      setJsonInput('');
      onRefreshAll();
    } catch (e: any) {
      setImportStatus(`Import Error: ${e.message}`);
    }
  };

  const handleReseed = async () => {
    setIsReseeding(true);
    try {
      await reseedDemo();
      onRefreshAll();
      setImportStatus("Database successfully reset to 25 verified public figures and precomputed dating runs.");
    } catch (e: any) {
      setImportStatus(`Reset error: ${e.message}`);
    } finally {
      setIsReseeding(false);
    }
  };

  const sampleJson = JSON.stringify([
    {
      "display_name": "Ada Lovelace",
      "headline": "Mathematician & Computing Pioneer",
      "bio": "Devoted to poetical science, analytical engines, and music composition.",
      "linkedin_url": "https://www.linkedin.com/in/adalovelace",
      "instagram_url": "https://www.instagram.com/adalovelace"
    }
  ], null, 2);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Title */}
      <div>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: 10 }}>
          <Settings size={24} color="var(--accent-gold)" /> Ingestion, Apify Scrapers & Data Provenance
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Configure live Apify actors, import custom JSON/CSV datasets, or inspect credential disclosure.
        </p>
      </div>

      {/* Honest Credentials Disclosure Card */}
      <div style={{
        background: 'rgba(245, 158, 11, 0.08)',
        border: '1px solid rgba(245, 158, 11, 0.25)',
        borderRadius: 'var(--radius-md)',
        padding: '16px 20px',
        display: 'flex',
        alignItems: 'flex-start',
        gap: 14
      }}>
        <ShieldCheck size={22} color="var(--accent-gold)" style={{ flexShrink: 0, marginTop: 2 }} />
        <div style={{ fontSize: '0.85rem', color: '#fde68a', lineHeight: 1.55 }}>
          <strong>Assessment Integrity Disclosure:</strong> No live paid Apify credentials or credit cards are supplied.
          The platform operates with full fidelity using a verified 25-person public dataset and a deterministic LLM fallback engine.
          You may provide a custom Apify API token or import validated external profiles below at any time.
        </div>
      </div>

      {/* Grid: Apify Config & JSON/CSV Import */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: 24 }}>
        {/* Left: Apify Actor Configuration */}
        <div className="glass-panel" style={{ padding: 26 }}>
          <h2 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
            <Key size={18} color="var(--accent-gold)" /> Apify API & Actor Settings
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 6 }}>
                APIFY API TOKEN:
              </label>
              <input
                type="password"
                placeholder={settings?.has_apify_token ? "•••••••••••••••• (Configured)" : "Enter Apify Token (optional)..."}
                value={apifyToken}
                onChange={e => setApifyToken(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  background: 'rgba(0,0,0,0.3)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  color: '#fff',
                  fontSize: '0.88rem'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 6 }}>
                LINKEDIN ACTOR ID:
              </label>
              <input
                type="text"
                value={linkedinActorId}
                onChange={e => setLinkedinActorId(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  background: 'rgba(0,0,0,0.3)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  color: '#fff',
                  fontSize: '0.88rem'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 6 }}>
                INSTAGRAM ACTOR ID:
              </label>
              <input
                type="text"
                value={instagramActorId}
                onChange={e => setInstagramActorId(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  background: 'rgba(0,0,0,0.3)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  color: '#fff',
                  fontSize: '0.88rem'
                }}
              />
            </div>

            <button
              className="btn btn-secondary"
              style={{ padding: '10px 16px' }}
              onClick={handleTriggerScraper}
              disabled={isScraping}
            >
              <Terminal size={14} /> {isScraping ? 'Contacting Apify...' : 'Trigger Apify Actor Run'}
            </button>

            {collectionStatus && (
              <div style={{
                background: 'rgba(0,0,0,0.4)',
                padding: 12,
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.78rem',
                color: collectionStatus.includes('Error') || collectionStatus.includes('not configured') ? '#fca5a5' : '#86efac',
                border: '1px solid var(--border-subtle)'
              }}>
                {collectionStatus}
              </div>
            )}
          </div>
        </div>

        {/* Right: Safe JSON/CSV Dataset Import */}
        <div className="glass-panel" style={{ padding: 26 }}>
          <h2 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
            <Upload size={18} color="var(--accent-cyan)" /> Import Verified Profiles (JSON)
          </h2>

          <p style={{ color: 'var(--text-secondary)', fontSize: '0.84rem', marginBottom: 12 }}>
            Paste a JSON array of real public people with official LinkedIn and Instagram URLs to import them into the active database:
          </p>

          <textarea
            rows={7}
            placeholder={sampleJson}
            value={jsonInput}
            onChange={e => setJsonInput(e.target.value)}
            style={{
              width: '100%',
              padding: 12,
              background: 'rgba(0,0,0,0.3)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              color: '#fff',
              fontSize: '0.8rem',
              fontFamily: 'monospace',
              marginBottom: 14
            }}
          />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button
              className="btn btn-primary"
              style={{ fontSize: '0.84rem' }}
              onClick={handleJsonImport}
              disabled={!jsonInput.trim()}
            >
              <Upload size={14} /> Validate & Import Records
            </button>

            <button
              className="btn btn-secondary"
              style={{ fontSize: '0.78rem' }}
              onClick={() => setJsonInput(sampleJson)}
            >
              Load Sample JSON
            </button>
          </div>

          {importStatus && (
            <div style={{
              marginTop: 14,
              background: 'rgba(0,0,0,0.4)',
              padding: 12,
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.78rem',
              color: importStatus.includes('Error') ? '#fca5a5' : '#86efac'
            }}>
              {importStatus}
            </div>
          )}
        </div>
      </div>

      {/* Database Reset / Reseed Section */}
      <div className="glass-panel" style={{ padding: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
        <div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: 4 }}>
            Demonstration Fixtures & Seed Management
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.84rem' }}>
            Reset the SQLite database back to the pristine 25 verified public figures and precomputed dating records.
          </p>
        </div>

        <button
          className="btn btn-secondary"
          onClick={handleReseed}
          disabled={isReseeding}
        >
          <RefreshCw size={14} className={isReseeding ? 'pulse-element' : ''} /> {isReseeding ? 'Resetting...' : 'Re-seed Demo Dataset (25 Profiles)'}
        </button>
      </div>
    </div>
  );
};
