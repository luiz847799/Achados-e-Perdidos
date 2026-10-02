document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("image");
  const fileName = document.getElementById("file-name");
  if (fileInput && fileName) {
    fileInput.addEventListener("change", () => {
      fileName.textContent = fileInput.files.length ? fileInput.files[0].name : "Nenhuma imagem selecionada";
    });
  }

  document.querySelectorAll("[data-confirm]").forEach((button) => {
    button.closest("form").addEventListener("submit", (event) => {
      if (!window.confirm(button.dataset.confirm)) event.preventDefault();
    });
  });

  const form = document.getElementById("item-form");
  if (form) {
    form.addEventListener("submit", (event) => {
      const image = document.getElementById("image");
      if (image && image.files.length && image.files[0].size > 5 * 1024 * 1024) {
        event.preventDefault();
        alert("A imagem deve ter no máximo 5 MB.");
      }
    });
  }
});
