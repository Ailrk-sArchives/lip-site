// clickthorugh div for article cards
$(".click-card").click(function () {
  window.location = $(this).find("a").attr("href");
  return false;
});
