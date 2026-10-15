import React, { useState, useEffect } from 'react';
import type { Person, DemoOverview } from './types';
import { fetchPeople, fetchDemoOverview } from './api';
import { DashboardView } from './views/DashboardView';
import { DirectoryView } from './views/DirectoryView';
import { ProfileView } from './views/ProfileView';
import { DatingRoomView } from './views/DatingRoomView';
import { RankingsView } from './views/RankingsView';
import { SettingsView } from './views/SettingsView';
import { 
  LayoutDashboard, Users, HeartHandshake, Award, Settings, 
  Sparkles, ShieldCheck
} from 'lucide-react';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'dashboard' | 'directory' | 'profile' | 'dating' | 'rankings' | 'settings'>('dashboard');
  const [people, setPeople] = useState<Person[]>([]);
  const [demo, setDemo] = useState<DemoOverview | null>(null);
  const [selectedPersonId, setSelectedPersonId] = useState<string | null>(null);
  const [datingTargetAId, setDatingTargetAId] = useState<string | undefined>(undefined);
  const [datingTargetBId, setDatingTargetBId] = useState<string | undefined>(undefined);
  const [datingSessionId, setDatingSessionId] = useState<string | undefined>(undefined);
  const [, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    setLoading(true);
    try {
      const [peopleRes, demoRes] = await Promise.all([
        fetchPeople(),
        fetchDemoOverview()
      ]);
      setPeople(peopleRes.people);
      setDemo(demoRes);
    } catch (e) {
      console.error("Error loading app data:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleNavigate = (tab: string, personId?: string, sessionId?: string) => {
    if (personId) {
      setSelectedPersonId(personId);
    }
    if (sessionId) {
      setDatingSessionId(sessionId);
    }
    setCurrentTab(tab as any);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectPersonForDossier = (personId: string) => {
    setSelectedPersonId(personId);
    setCurrentTab('profile');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleStartDate = (personAId: string, personBId?: string) => {
    setDatingTargetAId(personAId);
    setDatingTargetBId(personBId);
    setDatingSessionId(undefined);
    setCurrentTab('dating');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleOpenDatingSession = (sessionId: string) => {
    setDatingSessionId(sessionId);
    setCurrentTab('dating');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <header style={{
        position: 'sticky',
        top: 0,
        zIndex: 100,
        background: 'rgba(10, 12, 16, 0.88)',
        backdropFilter: 'blur(16px)',
        borderBottom: '1px solid var(--border-subtle)',
        padding: '14px 28px'
      }}>
        <div style={{ maxWidth: 1300, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {/* Brand Logo */}
          <div 
            onClick={() => handleNavigate('dashboard')} 
            style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer' }}
          >
            <div style={{
              width: 36,
              height: 36,
              borderRadius: 'var(--radius-sm)',
              background: 'linear-gradient(135deg, #f59e0b, #f43f5e)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 15px rgba(245, 158, 11, 0.4)'
            }}>
              <Sparkles size={20} color="#000" />
            </div>
            <div>
              <div style={{ fontWeight: 800, fontSize: '1.05rem', letterSpacing: '-0.02em', color: '#fff' }}>
                CANDA <span style={{ color: 'var(--accent-gold)' }}>ADS</span> AGENTIC DATING
              </div>
              <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Autonomous Compatibility Engine
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
            <button 
              className={`nav-link ${currentTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => handleNavigate('dashboard')}
            >
              <LayoutDashboard size={15} /> Dashboard
            </button>
            <button 
              className={`nav-link ${currentTab === 'directory' ? 'active' : ''}`}
              onClick={() => handleNavigate('directory')}
            >
              <Users size={15} /> People Directory ({people.length})
            </button>
            <button 
              className={`nav-link ${currentTab === 'dating' ? 'active' : ''}`}
              onClick={() => handleNavigate('dating')}
            >
              <HeartHandshake size={15} /> Agent Dating Room
            </button>
            <button 
              className={`nav-link ${currentTab === 'rankings' ? 'active' : ''}`}
              onClick={() => handleNavigate('rankings')}
            >
              <Award size={15} /> Rankings Matrix
            </button>
            <button 
              className={`nav-link ${currentTab === 'settings' ? 'active' : ''}`}
              onClick={() => handleNavigate('settings')}
            >
              <Settings size={15} /> Ingestion & Apify
            </button>
          </nav>

          {/* Status Badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span className="badge badge-emerald" style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <ShieldCheck size={12} /> {people.length} Verified Agents
            </span>
          </div>
        </div>
      </header>

      {/* Main Content View Container */}
      <main style={{ maxWidth: 1300, width: '100%', margin: '0 auto', padding: '32px 24px', flex: 1 }}>
        {currentTab === 'dashboard' && (
          <DashboardView demo={demo} onNavigate={handleNavigate} />
        )}

        {currentTab === 'directory' && (
          <DirectoryView 
            people={people} 
            onSelectPerson={handleSelectPersonForDossier}
            onStartDate={handleStartDate}
          />
        )}

        {currentTab === 'profile' && (
          <ProfileView 
            personId={selectedPersonId || people[0]?.id || ''} 
            onBack={() => handleNavigate('directory')}
            onStartDate={handleStartDate}
            onOpenSession={handleOpenDatingSession}
          />
        )}

        {currentTab === 'dating' && (
          <DatingRoomView 
            people={people} 
            initialPersonAId={datingTargetAId}
            initialPersonBId={datingTargetBId}
            initialSessionId={datingSessionId}
            onViewProfile={handleSelectPersonForDossier}
          />
        )}

        {currentTab === 'rankings' && (
          <RankingsView 
            people={people} 
            onViewProfile={handleSelectPersonForDossier}
            onOpenDatingSession={handleOpenDatingSession}
          />
        )}

        {currentTab === 'settings' && (
          <SettingsView onRefreshAll={loadAllData} />
        )}
      </main>

      {/* Editorial Footer */}
      <footer style={{
        borderTop: '1px solid var(--border-subtle)',
        background: 'var(--bg-secondary)',
        padding: '24px 28px',
        marginTop: 48
      }}>
        <div style={{ maxWidth: 1300, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 14 }}>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            &copy; 2026 Canda ads Agentic Dating Assessment MVP. Built for production demonstration with 25 verified public figures.
          </div>
          <div style={{ display: 'flex', gap: 16, fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
            <span>Apify API Integration Ready</span>
            <span>&bull;</span>
            <span>Deterministic Compatibility Scoring</span>
            <span>&bull;</span>
            <span>Simulated Agent Interactions</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
