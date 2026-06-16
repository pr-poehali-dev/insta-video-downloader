import { useState } from 'react';
import Icon from '@/components/ui/icon';

const QUALITIES = [
  { id: '720p', label: '720p', note: 'HD' },
  { id: '1080p', label: '1080p', note: 'Full HD' },
  { id: '4k', label: '4K', note: 'Ultra HD' },
];

const Index = () => {
  const [url, setUrl] = useState('');
  const [quality, setQuality] = useState('1080p');

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-neutral-900 font-sans overflow-hidden relative">
      <div className="pointer-events-none absolute -top-40 -right-40 h-[480px] w-[480px] rounded-full bg-gradient-to-br from-[#FF6637]/20 to-[#FFB199]/10 blur-3xl animate-float" />
      <div className="pointer-events-none absolute -bottom-52 -left-40 h-[520px] w-[520px] rounded-full bg-gradient-to-tr from-neutral-200/60 to-transparent blur-3xl" />

      <header className="relative z-10 mx-auto flex max-w-6xl items-center justify-between px-6 py-7">
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-neutral-900">
            <Icon name="ArrowDownToLine" size={18} className="text-white" />
          </div>
          <span className="font-display text-lg tracking-tight">Saver</span>
        </div>
        <nav className="hidden items-center gap-9 text-sm text-neutral-500 sm:flex">
          <a href="#home" className="transition-colors hover:text-neutral-900">Главная</a>
          <a href="#download" className="transition-colors hover:text-neutral-900">Скачивание</a>
        </nav>
      </header>

      <main id="home" className="relative z-10 mx-auto max-w-6xl px-6">
        <section className="pt-16 pb-10 text-center sm:pt-24">
          <div className="mx-auto mb-7 inline-flex items-center gap-2 rounded-full border border-neutral-200 bg-white/70 px-4 py-1.5 text-xs text-neutral-500 backdrop-blur animate-fade-up" style={{ animationDelay: '0ms' }}>
            <span className="h-1.5 w-1.5 rounded-full bg-[#FF6637]" />
            Без водяных знаков
          </div>
          <h1 className="mx-auto max-w-3xl font-display text-5xl leading-[1.05] tracking-tight sm:text-7xl animate-fade-up" style={{ animationDelay: '80ms' }}>
            Видео из Instagram
            <span className="block text-neutral-400">в один клик</span>
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg leading-relaxed text-neutral-500 animate-fade-up" style={{ animationDelay: '160ms' }}>
            Вставьте ссылку на пост или Reels и скачайте видео
            в качестве до 4K. Чисто, быстро, без лишнего.
          </p>
        </section>

        <section id="download" className="mx-auto max-w-2xl pb-28 animate-fade-up" style={{ animationDelay: '240ms' }}>
          <div className="rounded-3xl border border-neutral-200/80 bg-white p-3 shadow-[0_24px_80px_-32px_rgba(0,0,0,0.18)]">
            <div className="flex flex-col gap-3 sm:flex-row">
              <div className="flex flex-1 items-center gap-3 rounded-2xl bg-[#F4F4F1] px-5">
                <Icon name="Link" size={18} className="shrink-0 text-neutral-400" />
                <input
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="instagram.com/reel/..."
                  className="w-full bg-transparent py-5 text-base outline-none placeholder:text-neutral-400"
                />
              </div>
              <button className="group flex items-center justify-center gap-2 rounded-2xl bg-neutral-900 px-7 py-5 font-medium text-white transition-all hover:bg-[#FF6637]">
                Скачать
                <Icon name="ArrowDown" size={18} className="transition-transform group-hover:translate-y-0.5" />
              </button>
            </div>

            <div className="mt-3 grid grid-cols-3 gap-2">
              {QUALITIES.map((q) => {
                const active = quality === q.id;
                return (
                  <button
                    key={q.id}
                    onClick={() => setQuality(q.id)}
                    className={`flex flex-col items-center rounded-2xl border py-4 transition-all ${
                      active
                        ? 'border-neutral-900 bg-neutral-900 text-white'
                        : 'border-neutral-200 bg-white text-neutral-700 hover:border-neutral-300'
                    }`}
                  >
                    <span className="text-base font-semibold">{q.label}</span>
                    <span className={`text-xs ${active ? 'text-white/60' : 'text-neutral-400'}`}>{q.note}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-sm text-neutral-400">
            <span className="flex items-center gap-2"><Icon name="Zap" size={15} /> Мгновенно</span>
            <span className="flex items-center gap-2"><Icon name="ShieldCheck" size={15} /> Без регистрации</span>
            <span className="flex items-center gap-2"><Icon name="Infinity" size={15} /> Без ограничений</span>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
