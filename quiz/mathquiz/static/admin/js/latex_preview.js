document.addEventListener("DOMContentLoaded", function () {
    // 問題文のプレビュー
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

    // 解説のプレビュー
    const explanationField = document.querySelector("#id_explanation"); // 解説フィールドを取得（適切なIDを確認）
    if (explanationField) {
        // プレビュー用のdivを作成
        const explanationPreview = document.createElement("div");
        explanationPreview.classList.add("mathjax-preview");
        explanationPreview.style.marginTop = "10px"; // プレビューのスタイル設定
        explanationField.parentNode.insertBefore(explanationPreview, explanationField.nextSibling);

        // 入力イベントをリッスンしてプレビューを更新
        explanationField.addEventListener("input", function () {
            explanationPreview.innerHTML = `\\(${explanationField.value}\\)`; // MathJax形式の数式をプレビューに表示
            MathJax.typesetPromise([explanationPreview]); // MathJaxを再レンダリング
        });
    }
});
