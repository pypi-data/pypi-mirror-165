const css = `
.bk.panel-widget-box {
  min-height: 20px;
  background-color: #f5f5f5;
  border: 1px solid #e3e3e3;
  border-radius: 4px;
  -webkit-box-shadow: inset 0 1px 1px rgba(0,0,0,.05);
  box-shadow: inset 0 1px 1px rgba(0,0,0,.05);
  overflow-x: hidden;
  overflow-y: hidden;
}

.scrollable {
  overflow: scroll;
}

progress {
  appearance: none;
  -moz-appearance: none;
  -webkit-appearance: none;
  border: none;
  height: 20px;
  background-color: whiteSmoke;
  border-radius: 3px;
  box-shadow: 0 2px 3px rgba(0,0,0,.5) inset;
  color: royalblue;
  position: relative;
  margin: 0 0 1.5em;
}

progress[value]::-webkit-progress-bar {
  background-color: whiteSmoke;
  border-radius: 3px;
  box-shadow: 0 2px 3px rgba(0,0,0,.5) inset;
}

progress[value]::-webkit-progress-value {
  position: relative;
  background-size: 35px 20px, 100% 100%, 100% 100%;
  border-radius:3px;
}

progress.active:not([value])::before {
  background-position: 10%;
  animation-name: stripes;
  animation-duration: 3s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

progress[value]::-moz-progress-bar {
  background-size: 35px 20px, 100% 100%, 100% 100%;
  border-radius:3px;
}

progress:not([value])::-moz-progress-bar {
  border-radius:3px;
  background: linear-gradient(-45deg, transparent 33%, rgba(0, 0, 0, 0.2) 33%, rgba(0, 0, 0, 0.2) 66%, transparent 66%) left/2.5em 1.5em;
}

progress.active:not([value])::-moz-progress-bar {
  background-position: 10%;
  animation-name: stripes;
  animation-duration: 3s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

progress.active:not([value])::-webkit-progress-bar {
  background-position: 10%;
  animation-name: stripes;
  animation-duration: 3s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

progress.primary[value]::-webkit-progress-value { background-color: #007bff; }
progress.primary:not([value])::before { background-color: #007bff; }
progress.primary:not([value])::-webkit-progress-bar { background-color: #007bff; }
progress.primary::-moz-progress-bar { background-color: #007bff; }

progress.secondary[value]::-webkit-progress-value { background-color: #6c757d; }
progress.secondary:not([value])::before { background-color: #6c757d; }
progress.secondary:not([value])::-webkit-progress-bar { background-color: #6c757d; }
progress.secondary::-moz-progress-bar { background-color: #6c757d; }

progress.success[value]::-webkit-progress-value { background-color: #28a745; }
progress.success:not([value])::before { background-color: #28a745; }
progress.success:not([value])::-webkit-progress-bar { background-color: #28a745; }
progress.success::-moz-progress-bar { background-color: #28a745; }

progress.danger[value]::-webkit-progress-value { background-color: #dc3545; }
progress.danger:not([value])::before { background-color: #dc3545; }
progress.danger:not([value])::-webkit-progress-bar { background-color: #dc3545; }
progress.danger::-moz-progress-bar { background-color: #dc3545; }

progress.warning[value]::-webkit-progress-value { background-color: #ffc107; }
progress.warning:not([value])::before { background-color: #ffc107; }
progress.warning:not([value])::-webkit-progress-bar { background-color: #ffc107; }
progress.warning::-moz-progress-bar { background-color: #ffc107; }

progress.info[value]::-webkit-progress-value { background-color: #17a2b8; }
progress.info:not([value])::before { background-color: #17a2b8; }
progress.info:not([value])::-webkit-progress-bar { background-color: #17a2b8; }
progress.info::-moz-progress-bar { background-color: #17a2b8; }

progress.light[value]::-webkit-progress-value { background-color: #f8f9fa; }
progress.light:not([value])::before { background-color: #f8f9fa; }
progress.light:not([value])::-webkit-progress-bar { background-color: #f8f9fa; }
progress.light::-moz-progress-bar { background-color: #f8f9fa; }

progress.dark[value]::-webkit-progress-value { background-color: #343a40; }
progress.dark:not([value])::-webkit-progress-bar { background-color: #343a40; }
progress.dark:not([value])::before { background-color: #343a40; }
progress.dark::-moz-progress-bar { background-color: #343a40; }

progress:not([value])::-webkit-progress-bar {
  border-radius: 3px;
  background: linear-gradient(-45deg, transparent 33%, rgba(0, 0, 0, 0.2) 33%, rgba(0, 0, 0, 0.2) 66%, transparent 66%) left/2.5em 1.5em;
}
progress:not([value])::before {
  content:" ";
  position:absolute;
  height: 20px;
  top:0;
  left:0;
  right:0;
  bottom:0;
  border-radius: 3px;
  background: linear-gradient(-45deg, transparent 33%, rgba(0, 0, 0, 0.2) 33%, rgba(0, 0, 0, 0.2) 66%, transparent 66%) left/2.5em 1.5em;
}

@keyframes stripes {
  from {background-position: 0%}
  to {background-position: 100%}
}

.bk-root .bk.loader {
  overflow: hidden;
}

.bk.loader::after {
  content: "";
  border-radius: 50%;
  -webkit-mask-image: radial-gradient(transparent 50%, rgba(0, 0, 0, 1) 54%);
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  position: absolute;
}

.bk-root .bk.loader.dark::after {
  background: #0f0f0f;
}

.bk-root .bk.loader.light::after {
  background: #f0f0f0;
}

.bk-root .bk.loader.spin::after {
  animation: spin 2s linear infinite;
}

.bk-root div.bk.loader.spin.primary-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #007bff 50%);
}

.bk-root div.bk.loader.spin.secondary-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #6c757d 50%);
}

.bk-root div.bk.loader.spin.success-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #28a745 50%);
}

.bk-root div.bk.loader.spin.danger-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #dc3545 50%);
}

.bk-root div.bk.loader.spin.warning-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #ffc107 50%);
}

.bk-root div.bk.loader.spin.info-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #17a2b8 50%);
}

.bk-root div.bk.loader.spin.light-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #f8f9fa 50%);
}

.bk-root div.bk.loader.dark-light::after {
  background: linear-gradient(135deg, #f0f0f0 50%, transparent 50%), linear-gradient(45deg, #f0f0f0 50%, #343a40 50%);
}

.bk-root div.bk.loader.spin.primary-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #007bff 50%);
}

.bk-root div.bk.loader.spin.secondary-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #6c757d 50%);
}

.bk-root div.bk.loader.spin.success-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #28a745 50%);
}

.bk-root div.bk.loader.spin.danger-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #dc3545 50%)
}

.bk-root div.bk.loader.spin.warning-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #ffc107 50%);
}

.bk-root div.bk.loader.spin.info-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #17a2b8 50%);
}

.bk-root div.bk.loader.spin.light-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #f8f9fa 50%);
}

.bk-root div.bk.loader.spin.dark-dark::after {
  background: linear-gradient(135deg, #0f0f0f 50%, transparent 50%), linear-gradient(45deg, #0f0f0f 50%, #343a40 50%);
}

/* Safari */
@-webkit-keyframes spin {
  0% { -webkit-transform: rotate(0deg); }
  100% { -webkit-transform: rotate(360deg); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.dot div {
  height: 100%;
  width: 100%;
  border: 1px solid #000 !important;
  background-color: #fff;
  border-radius: 50%;
  display: inline-block;
}

.dot-filled div {
  height: 100%;
  width: 100%;
  border: 1px solid #000 !important;
  border-radius: 50%;
  display: inline-block;
}

.dot-filled.primary div {
  background-color: #007bff;
}

.dot-filled.secondary div {
  background-color: #6c757d;
}

.dot-filled.success div {
  background-color: #28a745;
}

.dot-filled.danger div {
  background-color: #dc3545;
}

.dot-filled.warning div {
  background-color: #ffc107;
}

.dot-filled.info div {
  background-color: #17a2b8;
}

.dot-filled.dark div {
  background-color: #343a40;
}

.dot-filled.light div {
  background-color: #f8f9fa;
}

/* Slider editor */
.slider-edit .bk-input-group .bk-input {
  border: 0;
  border-radius: 0;
  min-height: 0;
  padding-left: 0;
  padding-right: 0;
  font-weight: bold;
}

.slider-edit .bk-input-group .bk-spin-wrapper {
  display: contents;
}

.slider-edit .bk-input-group .bk-spin-wrapper .bk.bk-spin-btn-up {
  top: -6px;
}

.slider-edit .bk-input-group .bk-spin-wrapper .bk.bk-spin-btn-down {
  bottom: 3px;
}

/* JSON Pane */
.bk-root .json-formatter-row .json-formatter-string, .bk-root .json-formatter-row .json-formatter-stringifiable {
  white-space: pre-wrap;
}

.ql-bubble .ql-editor {
  border: 1px solid #ccc;
}
`;
export default css;
