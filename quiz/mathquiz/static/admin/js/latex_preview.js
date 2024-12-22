document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.querySelector("#id_text"); // 問題文フィールドを取得
    if (inputField) {
        // プレビュー用のdivを作成
        const preview = document.createElement("div");
        preview.classList.add("mathjax-preview");
        preview.style.marginTop = "10px"; // プレビューのスタイル設定
        inputField.parentNode.insertBefore(preview, inputField.nextSibling);

        // 入力イベントをリッスンしてプレビューを更新
        inputField.addEventListener("input", function () {
            preview.innerHTML = `\\(${inputField.value}\\)`; // MathJax形式の数式をプレビューに表示
            MathJax.typesetPromise([preview]); // MathJaxを再レンダリング
        });
    }
});
