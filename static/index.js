window.addEventListener("load", () => {
  const loader = document.querySelector(".loader");

  loader.classList.add("loader--hidden");

  loader.addEventListener("transitionend", () => {
    document.body.removeChild(loader);
  });
});


window.scrollTo(0,500);

    function copyText(i) {
        var Text = document.getElementById("outputtext"+i).textContent;
        navigator.clipboard.writeText(Text);
    };
