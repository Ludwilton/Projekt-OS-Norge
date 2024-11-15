window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_main_content: function(...clickedTimes) {
            const contentIds = ["home-content", "norway-content", "new-content"];
            contentIds.forEach(id => {
                document.getElementById(id).style.display = "none";
            });

            const buttons = [
                { id: "home-content", time: clickedTimes[0] },
                { id: "norway-content", time: clickedTimes[1] },
                { id: "new-content", time: clickedTimes[2] }
            ];

            let latestButton = null
            buttons.forEach((button) => {
                if (button.time) {
                    if (!latestButton || button.time > latestButton.time) {
                        latestButton = button;
                    }
                }
            })

            if (latestButton) {
                document.getElementById(latestButton.id).style.display = "";
            }
        }
    }
});
