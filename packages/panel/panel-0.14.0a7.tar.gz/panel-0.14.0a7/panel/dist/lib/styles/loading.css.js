const css = `
.bk.pn-loading:before {
  position: absolute;
  height: 100%;
  width: 100%;
  content: '';
  z-index: 1000;
  background-color: rgb(255,255,255,0.50);
  border-color: lightgray;
  background-repeat: no-repeat;
  background-position: center;
  background-size: auto 50%;
  border-width: 1px;
  cursor: progress;
}
.bk.pn-loading.arcs:hover:before {
  cursor: progress;
}
`;
export default css;
