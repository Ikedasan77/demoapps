document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.querySelector("#id_text"); // テキストエリアのID
    if (inputField) {
        const preview = document.createElement("div");
        preview.style.marginTop = "10px"; // プレビュー表示の余白
        inputField.parentNode.insertBefore(preview, inputField.nextSibling);

        inputField.addEventListener("input", function () {
            preview.innerHTML = `\\(${inputField.value}\\)`; // LaTeXをプレビュー
            MathJax.typesetPromise(); // MathJaxで再レンダリング
        });
    }
});
