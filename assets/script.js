window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_main_content: function(homeClickedTime, norwayClickedTime) {
            document.getElementById("home-content").style.display = "none"
            document.getElementById("norway-content").style.display = "none"

            if (!norwayClickedTime || homeClickedTime > norwayClickedTime) {
                document.getElementById("home-content").style.display = ""
            } else if (!homeClickedTime || norwayClickedTime > homeClickedTime) {
                document.getElementById("norway-content").style.display = ""
            }
        }
    }
});