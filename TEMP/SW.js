// sw.js 파일 내용
self.addEventListener('install', (e) => {
    console.log('Service Worker: Installed');
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    console.log('Service Worker: Activated');
});

self.addEventListener('fetch', (e) => {
    // 모든 요청을 통과시켜서 설치 조건을 충족시킴
    e.respondWith(fetch(e.request));
});