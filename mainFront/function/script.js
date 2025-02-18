document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("calculation-form");
  const downloadSection = document.querySelector(".download");
  const loadingIndicator = document.querySelector(".loading-indicator");
  const numberInput = document.getElementById("number-of-arg");
  const donationButton = document.querySelector(".fa-hand-holding-dollar");
  const modal = document.querySelector(".modal-overlay");
  const closeButton = document.querySelector(".modal-close");
  const ratioOptions = document.querySelectorAll(".ratio-option");
  const numberArgWrapper = document.getElementById("number-arg-wrapper");
  const languageToggle = document.getElementById("language-toggle");
  const languageDropdown = document.querySelector(".language-dropdown");
  const elementalBasis = document.getElementById("elemental-basis");
  const numberInputWrapper = document.getElementById("number-input-wrapper");
  const numberInputField = document.getElementById("number-input");
  let fieldCounter = 1;
  const infoButton = document.querySelector(".fa-circle-info");
  const faq = document.querySelector(".faq");
  const faqCloseButton = document.querySelector(".faq-close");

  const openFaq = () => {
    faq.classList.add("show");
  };

  const closeFaq = () => {
    faq.classList.remove("show");
  };

  infoButton.addEventListener("click", openFaq);
  faqCloseButton.addEventListener("click", closeFaq);

  faq.addEventListener("click", (e) => {
    if (e.target === faq) {
      closeFaq();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && faq.classList.contains("show")) {
      closeFaq();
    }
  });

  languageToggle.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    languageDropdown.classList.toggle("show");
  });

  document.addEventListener("click", (e) => {
    if (!languageToggle.contains(e.target)) {
      languageDropdown.classList.remove("show");
    }
  });

  numberInputField.value = "1/1";

  numberInputField.addEventListener("input", (e) => {
    let value = e.target.value.replace(/[^0-9/]/g, "");
    if (value.length > 3) value = value.slice(0, 3);
    if (value[1] !== "/") value = value[0] + "/" + (value[1] || "");
    e.target.value = value;
  });

  numberInputField.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" && numberInputField.selectionStart === 2) {
      e.preventDefault();
    }
  });

  elementalBasis.addEventListener("change", () => {
    numberInputWrapper.classList.remove("hidden");
  });

  ratioOptions.forEach((option) => {
    option.addEventListener("click", () => {
      ratioOptions.forEach((btn) => btn.classList.remove("active"));
      option.classList.add("active");
      numberArgWrapper.classList.toggle(
        "hidden",
        option.dataset.mode === "expression"
      );
    });
  });

  const validateFunctionInput = (input) => {
    const isExpressionMode = document
      .querySelector('.ratio-option[data-mode="expression"]')
      .classList.contains("active");
    input.value = isExpressionMode
      ? input.value.replace(/[^a-zA-Z0-9!&|]/g, "").slice(0, 52)
      : input.value.replace(/[^0-9,]/g, "").slice(0, 52);
  };

  const createFieldGroup = (counter) => {
    const newGroup = document.createElement("div");
    newGroup.className = "input-group";
    newGroup.innerHTML = `
      <label>F${counter}<input type="text" id="f${counter}" placeholder="Value" required /></label>
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

    const input = newGroup.querySelector(`#f${counter}`);
    input.addEventListener("input", () => validateFunctionInput(input));
    return newGroup;
  };

  const addNewField = () => {
    if (fieldCounter >= 9) return;
    fieldCounter++;

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

    document.querySelectorAll(".input-group").forEach((group, index) => {
      const label = group.querySelector("label");
      const input = group.querySelector("input");
      label.childNodes[0].textContent = `F${index + 1} `;
      input.id = `f${index + 1}`;
    });

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
    group.querySelector(".add-field")?.addEventListener("click", (e) => {
      e.preventDefault();
      addNewField();
    });

    group.querySelector(".remove-field")?.addEventListener("click", (e) => {
      e.preventDefault();
      removeField(e);
    });
  };

  const initialGroup = document.querySelector(".input-group");
  initialGroup.querySelector(".button-group").innerHTML =
    '<button type="button" class="add-field" title="Add field"><i class="fa-solid fa-plus"></i></button>';
  attachFieldListeners(initialGroup);
  initialGroup
    .querySelector("input")
    .addEventListener("input", (e) => validateFunctionInput(e.target));

  const openModal = () => {
    const scrollbarWidth =
      window.innerWidth - document.documentElement.clientWidth;
    document.body.style.paddingRight = `${scrollbarWidth}px`;
    document.body.style.overflow = "hidden";
    modal.classList.add("show");
  };

  const closeModal = () => {
    modal.classList.remove("show");
    document.body.style.paddingRight = "";
    document.body.style.overflow = "";
  };

  donationButton.addEventListener("click", openModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal || e.target.closest(".modal-close")) {
      closeModal();
    }
  });

  closeButton.addEventListener("click", () => closeModal());

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("show")) {
      closeModal();
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const submitButton = document.getElementById("submit-button");
    submitButton.disabled = true;
    loadingIndicator.classList.add("show");
    downloadSection.style.display = "none";
    downloadSection.classList.remove("show");

    try {
      await new Promise((resolve) => setTimeout(resolve, 2000));
      downloadSection.style.display = "block";
      setTimeout(() => downloadSection.classList.add("show"), 50);
    } catch (error) {
      console.error("Processing failed:", error);
    } finally {
      loadingIndicator.classList.remove("show");
      submitButton.disabled = false;
    }
  });

  const themeToggle = document.querySelector(".fa-toggle-off");
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    themeToggle.classList.toggle("fa-toggle-off");
    themeToggle.classList.toggle("fa-toggle-on");
  });

  window.copyToClipboard = function (elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    const button = element.nextElementSibling;

    navigator.clipboard.writeText(text).then(() => {
      const icon = button.querySelector("i");
      icon.classList.remove("fa-copy");
      icon.classList.add("fa-check");
      button.classList.add("copied");

      setTimeout(() => {
        icon.classList.remove("fa-check");
        icon.classList.add("fa-copy");
        button.classList.remove("copied");
      }, 2000);
    });
  };
  document.querySelectorAll("details").forEach((details) => {
    details.addEventListener("toggle", (event) => {
      if (event.target.open) {
        event.target.style.transition = "max-height 0.3s ease-in-out";
      }
    });
  });
});
