      function makeHandler(e) {
        return function() {
          e.className = (e.className == "expanded") ? "" : "expanded";
        };
      }
      var e = document.querySelectorAll("nav > ul > li");
      for(var i = 0; i < e.length; i++) {
        e[i].getElementsByTagName("span")[0].onclick = makeHandler(e[i]);
      }