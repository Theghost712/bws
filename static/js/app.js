(function () {
    "use strict";

    function status(message) {
        var el = document.getElementById("action-status") || document.getElementById("designer-status");
        if (el) {
            el.textContent = message;
        }
    }

    function readSource(selector) {
        var el = document.querySelector(selector);
        if (!el) return "";
        return ("value" in el && el.value) ? el.value : (el.textContent || "").trim();
    }

    // --- Theme toggle -----------------------------------------------------
    var THEME_KEY = "paveline-theme";
    var toggle = document.getElementById("theme-toggle");
    function applyTheme(mode) {
        var dark = mode === "dark";
        document.documentElement.setAttribute("data-bs-theme", dark ? "dark" : "light");
        document.body.classList.toggle("dark-mode", dark);
        if (toggle) {
            var icon = toggle.querySelector(".theme-icon");
            if (icon) icon.textContent = dark ? "☀" : "☾";
        }
    }
    if (toggle) {
        toggle.addEventListener("click", function () {
            var next = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
            applyTheme(next);
            try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* storage unavailable */ }
        });
        try {
            var saved = localStorage.getItem(THEME_KEY);
            if (saved) applyTheme(saved);
        } catch (e) { /* ignore */ }
    }

    // --- Copy to clipboard ------------------------------------------------
    document.addEventListener("click", function (event) {
        var copyBtn = event.target.closest("[data-copy-source]");
        if (copyBtn && !copyBtn.hasAttribute("data-web-share")) {
            var text = readSource(copyBtn.getAttribute("data-copy-source"));
            if (!text) return;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(function () {
                    status("Copied. Ready to share!");
                }).catch(function () {
                    status("Copy is unavailable — please select the text manually.");
                });
            } else {
                status("Copy is unavailable — please select the text manually.");
            }
        }

        var shareBtn = event.target.closest("[data-web-share]");
        if (shareBtn) {
            var shareText = readSource(shareBtn.getAttribute("data-copy-source"));
            if (navigator.share && shareText) {
                navigator.share({ title: "A birthday wish for you", text: shareText }).catch(function () {
                    status("Sharing was cancelled. You can still copy the wish.");
                });
            } else if (navigator.clipboard && shareText) {
                navigator.clipboard.writeText(shareText).then(function () {
                    status("Sharing is not supported here, so we copied the wish instead.");
                });
            } else {
                status("Sharing is not supported in this browser. Copy the wish instead.");
            }
        }
    });
})();
