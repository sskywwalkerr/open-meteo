document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("city-input");
    const suggestionsDiv = document.getElementById("suggestions");

    const GEONAMES_USERNAME = "skywwalker";

    input.addEventListener("input", async (event) => {
        const query = event.target.value.trim();
        if (query.length < 2) {
            suggestionsDiv.innerHTML = "";
            return;
        }
                try {
            const response = await axios.get("http://api.geonames.org/searchJSON", {
                params: {
                    q: query,
                    maxRows: 10,
                    username: GEONAMES_USERNAME,
                    style: "short",
                    featureClass: "P" // Только населённые пункты
                }
            });

            const cities = response.data.geonames.map(city => ({
                name: city.name,
                country: city.countryName
            }));

            suggestionsDiv.innerHTML = "";
            if (cities.length === 0) {
                suggestionsDiv.innerHTML = "<div class='suggestion-item'>Ничего не найдено</div>";
                return;
            }

            cities.forEach(city => {
                const div = document.createElement("div");
                div.className = "suggestion-item";
                div.textContent = `${city.name}, ${city.country}`;
                div.onclick = () => {
                    input.value = city.name;
                    suggestionsDiv.innerHTML = "";
                };
                suggestionsDiv.appendChild(div);
            });
        } catch (error) {
            console.error("Ошибка при получении данных GeoNames:", error);
            suggestionsDiv.innerHTML = "<div class='suggestion-item'>Ошибка загрузки</div>";
        }

    });

    // Скрыть подсказки при клике вне поля ввода
    document.addEventListener("click", (event) => {
        if (!event.target.closest("#city-input")) {
            suggestionsDiv.innerHTML = "";
        }
    });
});