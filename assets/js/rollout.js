var acc = document.getElementsByClassName("ep-description");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    // var panel = this.nextElementSibling;
    // if (panel.style.maxHeight) {
    //   panel.style.maxHeight = null;
    // } else {
    //   panel.style.maxHeight = panel.scrollHeight + "px";
    // }
    this.style.overflowY = 'visible';
    this.style.whitespace = 'normal';
  });
}