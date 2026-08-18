(function () {
  "use strict";

  function escapeHtml(s) {
    return s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // Tiny, dependency-free Markdown-subset renderer for the admin preview.
  // All input is HTML-escaped first, so the preview can never execute
  // injected markup (XSS-safe).
  function renderMarkdown(src) {
    var lines = src.replace(/\r\n?/g, "\n").split("\n");
    var html = [];
    var i = 0;
    var inCode = false;
    var codeBuf = [];
    var listOpen = false;

    function flushCode() {
      if (codeBuf.length) {
        html.push("<pre><code>" + escapeHtml(codeBuf.join("\n")) + "</code></pre>");
        codeBuf = [];
      }
    }

    function closeList() {
      if (listOpen) {
        html.push("</ul>");
        listOpen = false;
      }
    }

    function inline(text) {
      var t = escapeHtml(text);
      t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
      t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
      t = t.replace(/\*([^*]+)\*/g, "<em>$1</em>");
      t = t.replace(
        /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,
        '<a href="$2" rel="noopener noreferrer">$1</a>'
      );
      return t;
    }

    for (; i < lines.length; i++) {
      var line = lines[i];
      if (/^```/.test(line)) {
        if (inCode) {
          flushCode();
          inCode = false;
        } else {
          closeList();
          flushCode();
          inCode = true;
        }
        continue;
      }
      if (inCode) {
        codeBuf.push(line);
        continue;
      }
      var h = line.match(/^(#{1,6})\s+(.*)$/);
      if (h) {
        closeList();
        var n = h[1].length;
        html.push("<h" + n + ">" + inline(h[2]) + "</h" + n + ">");
        continue;
      }
      if (/^\s*([-*_])\s*$/.test(line) && line.trim().length <= 3) {
        closeList();
        html.push("<hr>");
        continue;
      }
      var li = line.match(/^\s*[-*+]\s+(.*)$/);
      if (li) {
        if (!listOpen) {
          listOpen = true;
          html.push("<ul>");
        }
        html.push("<li>" + inline(li[1]) + "</li>");
        continue;
      }
      closeList();
      if (line.trim() === "") {
        continue;
      }
      html.push("<p>" + inline(line) + "</p>");
    }
    if (inCode) {
      flushCode();
    }
    closeList();
    return html.join("");
  }

  function debounce(fn, ms) {
    var t;
    return function () {
      var args = arguments;
      var ctx = this;
      clearTimeout(t);
      t = setTimeout(function () {
        fn.apply(ctx, args);
      }, ms);
    };
  }

  function bindWidget(widget) {
    var ta = widget.querySelector("textarea");
    var out = widget.querySelector(".markdown-preview");
    if (!ta || !out) {
      return;
    }
    var update = function () {
      out.innerHTML = ta.value.trim()
        ? renderMarkdown(ta.value)
        : "<em>Preview…</em>";
    };
    ta.addEventListener("input", debounce(update, 150));
    update();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".markdown-preview-widget").forEach(bindWidget);
  });
})();
