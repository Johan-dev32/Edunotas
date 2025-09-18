document.getElementById("resumenForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const actividades = document.getElementById("actividades").value.split(",");
  const problemas = document.getElementById("problemas").value.split(",");

  const res = await fetch("/generar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ actividades, problemas })
  });

  if (!res.ok) {
    alert("Error al generar el PDF");
    return;
  }


  function generarPDF() {
    const element = document.querySelector('.container');
    html2pdf()
      .from(element)
      .set({
        margin: 0.5,
        filename: 'Manual_Administrador_EduNotas.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      })
      .save();
  }


  // Creamos un enlace temporal para descargarlo
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "resumen.pdf"; // Nombre del archivo
  document.body.appendChild(a);
  a.click();

  // Limpiamos
  a.remove();
  window.URL.revokeObjectURL(url);
});

