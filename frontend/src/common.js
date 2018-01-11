export default function loadFont() {
  let p = location.pathname.split('/');
  p.pop();
  p = `${p.join('/')}/static/typeface-nanum-barun-gothic/nanumbarungothic.css`;
  const link = document.createElement('link');
  link.href = p;
  link.type = 'text/css';
  link.rel = 'stylesheet';
  document.getElementsByTagName('head')[0].appendChild(link);
}
