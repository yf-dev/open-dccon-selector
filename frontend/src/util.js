export default function getParameterByName(name, url) {
  let tUrl = url;
  if (!tUrl) {
    tUrl = window.location.href;
  }
  const tName = name.replace(/[[\]]/g, '\\$&');
  const regex = new RegExp(`[?&]${tName}(=([^&#]*)|&|#|$)`);
  const results = regex.exec(tUrl);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
