function openNav() {
    document.getElementById("sidebar").style.left = "0";
    document.getElementById("global-blur").style.opacity = 1;
  }

  function closeNav() {
    document.getElementById("sidebar").style.left = "-200px";
    document.getElementById("global-blur").style.opacity = 0;
  }