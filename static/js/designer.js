(function () {
    "use strict";

    var form = document.getElementById("card-form");
    if (!form) return;

    var previewImg = document.getElementById("card-preview-img");
    var placeholder = document.getElementById("card-preview-placeholder");
    var statusEl = document.getElementById("designer-status");
    var downloadFlag = document.getElementById("download-flag");
    var renderUrl = form.getAttribute("action");
    var currentUrl = null;
    var timer = null;

    function setStatus(message) {
        if (statusEl) statusEl.textContent = message;
    }

    function refreshPreview() {
        setStatus("Rendering preview…");
        fetch(renderUrl, { method: "POST", body: new FormData(form) })
            .then(function (response) {
                if (!response.ok) {
                    return response.json().then(function (data) {
                        var first = data.errors ? Object.values(data.errors)[0] : null;
                        throw new Error((first && first[0]) || "Please check the form.");
                    });
                }
                return response.blob();
            })
            .then(function (blob) {
                if (currentUrl) URL.revokeObjectURL(currentUrl);
                currentUrl = URL.createObjectURL(blob);
                previewImg.src = currentUrl;
                previewImg.style.display = "block";
                if (placeholder) placeholder.style.display = "none";
                setStatus("Preview updated.");
            })
            .catch(function (error) {
                setStatus(error.message);
            });
    }

    function schedulePreview() {
        clearTimeout(timer);
        timer = setTimeout(refreshPreview, 500);
    }

    var previewBtn = document.getElementById("preview-btn");
    if (previewBtn) previewBtn.addEventListener("click", refreshPreview);

    var downloadBtn = document.getElementById("download-btn");
    if (downloadBtn) {
        downloadBtn.addEventListener("click", function () {
            downloadFlag.value = "1";
            setStatus("Preparing your download…");
            HTMLFormElement.prototype.submit.call(form);
            setTimeout(function () { downloadFlag.value = "0"; }, 1000);
        });
    }

    form.addEventListener("input", schedulePreview);
    form.addEventListener("change", schedulePreview);

    // Initial render.
    refreshPreview();
})();
