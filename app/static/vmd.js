// clickthorugh div for article cards
$(".card").click(function () {
  window.location = $(this).find("a").attr("href");
  return false;
});
