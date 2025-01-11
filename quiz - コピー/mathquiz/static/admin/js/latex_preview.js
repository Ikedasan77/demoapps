document.addEventListener("DOMContentLoaded", function () {
    // 問題文のプレビュー
    const inputField = document.querySelector("#id_text"); // 問題文フィールドを取得
    if (inputField) {
        const preview = document.createElement("div");
        preview.classList.add("mathjax-preview");
        preview.style.marginTop = "10px";
        inputField.parentNode.insertBefore(preview, inputField.nextSibling);

        inputField.addEventListener("input", function () {
            preview.innerHTML = `\\(${inputField.value}\\)`;
            MathJax.typesetPromise([preview]);
        });
    }

    // 解説のプレビュー
    const explanationField = document.querySelector("#id_explanation"); // 解説フィールドを取得
    if (explanationField) {
        const explanationPreview = document.createElement("div");
        explanationPreview.classList.add("mathjax-preview");
        explanationPreview.style.marginTop = "10px";
        explanationField.parentNode.insertBefore(explanationPreview, explanationField.nextSibling);

        explanationField.addEventListener("input", function () {
            explanationPreview.innerHTML = `\\(${explanationField.value}\\)`;
            MathJax.typesetPromise([explanationPreview]);
        });
    }
});
