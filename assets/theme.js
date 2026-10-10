/* Anjum Mart theme scripts — vanilla JS, no dependencies. */
(function () {
  'use strict';

  var config = (window.AnjumMart = window.AnjumMart || { routes: {}, strings: {} });
  var routes = config.routes;
  var strings = config.strings;

  /* ------------------------------------------------------------------
     Utilities
     ------------------------------------------------------------------ */
  function debounce(fn, wait) {
    var t;
    return function () {
      var args = arguments;
      var ctx = this;
      clearTimeout(t);
      t = setTimeout(function () {
        fn.apply(ctx, args);
      }, wait);
    };
  }

  function parseHTML(html) {
    return new DOMParser().parseFromString(html, 'text/html');
  }

  function formatMoney(cents, format) {
    if (typeof cents === 'string') cents = cents.replace('.', '');
    var value = '';
    var placeholderRegex = /\{\{\s*(\w+)\s*\}\}/;
    var formatString = format || config.moneyFormat || '{{amount}}';

    function formatWithDelimiters(number, precision, thousands, decimal) {
      thousands = thousands || ',';
      decimal = decimal || '.';
      if (isNaN(number) || number == null) return 0;
      number = (number / 100.0).toFixed(precision);
      var parts = number.split('.');
      var dollars = parts[0].replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1' + thousands);
      var centsPart = parts[1] ? decimal + parts[1] : '';
      return dollars + centsPart;
    }

    var match = formatString.match(placeholderRegex);
    switch (match ? match[1] : 'amount') {
      case 'amount':
        value = formatWithDelimiters(cents, 2);
        break;
      case 'amount_no_decimals':
        value = formatWithDelimiters(cents, 0);
        break;
      case 'amount_with_comma_separator':
        value = formatWithDelimiters(cents, 2, '.', ',');
        break;
      case 'amount_no_decimals_with_comma_separator':
        value = formatWithDelimiters(cents, 0, '.', ',');
        break;
      case 'amount_with_apostrophe_separator':
        value = formatWithDelimiters(cents, 2, "'", '.');
        break;
      case 'amount_no_decimals_with_space_separator':
        value = formatWithDelimiters(cents, 0, ' ');
        break;
      case 'amount_with_space_separator':
        value = formatWithDelimiters(cents, 2, ' ', ',');
        break;
      case 'amount_with_period_and_space_separator':
        value = formatWithDelimiters(cents, 2, ' ', '.');
        break;
      default:
        value = formatWithDelimiters(cents, 2);
    }
    return formatString.replace(placeholderRegex, value);
  }

  var toastEl;
  var toastTimer;
  function ensureToast() {
    if (toastEl) return toastEl;
    toastEl = document.createElement('div');
    toastEl.className = 'toast';
    toastEl.setAttribute('role', 'status');
    toastEl.setAttribute('aria-live', 'polite');
    document.body.appendChild(toastEl);
    return toastEl;
  }

  function announce(message) {
    var region = document.getElementById('A11yStatus');
    if (!region) return;
    region.textContent = '';
    setTimeout(function () {
      region.textContent = message;
    }, 50);
  }

  function toast(message, type) {
    ensureToast();
    toastEl.textContent = message;
    toastEl.classList.toggle('toast--error', type === 'error');
    requestAnimationFrame(function () {
      toastEl.classList.add('is-visible');
    });
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toastEl.classList.remove('is-visible');
    }, 4000);
  }

  var FOCUSABLE =
    'a[href], area[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

  /* ------------------------------------------------------------------
     Drawer (mobile menu, cart, filters)
     ------------------------------------------------------------------ */
  var openDrawer = null;

  function Drawer(el) {
    this.el = el;
    this.panel = el.querySelector('.drawer__panel');
    this.trigger = null;
    var self = this;
    el.addEventListener('click', function (e) {
      if (e.target.closest('[data-drawer-close]')) {
        e.preventDefault();
        self.close();
      }
    });
    el.addEventListener('keydown', function (e) {
      if (!el.classList.contains('is-open')) return;
      if (e.key === 'Escape') self.close();
      if (e.key === 'Tab') self.trapFocus(e);
    });
  }

  function setExpanded(trigger, value) {
    if (trigger && trigger.hasAttribute && trigger.hasAttribute('aria-expanded')) trigger.setAttribute('aria-expanded', value);
  }

  Drawer.prototype.open = function (trigger) {
    if (openDrawer && openDrawer !== this) openDrawer.close(true);
    this.trigger = trigger || document.activeElement;
    this.el.hidden = false;
    var self = this;
    requestAnimationFrame(function () {
      self.el.classList.add('is-open');
      if (self.el.hasAttribute('data-static-desktop')) {
        self.panel.setAttribute('role', 'dialog');
        self.panel.setAttribute('aria-modal', 'true');
        var title = self.panel.querySelector('h2[id]');
        if (title) self.panel.setAttribute('aria-labelledby', title.id);
      } else {
        self.el.setAttribute('aria-hidden', 'false');
      }
      document.body.classList.add('overflow-hidden');
      setExpanded(self.trigger, 'true');
      var focusTarget = self.panel.querySelector('[data-drawer-focus]') || self.panel.querySelector(FOCUSABLE);
      if (focusTarget) setTimeout(function () { focusTarget.focus(); }, 60);
    });
    openDrawer = this;
  };

  Drawer.prototype.close = function (skipFocus) {
    this.el.classList.remove('is-open');
    if (this.el.hasAttribute('data-static-desktop')) {
      this.panel.removeAttribute('role');
      this.panel.removeAttribute('aria-modal');
      this.panel.removeAttribute('aria-labelledby');
    } else {
      this.el.setAttribute('aria-hidden', 'true');
    }
    document.body.classList.remove('overflow-hidden');
    setExpanded(this.trigger, 'false');
    if (!skipFocus && this.trigger && this.trigger.focus) this.trigger.focus();
    if (openDrawer === this) openDrawer = null;
  };

  Drawer.prototype.trapFocus = function (e) {
    var nodes = Array.prototype.filter.call(this.panel.querySelectorAll(FOCUSABLE), function (n) {
      return n.offsetParent !== null;
    });
    if (!nodes.length) return;
    var first = nodes[0];
    var last = nodes[nodes.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  };

  var drawers = {};
  function getDrawer(id) {
    if (drawers[id] && drawers[id].el.isConnected) return drawers[id];
    var el = document.getElementById(id);
    if (!el) return null;
    drawers[id] = new Drawer(el);
    return drawers[id];
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && openDrawer && !openDrawer.el.contains(e.target)) openDrawer.close();
  });

  document.addEventListener('click', function (e) {
    var toggle = e.target.closest('[data-drawer-open]');
    if (!toggle) return;
    var drawer = getDrawer(toggle.getAttribute('data-drawer-open'));
    if (!drawer) return;
    e.preventDefault();
    drawer.open(toggle);
  });

  /* ------------------------------------------------------------------
     Header: sticky shadow, announcement rotation
     ------------------------------------------------------------------ */
  function initHeader() {
    var header = document.querySelector('[data-site-header]');
    if (header) {
      var onScroll = function () {
        header.classList.toggle('is-scrolled', window.scrollY > 8);
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
      var setOffset = function () {
        document.documentElement.style.setProperty('--header-sticky-offset', header.offsetHeight + 20 + 'px');
      };
      setOffset();
      window.addEventListener('resize', debounce(setOffset, 150));
    }


    // Close desktop dropdowns when clicking outside or pressing Escape
    document.addEventListener('click', function (e) {
      document.querySelectorAll('[data-nav-dropdown][open]').forEach(function (d) {
        if (!d.contains(e.target)) d.removeAttribute('open');
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      document.querySelectorAll('[data-nav-dropdown][open]').forEach(function (d) {
        d.removeAttribute('open');
        var summary = d.querySelector('summary');
        if (summary) summary.focus();
      });
    });
  }

  function initAnnouncements(scope) {
    (scope || document).querySelectorAll('[data-announcement]').forEach(function (bar) {
      clearInterval(bar._timer);
      var messages = bar.querySelectorAll('.announcement-bar__message');
      if (!messages.length) return;
      messages.forEach(function (m) {
        m.classList.remove('is-active');
      });
      messages[0].classList.add('is-active');
      if (messages.length < 2) return;
      var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var index = 0;
      var speed = parseInt(bar.getAttribute('data-speed'), 10) || 5;
      var paused = reduced;
      var toggle = bar.querySelector('[data-announcement-toggle]');
      var stop = function () {
        clearInterval(bar._timer);
      };
      var start = function () {
        stop();
        if (paused) return;
        bar._timer = setInterval(function () {
          messages[index].classList.remove('is-active');
          index = (index + 1) % messages.length;
          messages[index].classList.add('is-active');
        }, speed * 1000);
      };
      var resume = function () {
        if (!bar.matches(':hover') && !bar.contains(document.activeElement)) start();
      };
      if (toggle) {
        toggle.hidden = false;
        toggle.setAttribute('aria-pressed', paused ? 'true' : 'false');
        toggle.addEventListener('click', function () {
          paused = !paused;
          toggle.setAttribute('aria-pressed', paused ? 'true' : 'false');
          if (paused) stop();
          else resume();
        });
      }
      bar.addEventListener('mouseenter', stop);
      bar.addEventListener('mouseleave', resume);
      bar.addEventListener('focusin', stop);
      bar.addEventListener('focusout', function () {
        setTimeout(resume, 0);
      });
      start();
    });
  }

  /* ------------------------------------------------------------------
     Predictive search
     ------------------------------------------------------------------ */
  function PredictiveSearch(form) {
    this.form = form;
    this.input = form.querySelector('input[type="search"]');
    this.results = form.querySelector('[data-predictive-results]');
    this.status = form.querySelector('[data-predictive-status]');
    if (!this.input || !this.results || !routes.predictiveSearch) return;
    this.cache = {};
    this.abort = null;
    var self = this;
    this.input.addEventListener(
      'input',
      debounce(function () {
        self.onInput();
      }, 260)
    );
    this.input.addEventListener('focus', function () {
      if (self.input.value.trim().length && self.results.innerHTML.trim()) self.open();
    });
    this.input.addEventListener('keydown', function (e) {
      self.onKeydown(e);
    });
    document.addEventListener('click', function (e) {
      if (!self.form.contains(e.target)) self.close();
    });
    form.addEventListener('focusout', function () {
      setTimeout(function () {
        if (!self.form.contains(document.activeElement)) self.close();
      }, 0);
    });
  }

  PredictiveSearch.prototype.onInput = function () {
    var term = this.input.value.trim();
    if (!term.length) {
      this.close();
      return;
    }
    this.fetchResults(term);
  };

  PredictiveSearch.prototype.fetchResults = function (term) {
    var self = this;
    var key = term.toLowerCase();
    if (this.cache[key]) {
      this.render(this.cache[key]);
      return;
    }
    if (this.abort) this.abort.abort();
    this.abort = typeof AbortController !== 'undefined' ? new AbortController() : null;
    this.results.innerHTML = '<p class="predictive-search__loading" aria-hidden="true">' + (strings.loading || 'Loading…') + '</p>';
    this.setStatus(strings.loading || 'Loading…');
    this.open();
    var url =
      routes.predictiveSearch +
      '?q=' +
      encodeURIComponent(term) +
      '&section_id=predictive-search' +
      '&resources[type]=product,collection,query' +
      '&resources[limit]=6' +
      '&resources[limit_scope]=each' +
      '&resources[options][unavailable_products]=last' +
      '&resources[options][fields]=title,product_type,variants.title,vendor,tag';
    fetch(url, { signal: this.abort ? this.abort.signal : undefined })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      })
      .then(function (text) {
        var doc = parseHTML(text);
        var section = doc.querySelector('#shopify-section-predictive-search') || doc.body;
        var html = section.innerHTML;
        self.cache[key] = html;
        if (self.input.value.trim().toLowerCase() === key) self.render(html);
      })
      .catch(function (err) {
        if (err && err.name === 'AbortError') return;
        self.close();
      });
  };

  PredictiveSearch.prototype.render = function (html) {
    this.results.innerHTML = html;
    var prefix = this.results.id || 'predictive';
    this.results.querySelectorAll('[role="option"]').forEach(function (option, i) {
      option.id = prefix + '-option-' + i;
      option.setAttribute('aria-selected', 'false');
    });
    this.input.removeAttribute('aria-activedescendant');
    var empty = this.results.querySelector('.predictive-search__empty');
    if (empty) {
      this.setStatus(empty.textContent.trim());
    } else {
      var count = this.results.querySelectorAll('[role="option"]:not(.predictive-search__all)').length;
      this.setStatus((strings.suggestions || '[count] suggestions').replace('[count]', count));
    }
    this.open();
  };

  PredictiveSearch.prototype.setStatus = function (message) {
    if (this.status) this.status.textContent = message;
  };

  PredictiveSearch.prototype.open = function () {
    this.results.hidden = false;
    this.input.setAttribute('aria-expanded', 'true');
  };

  PredictiveSearch.prototype.close = function () {
    this.results.hidden = true;
    this.input.setAttribute('aria-expanded', 'false');
    this.input.removeAttribute('aria-activedescendant');
  };

  PredictiveSearch.prototype.onKeydown = function (e) {
    if (e.key === 'Escape') {
      this.close();
      return;
    }
    if (this.results.hidden) return;
    var options = Array.prototype.slice.call(this.results.querySelectorAll('[role="option"]'));
    if (!options.length) return;
    var current = this.results.querySelector('[aria-selected="true"]');
    var index = options.indexOf(current);
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      index = e.key === 'ArrowDown' ? index + 1 : index - 1;
      if (index >= options.length) index = 0;
      if (index < 0) index = options.length - 1;
      if (current) current.setAttribute('aria-selected', 'false');
      options[index].setAttribute('aria-selected', 'true');
      this.input.setAttribute('aria-activedescendant', options[index].id);
      options[index].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter' && current) {
      e.preventDefault();
      var link = current.tagName === 'A' ? current : current.querySelector('a');
      if (link) window.location.href = link.href;
      else if (current.tagName === 'BUTTON') current.click();
    }
  };

  /* ------------------------------------------------------------------
     Cart
     ------------------------------------------------------------------ */
  var Cart = {
    drawerId: 'CartDrawer',

    sectionsToRender: function () {
      var ids = ['cart-drawer'];
      var page = document.querySelector('[data-cart-page]');
      if (page && page.getAttribute('data-section-id')) ids.push(page.getAttribute('data-section-id'));
      return ids;
    },

    add: function (form, button) {
      var self = this;
      var errorEl = form.querySelector('[data-form-error]');
      if (errorEl) {
        errorEl.hidden = true;
        errorEl.textContent = '';
      }
      if (button) {
        button.classList.add('is-loading');
        button.setAttribute('aria-disabled', 'true');
      }
      var body = new FormData(form);
      body.append('sections', this.sectionsToRender().join(','));
      body.append('sections_url', window.location.pathname);
      return fetch(routes.cartAdd + '.js', {
        method: 'POST',
        headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        body: body
      })
        .then(function (r) {
          return r.json().then(function (data) {
            return { ok: r.ok, data: data };
          });
        })
        .then(function (res) {
          if (!res.ok || res.data.status) {
            var message = res.data.description || res.data.message || strings.cartError;
            if (errorEl) {
              errorEl.textContent = message;
              errorEl.hidden = false;
            } else {
              toast(message, 'error');
            }
            return;
          }
          if (config.cartType === 'page') {
            window.location.href = routes.cart;
            return;
          }
          self.renderSections(res.data.sections);
          var drawer = getDrawer(self.drawerId);
          if (drawer && !document.querySelector('[data-cart-page]')) {
            drawer.open(button);
          } else {
            toast(strings.added || 'Added to cart');
          }
        })
        .catch(function () {
          toast(strings.cartError, 'error');
        })
        .finally(function () {
          if (button) {
            button.classList.remove('is-loading');
            button.removeAttribute('aria-disabled');
          }
        });
    },

    setBusy: function (busy) {
      document.querySelectorAll('[data-cart-drawer-content], [data-cart-page]').forEach(function (el) {
        el.classList.toggle('is-busy', busy);
        el.setAttribute('aria-busy', busy ? 'true' : 'false');
      });
    },

    change: function (key, quantity, itemEl) {
      var self = this;
      if (this.pending) {
        // Run the latest change made while a request is in flight once it finishes
        this.queued = { key: key, quantity: quantity };
        return Promise.resolve();
      }
      this.pending = true;
      this.setBusy(true);
      if (itemEl) itemEl.classList.add('is-updating');
      var title = itemEl && itemEl.querySelector('.cart-item__title');
      return fetch(routes.cartChange + '.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          id: String(key),
          quantity: quantity,
          sections: this.sectionsToRender().join(','),
          sections_url: window.location.pathname
        })
      })
        .then(function (r) {
          return r.json().then(function (data) {
            return { ok: r.ok, data: data };
          });
        })
        .then(function (res) {
          if (!res.ok || res.data.status) {
            var message = res.data.description || res.data.message || strings.cartError;
            if (itemEl) {
              itemEl.classList.remove('is-updating');
              var err = itemEl.querySelector('[data-line-error]');
              if (err) {
                err.textContent = message;
                err.hidden = false;
              }
              var input = itemEl.querySelector('input[data-line-key]');
              if (input && input.defaultValue) input.value = input.defaultValue;
            } else {
              toast(message, 'error');
            }
            announce(message);
            return;
          }
          self.renderSections(res.data.sections);
          if (quantity === 0 && title) {
            announce((strings.removed || 'Removed [title]').replace('[title]', title.textContent.trim()));
          } else {
            var total = document.querySelector('[data-cart-drawer-content] .cart-summary__total, [data-cart-page] .cart-summary__total');
            announce((strings.cartUpdated || 'Cart updated') + (total ? '. ' + (strings.subtotal || 'Subtotal') + ' ' + total.textContent.trim() : ''));
          }
        })
        .catch(function () {
          if (itemEl) itemEl.classList.remove('is-updating');
          toast(strings.cartError, 'error');
        })
        .finally(function () {
          self.pending = false;
          self.setBusy(false);
          var next = self.queued;
          self.queued = null;
          if (next) {
            var control = document.querySelector('[data-cart-item] [data-line-key="' + String(next.key).replace(/"/g, '\\"') + '"]');
            self.change(next.key, next.quantity, control ? control.closest('[data-cart-item]') : null);
          }
        });
    },

    updateNote: debounce(function (note) {
      fetch(routes.cartUpdate + '.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ note: note })
      }).catch(function () {});
    }, 500),

    renderSections: function (sections) {
      if (!sections) return;
      // Remember which control had focus so it can be restored after re-rendering
      var active = document.activeElement;
      var focusContainer = active && active.closest ? active.closest('[data-cart-drawer-content], [data-cart-page]') : null;
      var focusIndex = -1;
      if (focusContainer) focusIndex = Array.prototype.indexOf.call(focusContainer.querySelectorAll(FOCUSABLE), active);

      var drawerHTML = sections['cart-drawer'];
      if (drawerHTML) {
        var doc = parseHTML(drawerHTML);
        var source = doc.querySelector('[data-cart-drawer-content]');
        var target = document.querySelector('[data-cart-drawer-content]');
        if (source && target) target.innerHTML = source.innerHTML;
        var countSource = doc.querySelector('[data-cart-count]');
        if (countSource) this.updateCount(countSource.getAttribute('data-cart-count'));
      }
      var page = document.querySelector('[data-cart-page]');
      if (page) {
        var id = page.getAttribute('data-section-id');
        if (sections[id]) {
          var pageDoc = parseHTML(sections[id]);
          var pageSource = pageDoc.querySelector('[data-cart-page]');
          // Keep an order note the shopper is still typing (its save may not have finished)
          var noteEl = page.querySelector('[data-cart-note]');
          var noteValue = noteEl ? noteEl.value : null;
          if (pageSource) page.innerHTML = pageSource.innerHTML;
          var newNote = page.querySelector('[data-cart-note]');
          if (newNote && noteValue !== null) newNote.value = noteValue;
        }
      }
      if (focusContainer && focusIndex > -1 && document.contains(focusContainer)) {
        var nodes = focusContainer.querySelectorAll(FOCUSABLE);
        if (nodes.length) nodes[Math.min(focusIndex, nodes.length - 1)].focus();
      }
    },

    updateCount: function (count) {
      document.querySelectorAll('[data-cart-count-bubble]').forEach(function (bubble) {
        var changed = bubble.textContent.trim() !== String(count);
        bubble.textContent = count;
        bubble.setAttribute('data-count', count);
        if (changed) {
          bubble.classList.remove('is-bumped');
          void bubble.offsetWidth;
          bubble.classList.add('is-bumped');
        }
      });
      document.querySelectorAll('[data-cart-count-label]').forEach(function (label) {
        var text = label.getAttribute(count === '1' ? 'data-label-one' : 'data-label-other');
        if (text) label.textContent = text.replace('[count]', count);
      });
    }
  };

  function initCart() {
    // Product forms (product page + quick add buttons)
    document.addEventListener('submit', function (e) {
      var form = e.target.closest('form[data-product-form]');
      if (!form) return;
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var button = e.submitter && e.submitter.name !== 'checkout' ? e.submitter : form.querySelector('[type="submit"]');
      if (button && button.getAttribute('aria-disabled') === 'true') return;
      Cart.add(form, button);
    });

    // Cart icon opens drawer
    document.addEventListener('click', function (e) {
      var toggle = e.target.closest('[data-cart-toggle]');
      if (!toggle || config.cartType === 'page' || document.querySelector('[data-cart-page]')) return;
      var drawer = getDrawer(Cart.drawerId);
      if (!drawer) return;
      e.preventDefault();
      drawer.open(toggle);
    });

    // Quantity buttons & remove in cart (drawer + page)
    document.addEventListener('click', function (e) {
      var remove = e.target.closest('[data-line-remove]');
      if (remove) {
        e.preventDefault();
        Cart.change(remove.getAttribute('data-line-key'), 0, remove.closest('[data-cart-item]'));
      }
    });

    document.addEventListener('change', function (e) {
      var input = e.target.closest && e.target.closest('input[data-line-key]');
      if (!input) return;
      clearTimeout(input._qtyTimer);
      input._qtyTimer = setTimeout(function () {
        var qty = Math.max(0, parseInt(input.value, 10) || 0);
        Cart.change(input.getAttribute('data-line-key'), qty, input.closest('[data-cart-item]'));
      }, 350);
    });

    document.addEventListener('input', function (e) {
      if (e.target.matches && e.target.matches('[data-cart-note]')) Cart.updateNote(e.target.value);
    });
  }

  /* ------------------------------------------------------------------
     Quantity steppers
     ------------------------------------------------------------------ */
  function initQuantity() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-qty-step]');
      if (!btn) return;
      e.preventDefault();
      var wrapper = btn.closest('[data-quantity]');
      var input = wrapper && wrapper.querySelector('input');
      if (!input) return;
      var step = parseInt(btn.getAttribute('data-qty-step'), 10);
      var min = parseInt(input.getAttribute('min'), 10);
      if (isNaN(min)) min = 0;
      var max = parseInt(input.getAttribute('max'), 10);
      var next = (parseInt(input.value, 10) || 0) + step;
      if (next < min) next = min;
      if (!isNaN(max) && next > max) next = max;
      if (String(next) === input.value) return;
      input.value = next;
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
  }

  /* ------------------------------------------------------------------
     Product page: variant picker + gallery
     ------------------------------------------------------------------ */
  function ProductForm(root) {
    this.root = root;
    var json = root.querySelector('[data-variants-json]');
    if (!json) return;
    try {
      this.variants = JSON.parse(json.textContent);
    } catch (err) {
      return;
    }
    this.form = root.querySelector('form[data-product-form]');
    this.idInput = this.form && this.form.querySelector('input[name="id"]');
    this.picker = root.querySelector('[data-variant-picker]');
    this.lowStock = parseInt(root.getAttribute('data-low-stock'), 10) || 0;
    this.updateUrl = root.getAttribute('data-update-url') === 'true';
    var self = this;
    if (this.picker) {
      this.picker.addEventListener('change', function () {
        self.onChange();
      });
      this.updateOptionStates(this.selectedOptions());
    }
  }

  ProductForm.prototype.selectedOptions = function () {
    var values = [];
    this.picker.querySelectorAll('[data-option-index]').forEach(function (group) {
      var index = parseInt(group.getAttribute('data-option-index'), 10);
      var checked = group.querySelector('input:checked');
      var select = group.querySelector('select');
      values[index] = checked ? checked.value : select ? select.value : null;
      var label = group.querySelector('[data-selected-value]');
      if (label) label.textContent = values[index] || '';
    });
    return values;
  };

  ProductForm.prototype.findVariant = function (options) {
    return (
      this.variants.find(function (v) {
        return v.options.every(function (value, i) {
          return value === options[i];
        });
      }) || null
    );
  };

  ProductForm.prototype.updateOptionStates = function (selected) {
    var variants = this.variants;
    this.picker.querySelectorAll('[data-option-index]').forEach(function (group) {
      var index = parseInt(group.getAttribute('data-option-index'), 10);
      group.querySelectorAll('input[type="radio"], option').forEach(function (input) {
        var candidate = selected.slice();
        candidate[index] = input.value;
        var available = variants.some(function (v) {
          return (
            v.available &&
            v.options.every(function (value, i) {
              return i > index ? true : value === candidate[i];
            })
          );
        });
        if (input.tagName === 'OPTION') {
          input.textContent = input.value + (available ? '' : ' — ' + strings.soldOut);
        } else {
          input.classList.toggle('is-unavailable', !available);
          var label = input.nextElementSibling;
          var sr = label && label.querySelector('[data-unavailable-sr]');
          if (!available && label && !sr) {
            var span = document.createElement('span');
            span.className = 'visually-hidden';
            span.setAttribute('data-unavailable-sr', '');
            span.textContent = ' — ' + strings.soldOut;
            label.appendChild(span);
          } else if (available && sr) {
            sr.remove();
          }
        }
      });
    });
  };

  ProductForm.prototype.onChange = function () {
    var options = this.selectedOptions();
    var variant = this.findVariant(options);
    this.updateOptionStates(options);
    this.render(variant);
    if (variant) {
      if (this.idInput) {
        this.idInput.value = variant.id;
        this.idInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
      if (this.updateUrl && window.history.replaceState) {
        var url = new URL(window.location.href);
        url.searchParams.set('variant', variant.id);
        window.history.replaceState({}, '', url.toString());
      }
      if (variant.featured_media_id) {
        var gallery = document.querySelector('[data-product-gallery]');
        if (gallery && gallery._gallery) gallery._gallery.goTo(variant.featured_media_id);
      }
    }
  };

  ProductForm.prototype.render = function (variant) {
    var root = this.root;
    var button = root.querySelector('[data-add-button]');
    var buttonText = root.querySelector('[data-add-button-text]');
    var price = root.querySelector('[data-price]');
    var stock = root.querySelector('[data-stock]');
    var sku = root.querySelector('[data-sku]');
    var buyNow = root.querySelector('[data-buy-now]');

    if (!variant) {
      if (button) button.disabled = true;
      if (buttonText) buttonText.textContent = strings.unavailable;
      if (stock) {
        stock.className = 'stock stock--out';
        stock.textContent = strings.unavailable;
        stock.hidden = false;
      }
      if (buyNow) buyNow.hidden = true;
      return;
    }

    if (button) button.disabled = !variant.available;
    if (buttonText) buttonText.textContent = variant.available ? strings.addToCart : strings.soldOut;
    if (buyNow) buyNow.hidden = !variant.available;

    if (price) {
      var onSale = variant.compare_at_price && variant.compare_at_price > variant.price;
      var html = '';
      if (onSale) {
        html +=
          '<span class="visually-hidden">' + (strings.salePrice || '') + '</span>' +
          '<span class="price-item price-item--sale">' + formatMoney(variant.price) + '</span>' +
          '<span class="visually-hidden">' + (strings.regularPrice || '') + '</span>' +
          '<s class="price-item price-item--compare">' + formatMoney(variant.compare_at_price) + '</s>';
        var percent = Math.round(((variant.compare_at_price - variant.price) * 100) / variant.compare_at_price);
        if (percent > 0 && strings.percentOff) {
          html += '<span class="badge badge--sale">' + strings.percentOff.replace('[percent]', percent) + '</span>';
        }
      } else {
        html += '<span class="price-item price-item--regular">' + formatMoney(variant.price) + '</span>';
      }
      if (variant.unit_price) {
        html +=
          '<span class="price__unit">' + formatMoney(variant.unit_price) + ' / ' + (variant.unit_price_reference || '') + '</span>';
      }
      price.innerHTML = '<div class="price price--large">' + html + '</div>';
    }

    if (stock) {
      stock.hidden = false;
      if (!variant.available) {
        stock.className = 'stock stock--out';
        stock.textContent = strings.soldOut;
      } else if (variant.inventory != null && this.lowStock > 0 && variant.inventory > 0 && variant.inventory <= this.lowStock) {
        stock.className = 'stock stock--low';
        stock.textContent = (strings.lowStock || '').replace('[count]', variant.inventory);
      } else if (variant.in_stock) {
        stock.className = 'stock stock--in';
        stock.textContent = strings.inStock;
      } else {
        stock.className = 'stock';
        stock.textContent = '';
        stock.hidden = true;
      }
    }

    if (sku) {
      sku.hidden = !variant.sku;
      var skuValue = sku.querySelector('[data-sku-value]');
      if (skuValue) skuValue.textContent = variant.sku || '';
    }

    var qty = root.querySelector('[data-quantity] input');
    if (qty) {
      if (variant.inventory != null && variant.inventory > 0) qty.setAttribute('max', variant.inventory);
      else qty.removeAttribute('max');
    }
  };

  function Gallery(root) {
    this.root = root;
    this.track = root.querySelector('[data-gallery-track]');
    this.thumbs = Array.prototype.slice.call(root.querySelectorAll('[data-gallery-thumb]'));
    this.slides = Array.prototype.slice.call(root.querySelectorAll('[data-media-id]'));
    if (!this.track || !this.slides.length) return;
    var self = this;
    root._gallery = this;

    this.thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        self.goTo(thumb.getAttribute('data-gallery-thumb'));
      });
    });

    root.querySelectorAll('[data-gallery-step]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var step = parseInt(btn.getAttribute('data-gallery-step'), 10);
        var index = self.currentIndex() + step;
        if (index < 0) index = self.slides.length - 1;
        if (index >= self.slides.length) index = 0;
        self.goTo(self.slides[index].getAttribute('data-media-id'));
      });
    });

    this.track.addEventListener(
      'scroll',
      debounce(function () {
        self.setActive(self.slides[self.currentIndex()].getAttribute('data-media-id'));
      }, 80),
      { passive: true }
    );
  }

  Gallery.prototype.currentIndex = function () {
    var width = this.track.clientWidth || 1;
    var index = Math.round(this.track.scrollLeft / width);
    return Math.max(0, Math.min(this.slides.length - 1, index));
  };

  Gallery.prototype.goTo = function (mediaId) {
    var slide = this.root.querySelector('[data-media-id="' + mediaId + '"]');
    if (!slide) return;
    var behavior = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
    this.track.scrollTo({ left: slide.offsetLeft - this.track.offsetLeft, behavior: behavior });
    this.setActive(mediaId);
  };

  Gallery.prototype.setActive = function (mediaId) {
    this.thumbs.forEach(function (thumb) {
      var active = thumb.getAttribute('data-gallery-thumb') === String(mediaId);
      thumb.classList.toggle('is-active', active);
      thumb.setAttribute('aria-current', active ? 'true' : 'false');
    });
    var index = this.slides.findIndex(function (slide) {
      return slide.getAttribute('data-media-id') === String(mediaId);
    });
    if (index < 0) index = this.currentIndex();
    var counter = this.root.querySelector('[data-gallery-counter]');
    if (counter) counter.textContent = index + 1 + ' / ' + this.slides.length;
  };

  /* ------------------------------------------------------------------
     Collection & search filters
     ------------------------------------------------------------------ */
  function initFacets() {
    var form = document.querySelector('[data-facets-form]');
    if (!form || form._facetsInit) return;
    form._facetsInit = true;
    var desktop = window.matchMedia('(min-width: 990px)');
    var results = document.querySelector('[data-facets-results]');
    var jsDisabled = [];
    var FOCUS_KEY = 'anjumFacetFocus';

    // Put focus back on the control that reloaded the page, so keyboard users keep their place
    try {
      var lastId = sessionStorage.getItem(FOCUS_KEY);
      if (lastId) {
        sessionStorage.removeItem(FOCUS_KEY);
        var last = document.getElementById(lastId);
        if (last && last.offsetParent !== null) last.focus();
      }
    } catch (err) {}

    var submit = function (source) {
      try {
        if (source && source.id) sessionStorage.setItem(FOCUS_KEY, source.id);
      } catch (err) {}
      form.querySelectorAll('input, select').forEach(function (input) {
        if ((input.type === 'number' || input.type === 'text' || input.tagName === 'SELECT') && input.value === '' && !input.disabled) {
          input.disabled = true;
          jsDisabled.push(input);
        }
      });
      if (results) results.classList.add('is-loading');
      form.submit();
    };

    // Returning with the back button restores the page from cache: undo the submit state
    window.addEventListener('pageshow', function (e) {
      if (!e.persisted) return;
      jsDisabled.forEach(function (input) {
        input.disabled = false;
      });
      jsDisabled = [];
      if (results) results.classList.remove('is-loading');
    });

    // Close the mobile filter drawer if the window grows to the desktop layout
    var onMq = function (e) {
      if (e.matches && openDrawer && openDrawer.el.id === 'FacetsDrawer') openDrawer.close(true);
    };
    if (desktop.addEventListener) desktop.addEventListener('change', onMq);
    else if (desktop.addListener) desktop.addListener(onMq);

    form.addEventListener('change', function (e) {
      var target = e.target;
      if (target.matches('[data-sort]') || target.matches('input[type="number"]')) return;
      if (desktop.matches) submit(target);
    });

    // Price range: apply when focus leaves both fields, not after the first one
    form.querySelectorAll('.facet__price').forEach(function (group) {
      var dirty = false;
      group.addEventListener('change', function () {
        dirty = true;
      });
      group.addEventListener('focusout', function (e) {
        if (desktop.matches && dirty && !group.contains(e.relatedTarget)) {
          dirty = false;
          submit(e.target);
        }
      });
    });

    form.querySelectorAll('input[type="number"]').forEach(function (input) {
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          submit(input);
        }
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      submit();
    });

    // Sorting: apply at once for mouse/touch, but wait for Enter or blur after arrow-key browsing
    var sorts = Array.prototype.slice.call(form.querySelectorAll('select[data-sort]')).concat(
      Array.prototype.slice.call(document.querySelectorAll('[data-sort-external]'))
    );
    sorts.forEach(function (select) {
      var initial = select.value;
      var keyed = false;
      var apply = function () {
        keyed = false;
        if (select.value === initial) return;
        var hidden = form.querySelector('input[data-sort]');
        if (hidden) hidden.value = select.value;
        submit(select);
      };
      select.addEventListener('pointerdown', function () {
        keyed = false;
      });
      select.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          apply();
        } else if (e.key !== 'Tab' && e.key !== 'Shift' && e.key !== 'Escape') {
          keyed = true;
        }
      });
      select.addEventListener('change', function () {
        if (!keyed) apply();
      });
      select.addEventListener('blur', function () {
        if (keyed) apply();
      });
    });
  }

  /* ------------------------------------------------------------------
     Product recommendations
     ------------------------------------------------------------------ */
  function initRecommendations(scope) {
    (scope || document).querySelectorAll('[data-recommendations]').forEach(function (el) {
      var load = function () {
        fetch(el.getAttribute('data-url'))
          .then(function (r) {
            return r.text();
          })
          .then(function (text) {
            var doc = parseHTML(text);
            var source = doc.querySelector('[data-recommendations]');
            if (source && source.querySelector('[data-product-card]')) {
              el.innerHTML = source.innerHTML;
              el.hidden = false;
              initSliders(el);
            } else {
              var section = el.closest('.shopify-section');
              if (section) section.hidden = true;
            }
          })
          .catch(function () {
            var section = el.closest('.shopify-section');
            if (section) section.hidden = true;
          });
      };
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(
          function (entries) {
            if (entries[0].isIntersecting) {
              io.disconnect();
              load();
            }
          },
          { rootMargin: '0px 0px 400px 0px' }
        );
        io.observe(el);
      } else {
        load();
      }
    });
  }

  /* ------------------------------------------------------------------
     Slider prev/next controls (product rails)
     ------------------------------------------------------------------ */
  function initSliders(scope) {
    (scope || document).querySelectorAll('[data-slider]').forEach(function (wrapper) {
      if (wrapper._sliderInit) return;
      wrapper._sliderInit = true;
      var track = wrapper.querySelector('[data-slider-track]');
      var prev = wrapper.querySelector('[data-slider-prev]');
      var next = wrapper.querySelector('[data-slider-next]');
      if (!track || !prev || !next) return;
      var update = function () {
        prev.disabled = track.scrollLeft <= 4;
        next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      };
      var step = function (dir) {
        var item = track.firstElementChild;
        var amount = item ? item.getBoundingClientRect().width + 20 : track.clientWidth * 0.8;
        track.scrollBy({ left: dir * amount, behavior: 'smooth' });
      };
      prev.addEventListener('click', function () { step(-1); });
      next.addEventListener('click', function () { step(1); });
      track.addEventListener('scroll', debounce(update, 60), { passive: true });
      window.addEventListener('resize', debounce(update, 150));
      update();
    });
  }

  /* ------------------------------------------------------------------
     Scroll reveal animations
     ------------------------------------------------------------------ */
  var REVEAL_SELECTOR = [
    '.section-header',
    '.product-grid > li',
    '[data-slider-track] > li',
    '.category-list > li',
    '.collection-list-grid > li',
    '.features > *',
    '.promo',
    '.rich-text',
    '.article-grid > li',
    '.collection-hero__inner'
  ].join(',');
  var revealObserver = null;

  function initReveal(scope) {
    if (!document.body.hasAttribute('data-animate')) return;
    if (window.Shopify && window.Shopify.designMode) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) return;
    if (!revealObserver) {
      revealObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('is-revealed');
            revealObserver.unobserve(entry.target);
          });
        },
        { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
      );
    }
    var viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    (scope || document).querySelectorAll(REVEAL_SELECTOR).forEach(function (el) {
      if (el._reveal) return;
      el._reveal = true;
      // Leave anything already on screen alone so the first view never flickers
      if (el.getBoundingClientRect().top < viewportHeight) return;
      var index = 0;
      var sibling = el.previousElementSibling;
      while (sibling && index < 5) {
        index++;
        sibling = sibling.previousElementSibling;
      }
      el.style.setProperty('--reveal-index', index);
      el.classList.add('reveal');
      revealObserver.observe(el);
    });
  }

  /* ------------------------------------------------------------------
     Copy-to-clipboard (gift card)
     ------------------------------------------------------------------ */
  function initCopy() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-copy]');
      if (!btn || !navigator.clipboard) return;
      navigator.clipboard.writeText(btn.getAttribute('data-copy')).then(function () {
        var original = btn.textContent;
        btn.textContent = btn.getAttribute('data-copied') || original;
        setTimeout(function () {
          btn.textContent = original;
        }, 2000);
      });
    });
  }

  /* ------------------------------------------------------------------
     Init
     ------------------------------------------------------------------ */
  function init() {
    ensureToast();
    initHeader();
    initAnnouncements();
    document.querySelectorAll('[data-predictive-search]').forEach(function (form) {
      new PredictiveSearch(form);
    });
    initCart();
    initQuantity();
    document.querySelectorAll('[data-product]').forEach(function (root) {
      new ProductForm(root);
    });
    document.querySelectorAll('[data-product-gallery]').forEach(function (root) {
      new Gallery(root);
    });
    initFacets();
    initRecommendations();
    initSliders();
    initCopy();
    initReveal();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // Re-initialise when sections are edited in the theme editor
  document.addEventListener('shopify:section:load', function (e) {
    initSliders(e.target);
    initAnnouncements(e.target);
    initRecommendations(e.target);
    if (e.target.querySelector('[data-facets-form]')) initFacets();
    e.target.querySelectorAll('[data-product]').forEach(function (root) {
      new ProductForm(root);
    });
    e.target.querySelectorAll('[data-product-gallery]').forEach(function (root) {
      new Gallery(root);
    });
    e.target.querySelectorAll('[data-predictive-search]').forEach(function (form) {
      new PredictiveSearch(form);
    });
  });

  document.addEventListener('shopify:section:unload', function (e) {
    if (openDrawer && e.target.contains(openDrawer.el)) {
      document.body.classList.remove('overflow-hidden');
      openDrawer = null;
    }
    e.target.querySelectorAll('[data-announcement]').forEach(function (bar) {
      clearInterval(bar._timer);
    });
  });

  window.AnjumMart.formatMoney = formatMoney;
  window.AnjumMart.cart = Cart;
})();
