      var now = new Date().getTime();
      e = document.querySelectorAll(".map li:last-child");
      for(i = 0; i < e.length; i++) {
        if (now - Date.parse(e[i].textContent) < 15768000000) {
          e[i].parentNode.parentNode.className += " new";
        }
      }
