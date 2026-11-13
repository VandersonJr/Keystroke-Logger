// Alterna a visibilidade da senha (arquivo externo por causa da CSP do painel).
(() => {
  const input = document.getElementById("password");
  const btn = document.getElementById("toggle-pw");
  if (!input || !btn) return;
  btn.addEventListener("click", () => {
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    btn.setAttribute("aria-pressed", String(show));
    btn.setAttribute("aria-label", show ? "Ocultar senha" : "Mostrar senha");
    btn.classList.toggle("on", show);
  });
})();