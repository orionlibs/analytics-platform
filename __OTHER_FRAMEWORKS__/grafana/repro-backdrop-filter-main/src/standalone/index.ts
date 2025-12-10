console.log("Hello, world!");

document.getElementById("open-modal")?.addEventListener("click", () => {
  document.getElementById("modal-container")?.classList.add("open");
});

document.getElementById("close-modal")?.addEventListener("click", () => {
  document.getElementById("modal-container")?.classList.remove("open");
});
