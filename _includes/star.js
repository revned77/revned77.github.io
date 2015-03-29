      var now = new Date().getTime();
      e = document.querySelectorAll(".new");
      for(i = 0; i < e.length; i++) {
        if (now - Date.parse(e[i].parentNode.textContent) < 15768000000) {
          e[i].innerHTML = "★";
        }
      }