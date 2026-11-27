if (window.gsap && window.ScrollTrigger && !navigator.connection?.saveData) {
  gsap.registerPlugin(ScrollTrigger);
  const motion = gsap.matchMedia();
  motion.add({
    animate: '(prefers-reduced-motion: no-preference) and (min-height: 521px)',
    portrait: '(max-width: 700px) and (orientation: portrait)'
  }, ({ conditions }) => {
    if (!conditions.animate) return;
    const video = document.querySelector('.media video');
    const playhead = { position: 0 };
    function seek() {
      if (video.readyState < 2 || video.seeking) return;
      const time = playhead.position * Math.max(0, video.duration - .08);
      if (Math.abs(video.currentTime - time) > .03) video.currentTime = time;
    }
    function showVideo() {
      video.classList.add('ready');
      seek();
    }
    function hideVideo() {
      video.classList.remove('ready');
    }
    video.addEventListener('loadeddata', showVideo);
    video.addEventListener('seeked', seek);
    video.addEventListener('error', hideVideo);
    const request = new AbortController();
    let mediaUrl;
    fetch(conditions.portrait ? video.dataset.tallSrc : video.dataset.wideSrc, { signal: request.signal })
      .then(response => {
        if (!response.ok) throw new Error('Video unavailable');
        return response.blob();
      })
      .then(blob => {
        if (request.signal.aborted) return;
        mediaUrl = URL.createObjectURL(blob);
        video.src = mediaUrl;
      })
      .catch(() => { if (!request.signal.aborted) hideVideo(); });
    const film = gsap.timeline({
      defaults: { ease: 'none', duration: 1 },
      scrollTrigger: {
        trigger: '.scene',
        start: 'top top',
        end: () => '+=' + Math.round(innerHeight * (conditions.portrait ? 1.0 : 1.25)),
        pin: true,
        scrub: .65,
        invalidateOnRefresh: true
      }
    });
    film.to(playhead, { position: 1, onUpdate: seek }, 0)
      .to('.media', { scale: 1.085 }, 0)
      .to('.progress', { scaleX: 1 }, 0);
    return () => {
      request.abort();
      if (mediaUrl) URL.revokeObjectURL(mediaUrl);
      video.removeEventListener('loadeddata', showVideo);
      video.removeEventListener('seeked', seek);
      video.removeEventListener('error', hideVideo);
      hideVideo();
      video.removeAttribute('src');
      video.load();
    };
  });
}

if (window.gsap && window.ScrollTrigger && !navigator.connection?.saveData) {
  gsap.matchMedia().add('(prefers-reduced-motion: no-preference)', () => {
    gsap.utils.toArray('.frame').forEach(frame => {
      gsap.fromTo(frame.querySelector('picture'), { yPercent: -3, scale: 1.08 },
        { yPercent: 3, scale: 1.08, ease: 'none', scrollTrigger: {
          trigger: frame, start: 'top bottom', end: 'bottom top', scrub: .45
        } });
    });

    gsap.from('.studio-photo img', { scale: 1.07, yPercent: 2, ease: 'power3.out',
      duration: .85, scrollTrigger: { trigger: '.studio-photo', start: 'top 82%', once: true } });

    gsap.from('.contact-rule', { scaleX: .18, ease: 'power3.out', duration: .65,
      scrollTrigger: { trigger: '.contact-rule', start: 'top 88%', once: true } });
  });
}
