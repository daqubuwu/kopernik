// Simple animations and interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-item, .review-item, .team-member, .value-item');

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elementPosition < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Set initial state for animated elements
    const animatedElements = document.querySelectorAll('.feature-item, .review-item, .team-member, .value-item');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });

    // Run once on page load
    animateOnScroll();

    // Run on scroll
    window.addEventListener('scroll', animateOnScroll);

    // Mobile menu toggle (if needed in future)
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    if (mobileMenuToggle) {
        const nav = document.querySelector('nav ul');

        mobileMenuToggle.addEventListener('click', function() {
            nav.classList.toggle('active');
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form form');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Проверка перед отправкой
            const username = this.querySelector('#id_username').value;
            const password = this.querySelector('#id_password').value;

            if (!username || !password) {
                e.preventDefault();
                alert('Заполните все поля');
            }
        });
    }
});


// Автоматическое закрытие уведомления через 5 секунд
document.addEventListener('DOMContentLoaded', function() {
  const closeButtons = document.querySelectorAll('.close-btn');

  closeButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      this.parentElement.style.display = 'none';
    });
  });

  // Авто-закрытие через 5 секунд
  setTimeout(() => {
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notif => {
      notif.style.display = 'none';
    });
  }, 5000);
});
