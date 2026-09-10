const form = document.getElementById("analyzer-form");
const expressionFields = document.getElementById("expression-fields");
const mintermFields = document.getElementById("minterm-fields");
const argsCount = document.getElementById("args-count");
const mintermInfo = document.getElementById("minterm-info");

function getMode() {
    return form.elements.mode.value;
}

function clampNumber(value, min, max, fallback) {
    const parsed = Number.parseInt(value, 10);

    if (Number.isNaN(parsed)) {
        return fallback;
    }

    return Math.min(max, Math.max(min, parsed));
}

function updateMode() {
    const isExpression = getMode() === "expression";
    expressionFields.hidden = !isExpression;
    mintermFields.hidden = isExpression;

    document.querySelectorAll(".mode-option").forEach((option) => {
        option.classList.toggle("active", option.querySelector("input").checked);
    });
}

function updateMintermInfo() {
    const count = clampNumber(argsCount.value, 1, 9, 3);
    argsCount.value = count;
    mintermInfo.dataset.tooltip = `Enter comma-separated integers from 0 to ${Math.pow(2, count) - 1}.`;
}

document.querySelectorAll("input[name='mode']").forEach((radio) => {
    radio.addEventListener("change", updateMode);
});

document.querySelectorAll("[data-step]").forEach((button) => {
    button.addEventListener("click", () => {
        const next = clampNumber(argsCount.value, 1, 9, 3) + Number.parseInt(button.dataset.step, 10);
        argsCount.value = clampNumber(next, 1, 9, 3);
        updateMintermInfo();
    });
});

argsCount.addEventListener("input", updateMintermInfo);

form.addEventListener("submit", (event) => {
    event.preventDefault();
});

updateMode();
updateMintermInfo();
