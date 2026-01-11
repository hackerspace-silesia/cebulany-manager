export function downloadFile(response) {
  // the most retard way.
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  const contentDisposition = response.headers['content-disposition'] || '';
  const match = contentDisposition.match(/filename="?([\w_.-]+)"?/);
  const filename = match ? match[1] : 'file.xlsx';
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
}
