document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("calculation-form");
  const downloadSection = document.querySelector(".download");
  const loadingIndicator = document.querySelector(".loading-indicator");
  let fieldCounter = 1;

  // Initially hide download section
  downloadSection.style.display = "none";

  const createFieldGroup = (counter) => {
    const newGroup = document.createElement("div");
    newGroup.className = "input-group";
    newGroup.innerHTML = `
        <div class="input-wrapper">
          <label>
            F${counter}
            <input type="text" id="f${counter}" placeholder="Value" />
          </label>
        </div>
        <div class="button-group">
          ${
            counter === fieldCounter
              ? '<button type="button" class="add-field" title="Add field"><i class="fa-solid fa-plus"></i></button>'
              : ""
          }
          ${
            counter === fieldCounter && counter > 1
              ? '<button type="button" class="remove-field" title="Remove field"><i class="fa-solid fa-minus"></i></button>'
              : ""
          }
        </div>
    `;
    return newGroup;
  };

  const addNewField = () => {
    if (fieldCounter >= 10) return;

    fieldCounter++;
    // Update buttons on the previous last field
    const previousLastGroup = document.querySelector(
      ".input-group:last-of-type"
    );
    previousLastGroup.querySelector(".button-group").innerHTML = "";

    const newGroup = createFieldGroup(fieldCounter);
    form.insertBefore(newGroup, document.getElementById("submit-button"));

    attachFieldListeners(newGroup);
  };

  const removeField = (event) => {
    const group = event.target.closest(".input-group");
    group.remove();
    fieldCounter--;

    // Update all field labels
    document.querySelectorAll(".input-group").forEach((group, index) => {
      const label = group.querySelector("label");
      const input = group.querySelector("input");
      label.childNodes[0].textContent = `F${index + 1} `;
      input.id = `f${index + 1}`;
    });

    // Update buttons on the new last field
    const lastGroup = document.querySelector(".input-group:last-of-type");
    lastGroup.querySelector(".button-group").innerHTML = `
      <button type="button" class="add-field" title="Add field"><i class="fa-solid fa-plus"></i></button>
      ${
        fieldCounter > 1
          ? '<button type="button" class="remove-field" title="Remove field"><i class="fa-solid fa-minus"></i></button>'
          : ""
      }
    `;

    attachFieldListeners(lastGroup);
  };

  const attachFieldListeners = (group) => {
    const addBtn = group.querySelector(".add-field");
    const removeBtn = group.querySelector(".remove-field");

    if (addBtn) {
      addBtn.addEventListener("click", (e) => {
        e.preventDefault();
        addNewField();
      });
    }
    if (removeBtn) {
      removeBtn.addEventListener("click", (e) => {
        e.preventDefault();
        removeField(e);
      });
    }
  };

  // Initial field group setup
  const initialGroup = document.querySelector(".input-group");
  initialGroup.querySelector(".button-group").innerHTML =
    '<button type="button" class="add-field" title="Add field"><i class="fa-solid fa-plus"></i></button>';
  attachFieldListeners(initialGroup);

  // Form submission handling
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Disable submit button and show loading
    const submitButton = document.getElementById("submit-button");
    submitButton.disabled = true;
    loadingIndicator.classList.add("show");
    downloadSection.style.display = "none";
    downloadSection.classList.remove("show");

    try {
      // Simulate processing delay
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Show download section
      downloadSection.style.display = "block";
      setTimeout(() => downloadSection.classList.add("show"), 50);
    } catch (error) {
      console.error("Processing failed:", error);
    } finally {
      // Reset UI state
      loadingIndicator.classList.remove("show");
      submitButton.disabled = false;
    }
  });

  // Theme toggle
  const themeToggle = document.querySelector(".fa-toggle-off");
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    themeToggle.classList.toggle("fa-toggle-off");
    themeToggle.classList.toggle("fa-toggle-on");
  });

  // Tab handling
  const tabs = document.querySelectorAll(".tab");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
    });
  });

  // Language dropdown
  const languageToggle = document.getElementById("language-toggle");
  const languageDropdown = document.getElementById("language-dropdown");

  languageToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    languageDropdown.classList.toggle("show");
  });

  document.addEventListener("click", (e) => {
    if (!languageToggle.contains(e.target)) {
      languageDropdown.classList.remove("show");
    }
  });
});
