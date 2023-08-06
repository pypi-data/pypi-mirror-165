"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[15101],{14166:(e,t,r)=>{r.d(t,{W:()=>o});var i=function(){return i=Object.assign||function(e){for(var t,r=1,i=arguments.length;r<i;r++)for(var o in t=arguments[r])Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o]);return e},i.apply(this,arguments)};function o(e,t,r){void 0===t&&(t=Date.now()),void 0===r&&(r={});var o=i(i({},n),r||{}),a=(+e-+t)/1e3;if(Math.abs(a)<o.second)return{value:Math.round(a),unit:"second"};var s=a/60;if(Math.abs(s)<o.minute)return{value:Math.round(s),unit:"minute"};var c=a/3600;if(Math.abs(c)<o.hour)return{value:Math.round(c),unit:"hour"};var d=a/86400;if(Math.abs(d)<o.day)return{value:Math.round(d),unit:"day"};var l=new Date(e),h=new Date(t),u=l.getFullYear()-h.getFullYear();if(Math.round(Math.abs(u))>0)return{value:Math.round(u),unit:"year"};var p=12*u+l.getMonth()-h.getMonth();if(Math.round(Math.abs(p))>0)return{value:Math.round(p),unit:"month"};var f=a/604800;return{value:Math.round(f),unit:"week"}}var n={second:45,minute:45,hour:22,day:5}},5435:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{G:()=>s});var i=r(14166),o=r(14516),n=r(54121);n.Xp&&await n.Xp;const a=(0,o.Z)((e=>new Intl.RelativeTimeFormat(e.language,{numeric:"auto"}))),s=(e,t,r,o=!0)=>{const n=(0,i.W)(e,r);return o?a(t).format(n.value,n.unit):Intl.NumberFormat(t.language,{style:"unit",unit:n.unit,unitDisplay:"long"}).format(Math.abs(n.value))};e()}),1)},67876:(e,t,r)=>{r.a(e,(async e=>{r.r(t),r.d(t,{HaScriptTrace:()=>S});var i=r(37500),o=r(33310),n=r(8636),a=r(86230),s=r(7323),c=r(44583),d=(r(10983),r(71955),r(13126),r(89497)),l=r(78940),h=r(7719),u=(r(54933),r(19476)),p=r(55422),f=r(97389),v=r(26765),m=r(11654),y=r(29311),b=e([p,c,h,l,d]);function k(){k=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!w(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var d=c.extras;if(d){for(var l=0;l<d.length;l++)this.addElementPlacement(d[l],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return I(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?I(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=T(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:$(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=$(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function g(e){var t,r=T(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function _(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function w(e){return e.decorators&&e.decorators.length}function E(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function $(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function T(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function I(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function x(e,t,r){return x="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}},x(e,t,r||e)}function C(e){return C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},C(e)}[p,c,h,l,d]=b.then?await b:b;let S=function(e,t,r,i){var o=k();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(E(n.descriptor)||E(o.descriptor)){if(w(n)||w(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(w(n)){if(w(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}_(n,o)}else t.push(n)}return t}(a.d.map(g)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("ha-script-trace")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"scriptEntityId",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"scripts",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_traces",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_runId",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_selected",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_trace",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_logbookEntries",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_view",value:()=>"details"},{kind:"field",decorators:[(0,o.IO)("hat-script-graph")],key:"_graph",value:void 0},{kind:"method",key:"render",value:function(){var e;const t=this.scriptEntityId?this.hass.states[this.scriptEntityId]:void 0,r=this._graph,o=null==r?void 0:r.trackedNodes,s=null==r?void 0:r.renderedNodes,d=(null==t?void 0:t.attributes.friendly_name)||this.scriptEntityId;const l=i.dy`
      <ha-icon-button
        label="Refresh"
        @click=${this._refreshTraces}
        .path=${"M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"}
      ></ha-icon-button>
      <ha-icon-button
        .disabled=${!this._trace}
        label="Download Trace"
        @click=${this._downloadTrace}
        .path=${"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"}
      ></ha-icon-button>
    `;return i.dy`
      ${""}
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${y.configSections.automations}
      >
        ${this.narrow?i.dy`<span slot="header"> ${d} </span>
              <div slot="toolbar-icon">${l}</div>`:""}
        <div class="toolbar">
          ${this.narrow?"":i.dy`<div>
                ${d}
                <a
                  class="linkButton"
                  href="/config/script/edit/${this.scriptEntityId}"
                >
                  <ha-icon-button
                    label="Edit Script"
                    tabindex="-1"
                    .path=${"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}
                  ></ha-icon-button>
                </a>
              </div>`}
          ${this._traces&&this._traces.length>0?i.dy`
                <div>
                  <ha-icon-button
                    .disabled=${this._traces[this._traces.length-1].run_id===this._runId}
                    label="Older trace"
                    @click=${this._pickOlderTrace}
                    .path=${"M1,12L5,16V13H17.17C17.58,14.17 18.69,15 20,15A3,3 0 0,0 23,12A3,3 0 0,0 20,9C18.69,9 17.58,9.83 17.17,11H5V8L1,12Z"}
                  ></ha-icon-button>
                  <select .value=${this._runId} @change=${this._pickTrace}>
                    ${(0,a.r)(this._traces,(e=>e.run_id),(e=>i.dy`<option value=${e.run_id}>
                          ${(0,c.E8)(new Date(e.timestamp.start),this.hass.locale)}
                        </option>`))}
                  </select>
                  <ha-icon-button
                    .disabled=${this._traces[0].run_id===this._runId}
                    label="Newer trace"
                    @click=${this._pickNewerTrace}
                    .path=${"M23,12L19,16V13H6.83C6.42,14.17 5.31,15 4,15A3,3 0 0,1 1,12A3,3 0 0,1 4,9C5.31,9 6.42,9.83 6.83,11H19V8L23,12Z"}
                  ></ha-icon-button>
                </div>
              `:""}
          ${this.narrow?"":i.dy`<div>${l}</div>`}
        </div>

        ${void 0===this._traces?i.dy`<div class="container">Loading…</div>`:0===this._traces.length?i.dy`<div class="container">No traces found</div>`:void 0===this._trace?"":i.dy`
              <div class="main">
                <div class="graph">
                  <hat-script-graph
                    .trace=${this._trace}
                    .selected=${null===(e=this._selected)||void 0===e?void 0:e.path}
                    @graph-node-selected=${this._pickNode}
                  ></hat-script-graph>
                </div>

                <div class="info">
                  <div class="tabs top">
                    ${[["details","Step Details"],["timeline","Trace Timeline"],["logbook","Related logbook entries"],["config","Script Config"]].map((([e,t])=>i.dy`
                        <button
                          tabindex="0"
                          .view=${e}
                          class=${(0,n.$)({active:this._view===e})}
                          @click=${this._showTab}
                        >
                          ${t}
                        </button>
                      `))}
                    ${this._trace.blueprint_inputs?i.dy`
                          <button
                            tabindex="0"
                            .view=${"blueprint"}
                            class=${(0,n.$)({active:"blueprint"===this._view})}
                            @click=${this._showTab}
                          >
                            Blueprint Config
                          </button>
                        `:""}
                  </div>
                  ${void 0===this._selected||void 0===this._logbookEntries||void 0===o?"":"details"===this._view?i.dy`
                        <ha-trace-path-details
                          .hass=${this.hass}
                          .narrow=${this.narrow}
                          .trace=${this._trace}
                          .selected=${this._selected}
                          .logbookEntries=${this._logbookEntries}
                          .trackedNodes=${o}
                          .renderedNodes=${s}
                        ></ha-trace-path-details>
                      `:"config"===this._view?i.dy`
                        <ha-trace-config
                          .hass=${this.hass}
                          .trace=${this._trace}
                        ></ha-trace-config>
                      `:"logbook"===this._view?i.dy`
                        <ha-trace-logbook
                          .hass=${this.hass}
                          .narrow=${this.narrow}
                          .trace=${this._trace}
                          .logbookEntries=${this._logbookEntries}
                        ></ha-trace-logbook>
                      `:"blueprint"===this._view?i.dy`
                        <ha-trace-blueprint-config
                          .hass=${this.hass}
                          .trace=${this._trace}
                        ></ha-trace-blueprint-config>
                      `:i.dy`
                        <ha-trace-timeline
                          .hass=${this.hass}
                          .trace=${this._trace}
                          .logbookEntries=${this._logbookEntries}
                          .selected=${this._selected}
                          @value-changed=${this._timelinePathPicked}
                        ></ha-trace-timeline>
                      `}
                </div>
              </div>
            `}
      </hass-tabs-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){if(x(C(r.prototype),"firstUpdated",this).call(this,e),!this.scriptEntityId)return;const t=new URLSearchParams(location.search);this._loadTraces(t.get("run_id")||void 0)}},{kind:"method",key:"willUpdate",value:function(e){x(C(r.prototype),"willUpdate",this).call(this,e),e.get("scriptEntityId")&&(this._traces=void 0,this._runId=void 0,this._trace=void 0,this._logbookEntries=void 0,this.scriptEntityId&&this._loadTraces()),e.has("_runId")&&this._runId&&(this._trace=void 0,this._logbookEntries=void 0,this._loadTrace())}},{kind:"method",key:"_pickOlderTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e+1].run_id,this._selected=void 0}},{kind:"method",key:"_pickNewerTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e-1].run_id,this._selected=void 0}},{kind:"method",key:"_pickTrace",value:function(e){this._runId=e.target.value,this._selected=void 0}},{kind:"method",key:"_pickNode",value:function(e){this._selected=e.detail}},{kind:"method",key:"_refreshTraces",value:function(){this._loadTraces()}},{kind:"method",key:"_loadTraces",value:async function(e){if(this._traces=await(0,f.lj)(this.hass,"script",this.scriptEntityId.split(".")[1]),this._traces.reverse(),e&&(this._runId=e),this._runId&&!this._traces.some((e=>e.run_id===this._runId))){if(this._runId=void 0,this._selected=void 0,e){const e=new URLSearchParams(location.search);e.delete("run_id"),history.replaceState(null,"",`${location.pathname}?${e.toString()}`)}await(0,v.Ys)(this,{text:"Chosen trace is no longer available"})}!this._runId&&this._traces.length>0&&(this._runId=this._traces[0].run_id)}},{kind:"method",key:"_loadTrace",value:async function(){const e=await(0,f.mA)(this.hass,"script",this.scriptEntityId.split(".")[1],this._runId);this._logbookEntries=(0,s.p)(this.hass,"logbook")?await(0,p.sS)(this.hass,e.timestamp.start,e.context.id):[],this._trace=e}},{kind:"method",key:"_downloadTrace",value:function(){const e=document.createElement("a");e.download=`trace ${this.scriptEntityId} ${this._trace.timestamp.start}.json`,e.href=`data:application/json;charset=utf-8,${encodeURI(JSON.stringify({trace:this._trace,logbookEntries:this._logbookEntries},void 0,2))}`,e.click()}},{kind:"method",key:"_importTrace",value:function(){const e=prompt("Enter downloaded trace");e&&(localStorage.devTrace=e,this._loadLocalTrace(e))}},{kind:"method",key:"_loadLocalStorageTrace",value:function(){localStorage.devTrace&&this._loadLocalTrace(localStorage.devTrace)}},{kind:"method",key:"_loadLocalTrace",value:function(e){const t=JSON.parse(e);this._trace=t.trace,this._logbookEntries=t.logbookEntries}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"method",key:"_timelinePathPicked",value:function(e){const t=e.detail.value,r=this._graph.trackedNodes;r[t]&&(this._selected=r[t])}},{kind:"get",static:!0,key:"styles",value:function(){return[m.Qx,u.b,i.iv`
        .toolbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 20px;
          height: var(--header-height);
          padding: 0 16px;
          background-color: var(--primary-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }

        .toolbar > * {
          display: flex;
          align-items: center;
        }

        :host([narrow]) .toolbar > * {
          display: contents;
        }

        .main {
          height: calc(100% - 56px);
          display: flex;
          background-color: var(--card-background-color);
        }

        :host([narrow]) .main {
          height: auto;
          flex-direction: column;
        }

        .container {
          padding: 16px;
        }

        .graph {
          border-right: 1px solid var(--divider-color);
          overflow-x: auto;
          max-width: 50%;
        }
        :host([narrow]) .graph {
          max-width: 100%;
        }

        .info {
          flex: 1;
          background-color: var(--card-background-color);
        }

        .linkButton {
          color: var(--primary-text-color);
        }
      `]}}]}}),i.oi)}))}}]);
//# sourceMappingURL=b9e64a2f.js.map