document.addEventListener('DOMContentLoaded', () => {
  const updateBadge = count => {
    let badge = document.getElementById('cart-count');
    if (count > 0) {
      if (!badge) {
        badge = document.createElement('span');
        badge.id = 'cart-count';
        Object.assign(badge.style, {
          position: 'absolute',
          top: '-6px',
          right: '-12px',
          backgroundColor: '#e53935',
          color: 'white',
          borderRadius: '50%',
          padding: '2px 6px',
          fontSize: '12px'
        });
        document.querySelector('.cart-icon').appendChild(badge);
      }
      badge.textContent = count;
    } else if (badge) {
      badge.remove();
    }
  };

  document.querySelectorAll('.js-add-cart').forEach(btn => {
    btn.addEventListener('click', async e => {
      e.preventDefault();
      const url = btn.dataset.url;
      try {
        const res = await fetch(url);
        const data = await res.json();
        updateBadge(data.cart_count);
      } catch (err) {
        console.error('Cart update failed', err);
      }
    });
  });

  function toggleDropdown(event) {
    // Only allow dropdown on desktop
    if (window.innerWidth < 769) return;
    event.preventDefault();
    const dropdownMenu = document.getElementById('userDropdown');
    const dropdownArrow = event.currentTarget.querySelector('.dropdown-arrow');

    if (dropdownMenu.style.display === 'none' || !dropdownMenu.style.display) {
        dropdownMenu.style.display = 'block';
        dropdownArrow.style.transform = 'rotate(180deg)';
    } else {
        dropdownMenu.style.display = 'none';
        dropdownArrow.style.transform = 'rotate(0)';
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function closeDropdown(e) {
        if (!e.target.closest('.profile-desktop-dropdown')) {
            dropdownMenu.style.display = 'none';
            dropdownArrow.style.transform = 'rotate(0)';
            document.removeEventListener('click', closeDropdown);
        }
    });
}

  const dropdownToggle = document.querySelector('.dropdown-toggle');
  const dropdownMenu = document.querySelector('.dropdown-menu');
  const dropdownArrow = document.querySelector('.dropdown-arrow');

  if (dropdownToggle && dropdownMenu) {
    // Toggle dropdown on click
    dropdownToggle.addEventListener('click', toggleDropdown);

    // Close dropdown when clicking outside
    document.addEventListener('click', function (event) {
      const dropdowns = document.getElementsByClassName('dropdown-menu');
      const arrows = document.getElementsByClassName('dropdown-arrow');

      for (const dropdown of dropdowns) {
        if (dropdown.classList.contains('show')) {
          dropdown.classList.remove('show');
        }
      }

      for (const arrow of arrows) {
        arrow.style.transform = 'rotate(0)';
      }
    });

    // Close dropdown on escape key
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        const dropdowns = document.getElementsByClassName('dropdown-menu');
        const arrows = document.getElementsByClassName('dropdown-arrow');

        for (const dropdown of dropdowns) {
          dropdown.classList.remove('show');
        }

        for (const arrow of arrows) {
          arrow.style.transform = 'rotate(0)';
        }
      }
    });
  }

  // Mobile nav and blur overlay logic (match landing page)
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('mainNavLinks');
  const blurOverlay = document.getElementById('navBlurOverlay');

  function closeMobileNav() {
    navLinks.classList.remove('open');
    blurOverlay.classList.remove('active');
  }

  if (menuToggle && navLinks && blurOverlay) {
    menuToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      const isOpen = navLinks.classList.toggle('open');
      if (isOpen) {
        blurOverlay.classList.add('active');
      } else {
        blurOverlay.classList.remove('active');
      }
    });
    blurOverlay.addEventListener('click', closeMobileNav);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMobileNav();
    });
  }
});