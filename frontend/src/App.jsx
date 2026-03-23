import React, { useState, useEffect, useRef } from 'react';
import Auth from './components/Auth.jsx';

const API = async (path, opts = {}) => {
  const token = localStorage.getItem('token');
  const res = await fetch('/api' + path, {
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    ...opts,
  });
  if (res.status === 401) { localStorage.removeItem('token'); window.location.reload(); }
  if (!res.ok) throw new Error(await res.text());
  return res.json();
};

function Card({ card, onDelete, onDragStart }) {
  return (
    <div
      draggable
      onDragStart={(e) => { e.dataTransfer.setData('cardId', String(card.id)); if (onDragStart) onDragStart(e, card); }}
      className="group bg-gray-700 hover:bg-gray-600 border border-gray-600 rounded-lg p-3 cursor-grab active:cursor-grabbing shadow-sm transition-all"
    >
      <div className="flex items-start justify-between gap-2">
        <p className="text-sm text-white font-medium leading-snug flex-1">{card.title}</p>
        <button onClick={() => onDelete(card.id)} className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 transition-all text-xs px-1">✕</button>
      </div>
      {card.description && <p className="text-xs text-gray-400 mt-1 leading-relaxed">{card.description}</p>}
    </div>
  );
}

function Column({ col, onCardDelete, onCardAdd, onDrop }) {
  const [adding, setAdding] = useState(false);
  const [title, setTitle] = useState('');
  const [dragOver, setDragOver] = useState(false);

  const handleAdd = async () => {
    if (!title.trim()) return;
    await onCardAdd(col.id, title.trim());
    setTitle(''); setAdding(false);
  };

  const DOTS = { 'Backlog': 'bg-gray-400', 'In Progress': 'bg-blue-500', 'Review': 'bg-yellow-500', 'Done': 'bg-green-500' };
  const dot = DOTS[col.title] || 'bg-purple-500';

  return (
    <div
      className={`flex flex-col w-72 min-w-[18rem] bg-gray-800 rounded-xl border transition-all ${dragOver ? 'border-blue-500 shadow-lg shadow-blue-500/20' : 'border-gray-700'}`}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(e) => { setDragOver(false); onDrop(e, col.id); }}
    >
      <div className="flex items-center gap-2 px-4 py-3 border-b border-gray-700">
        <span className={`w-2 h-2 rounded-full ${dot}`} />
        <span className="text-sm font-semibold text-gray-200 flex-1">{col.title}</span>
        <span className="text-xs text-gray-500 bg-gray-700 px-2 py-0.5 rounded-full">{(col.cards || []).length}</span>
      </div>
      <div className="flex flex-col gap-2 p-3 flex-1 min-h-[120px]">
        {(col.cards || []).map((card) => (
          <Card key={card.id} card={card} onDelete={onCardDelete} />
        ))}
      </div>
      <div className="p-3 border-t border-gray-700">
        {adding ? (
          <div className="flex flex-col gap-2">
            <input autoFocus value={title} onChange={(e) => setTitle(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleAdd(); if (e.key === 'Escape') setAdding(false); }}
              placeholder="Card title…"
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
            />
            <div className="flex gap-2">
              <button onClick={handleAdd} className="flex-1 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium py-1.5 rounded-lg transition-colors">Add</button>
              <button onClick={() => setAdding(false)} className="flex-1 bg-gray-700 hover:bg-gray-600 text-gray-300 text-xs font-medium py-1.5 rounded-lg transition-colors">Cancel</button>
            </div>
          </div>
        ) : (
          <button onClick={() => setAdding(true)} className="w-full text-left text-xs text-gray-400 hover:text-white hover:bg-gray-700 px-2 py-1.5 rounded-lg transition-colors">+ Add card</button>
        )}
      </div>
    </div>
  );
}

function BoardView({ boardId, onBack }) {
  const [board, setBoard] = useState(null);
  const load = () => API(`/boards/${boardId}`).then(setBoard);
  useEffect(() => { load(); }, [boardId]);

  const handleCardAdd = async (colId, title) => {
    await API(`/columns/${colId}/cards`, { method: 'POST', body: JSON.stringify({ title }) });
    load();
  };
  const handleCardDelete = async (cardId) => {
    await API(`/cards/${cardId}`, { method: 'DELETE' });
    load();
  };
  const handleDrop = async (e, targetColId) => {
    const cardId = parseInt(e.dataTransfer.getData('cardId'));
    if (!cardId) return;
    await API(`/cards/${cardId}/move`, { method: 'PATCH', body: JSON.stringify({ column_id: targetColId, position: 0 }) });
    load();
  };

  if (!board) return <div className="p-8 text-gray-400 text-sm">Loading…</div>;

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 px-6 py-4 border-b border-gray-700">
        <button onClick={onBack} className="text-gray-400 hover:text-white text-sm transition-colors">← Boards</button>
        <span className="text-gray-600">/</span>
        <h2 className="text-white font-semibold">{board.title}</h2>
      </div>
      <div className="flex gap-4 p-6 overflow-x-auto flex-1 items-start">
        {(board.columns || []).map((col) => (
          <Column key={col.id} col={col} onCardAdd={handleCardAdd} onCardDelete={handleCardDelete} onDrop={handleDrop} />
        ))}
      </div>
    </div>
  );
}

function BoardsList({ onSelectBoard }) {
  const [boards, setBoards] = useState([]);
  const [creating, setCreating] = useState(false);
  const [newTitle, setNewTitle] = useState('');

  const load = () => API('/boards').then(setBoards);
  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    if (!newTitle.trim()) return;
    await API('/boards', { method: 'POST', body: JSON.stringify({ title: newTitle.trim() }) });
    setNewTitle(''); setCreating(false); load();
  };

  const COLORS = ['from-blue-600 to-blue-800', 'from-purple-600 to-purple-800', 'from-green-600 to-green-800', 'from-orange-600 to-orange-800', 'from-pink-600 to-pink-800', 'from-teal-600 to-teal-800'];

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-white">My Boards</h2>
        <button onClick={() => setCreating(true)} className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">+ New Board</button>
      </div>
      {creating && (
        <div className="mb-6 flex gap-2">
          <input autoFocus value={newTitle} onChange={(e) => setNewTitle(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') handleCreate(); if (e.key === 'Escape') setCreating(false); }}
            placeholder="Board name…"
            className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
          />
          <button onClick={handleCreate} className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">Create</button>
          <button onClick={() => setCreating(false)} className="bg-gray-700 hover:bg-gray-600 text-gray-300 px-4 py-2 rounded-lg text-sm transition-colors">Cancel</button>
        </div>
      )}
      {boards.length === 0 && !creating ? (
        <div className="text-center py-20 text-gray-500">
          <div className="text-5xl mb-4">📋</div>
          <p className="text-lg font-medium text-gray-400">No boards yet</p>
          <p className="text-sm mt-1">Click "+ New Board" to get started</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {boards.map((b, i) => (
            <div key={b.id} onClick={() => onSelectBoard(b.id)}
              className={`group relative bg-gradient-to-br ${COLORS[i % COLORS.length]} rounded-xl p-5 cursor-pointer shadow-lg hover:scale-[1.02] transition-transform`}
            >
              <h3 className="text-white font-semibold text-lg">{b.title}</h3>
              <p className="text-white/60 text-xs mt-1">Backlog · In Progress · Review · Done</p>
              <button onClick={(e) => { e.stopPropagation(); if(confirm('Delete board?')) API(`/boards/${b.id}`, {method:'DELETE'}).then(load); }}
                className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 text-white/60 hover:text-white transition-all text-sm px-1">✕</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [selectedBoard, setSelectedBoard] = useState(null);

  useEffect(() => {
    if (isAuthenticated) API('/auth/me').then(setUser).catch(() => { localStorage.removeItem('token'); setIsAuthenticated(false); });
  }, [isAuthenticated]);

  if (!isAuthenticated) return <Auth onAuth={() => setIsAuthenticated(true)} />;

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <header className="flex items-center justify-between px-6 py-3 bg-gray-800 border-b border-gray-700 shadow-lg">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setSelectedBoard(null)}>
          <span className="text-xl">📋</span>
          <span className="text-lg font-bold tracking-tight">Kanban Board</span>
        </div>
        <div className="flex items-center gap-4">
          {user && <span className="text-sm text-gray-400">@{user.username}</span>}
          <button onClick={() => { localStorage.removeItem('token'); setIsAuthenticated(false); }}
            className="text-sm text-gray-400 hover:text-white bg-gray-700 hover:bg-gray-600 px-3 py-1.5 rounded-lg transition-colors">Logout</button>
        </div>
      </header>
      <main className="flex-1 overflow-hidden">
        {selectedBoard
          ? <BoardView boardId={selectedBoard} onBack={() => setSelectedBoard(null)} />
          : <BoardsList onSelectBoard={setSelectedBoard} />
        }
      </main>
    </div>
  );
}

export default App;
