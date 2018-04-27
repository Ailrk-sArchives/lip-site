// clickthorugh div for article cards
$(".click-card").click(function () {
  window.location = $(this).find("a").attr("href");
  return false;
});

// upload articles
$("#upload-article-file").click(function () {
  var file = document.getElementById("article-file").files[0];
  var reader = new FileReader();

  reader.onload = function (e) {
    var editor = document.getElementById("article-content-editor");
    editor.value = e.target.result;
  }

  reader.readAsText(file);
});

// select article category  (editor)
$(".editor-cate-drop").click(function () {
  $("#article-cate-editor").val($(this).text());
});
