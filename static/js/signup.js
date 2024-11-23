let currentAnimation = null;

// Animation function for focus events
function animatePath(offset) {
  if (currentAnimation) currentAnimation.pause();
  currentAnimation = anime({
    targets: 'path',
    strokeDashoffset: {
      value: offset,
      duration: 700,
      easing: 'easeOutQuart',
    },
    strokeDasharray: {
      value: '240 1386',
      duration: 700,
      easing: 'easeOutQuart',
    },
  });
}

// Event listeners for input fields
document.querySelector('#email').addEventListener('focus', function () {
  animatePath(0); // Position for email
});

document.querySelector('#username').addEventListener('focus', function () {
  animatePath(-336); // Position for username
});

document.querySelector('#password1').addEventListener('focus', function () {
  animatePath(-672); // Position for password1
});

document.querySelector('#password2').addEventListener('focus', function () {
  animatePath(-170); // Position for password2
});
