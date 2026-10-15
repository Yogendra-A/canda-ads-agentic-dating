import type { Person, DatingSession, RankingItem, DemoOverview, SettingsResponse } from './types';

const API_BASE = '/api';

export async function fetchHealth(): Promise<any> {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchPeople(search?: string, collectionMethod?: string): Promise<{ total: number; count: number; people: Person[] }> {
  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (collectionMethod) params.append('collection_method', collectionMethod);
  params.append('limit', '50');

  const res = await fetch(`${API_BASE}/people?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch people');
  return res.json();
}

export async function fetchPersonDetail(personId: string): Promise<Person> {
  const res = await fetch(`${API_BASE}/people/${personId}`);
  if (!res.ok) throw new Error('Failed to fetch person details');
  return res.json();
}

export async function fetchDatingSessions(): Promise<DatingSession[]> {
  const res = await fetch(`${API_BASE}/dating/sessions`);
  if (!res.ok) throw new Error('Failed to fetch dating sessions');
  return res.json();
}

export async function fetchDatingSessionDetail(sessionId: string): Promise<DatingSession> {
  const res = await fetch(`${API_BASE}/dating/sessions/${sessionId}`);
  if (!res.ok) throw new Error('Failed to fetch session detail');
  return res.json();
}

export async function runDatingSession(personAId: string, personBId: string, turnsCount: number = 6): Promise<DatingSession> {
  const res = await fetch(`${API_BASE}/dating/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ person_a_id: personAId, person_b_id: personBId, turns_count: turnsCount }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to run dating session');
  }
  return res.json();
}

export async function fetchRankings(personId: string): Promise<{ target_person_id: string; count: number; rankings: RankingItem[] }> {
  const res = await fetch(`${API_BASE}/rankings/${personId}`);
  if (!res.ok) throw new Error('Failed to fetch rankings');
  return res.json();
}

export async function fetchDemoOverview(): Promise<DemoOverview> {
  const res = await fetch(`${API_BASE}/demo`);
  if (!res.ok) throw new Error('Failed to fetch demo overview');
  return res.json();
}

export async function reseedDemo(): Promise<any> {
  const res = await fetch(`${API_BASE}/demo/seed`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to re-seed demo data');
  return res.json();
}

export async function fetchSettings(): Promise<SettingsResponse> {
  const res = await fetch(`${API_BASE}/settings`);
  if (!res.ok) throw new Error('Failed to fetch settings');
  return res.json();
}

export async function importPeopleDataset(payload: { people: any[] }): Promise<any> {
  const res = await fetch(`${API_BASE}/people/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Import failed');
  }
  return res.json();
}

export async function triggerCollection(actorId?: string, platform?: string, profileUrls?: string[]): Promise<any> {
  const res = await fetch(`${API_BASE}/collection/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ actor_id: actorId, platform: platform, profile_urls: profileUrls }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to start collection');
  }
  return res.json();
}

export async function analyzePersonProfile(personId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/people/${personId}/analyze`, { method: 'POST' });
  if (!res.ok) throw new Error('Analysis failed');
  return res.json();
}
