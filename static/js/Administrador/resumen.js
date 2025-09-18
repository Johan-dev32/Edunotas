document.getElementById("resumenForm").addEventListener("submit", (e) => {
  e.preventDefault();

  const actividades = document.getElementById("actividades").value.split(",");
  const problemas = document.getElementById("problemas").value.split(",");

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  // Título
  doc.setFontSize(18);
  doc.text("Resumen Semanal", 14, 20);

  // Actividades en tabla
  doc.autoTable({
    startY: 30,
    head: [["Actividades realizadas"]],
    body: actividades
      .filter((a) => a.trim() !== "")
      .map((a) => [a.trim()]),
  });

  // Problemas en tabla
  doc.autoTable({
    startY: doc.lastAutoTable.finalY + 10,
    head: [["Problemas encontrados"]],
    body: problemas
      .filter((p) => p.trim() !== "")
      .map((p) => [p.trim()]),
  });

  // Descargar PDF
  doc.save("resumen_semanal.pdf");
});
