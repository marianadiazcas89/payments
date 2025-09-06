// === gesture.js ===
// Handles swipe & arrow-key navigation with GSAP transition

// Configuration: map gestures to pages
const gestureRoutes = {
  swipeleft: () => navigateTo('make_payment.html'),
  swiperight: () => history.back(),
  swipeup: () => navigateTo('home.html'),
  swipedown: () => navigateTo('settings.html')  // Add if needed
};

// Animate then navigate
function navigateTo(target) {
  if (!target || gestureBlocked) return;

  gestureBlocked = true; // prevent double triggers

  gsap.to("body", {
    x: "-100%",
    opacity: 0,
    duration: 0.45,
    ease: "power1.inOut",
    onComplete: () => window.location.href = target
  });
}

let gestureBlocked = false;

document.addEventListener("DOMContentLoaded", () => {
  const zone = document.body;

  // Hammer.js setup
  const mc = new Hammer(zone);
  mc.get('swipe').set({ direction: Hammer.DIRECTION_ALL });

  mc.on("swipeleft swiperight swipeup swipedown", (ev) => {
    const handler = gestureRoutes[ev.type];
    if (handler) handler();
  });

  // ✅ Optional fallback: keyboard arrow keys
  window.addEventListener("keydown", (e) => {
    if (gestureBlocked) return;

    const keyMap = {
      ArrowLeft: "swipeleft",
      ArrowRight: "swiperight",
      ArrowUp: "swipeup",
      ArrowDown: "swipedown"
    };

    const gesture = keyMap[e.key];
    if (gesture && gestureRoutes[gesture]) {
      gestureRoutes[gesture]();
    }
  });
});
