const CACHE_NAME = 'deepfake-cache-v1';
const urlsToCache = [
  '/',
  '/index.html', // yahan aapka HTML file ka naam
  // Add any other assets (CSS, JS, icons) you want to cache
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});