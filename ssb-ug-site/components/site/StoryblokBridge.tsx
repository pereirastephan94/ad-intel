'use client';

import { useEffect } from 'react';

// Loads Storyblok's visual-editor bridge only inside the Storyblok editor
// (it opens the site with a `_storyblok` query parameter), and reloads the
// page when an editor saves or publishes, so changes show up immediately.
export default function StoryblokBridge() {
  useEffect(() => {
    if (!new URLSearchParams(window.location.search).has('_storyblok')) return;
    const s = document.createElement('script');
    s.src = 'https://app.storyblok.com/f/storyblok-v2-latest.js';
    s.async = true;
    s.onload = () => {
      const Bridge = (window as any).StoryblokBridge;
      if (!Bridge) return;
      const bridge = new Bridge();
      bridge.on(['published', 'change'], () => window.location.reload());
    };
    document.body.appendChild(s);
  }, []);
  return null;
}
