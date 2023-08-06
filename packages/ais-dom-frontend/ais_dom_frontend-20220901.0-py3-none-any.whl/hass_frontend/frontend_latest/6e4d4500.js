"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[80736],{5435:(e,r,t)=>{t.a(e,(async e=>{t.d(r,{G:()=>a});var i=t(14166),o=t(14516),n=t(54121);n.Xp&&await n.Xp;const s=(0,o.Z)((e=>new Intl.RelativeTimeFormat(e.language,{numeric:"auto"}))),a=(e,r,t,o=!0)=>{const n=(0,i.W)(e,t);return o?s(r).format(n.value,n.unit):Intl.NumberFormat(r.language,{style:"unit",unit:n.unit,unitDisplay:"long"}).format(Math.abs(n.value))};e()}),1)},21780:(e,r,t)=>{t.d(r,{f:()=>i});const i=e=>e.charAt(0).toUpperCase()+e.slice(1)},45339:(e,r,t)=>{t.d(r,{wC:()=>n,Ur:()=>a,F$:()=>l,iU:()=>d,eJ:()=>c,EB:()=>p,$X:()=>m});var i=t(97330),o=t(38346);const n={critical:1,error:2,warning:3},s=e=>e.sendMessagePromise({type:"repairs/list_issues"}),a=async(e,r,t)=>e.callWS({type:"repairs/ignore_issue",issue_id:r.issue_id,domain:r.domain,ignore:t}),l=(e,r,t)=>e.callApi("POST","repairs/issues/fix",{handler:r,issue_id:t}),d=(e,r)=>e.callApi("GET",`repairs/issues/fix/${r}`),c=(e,r,t)=>e.callApi("POST",`repairs/issues/fix/${r}`,t),p=(e,r)=>e.callApi("DELETE",`repairs/issues/fix/${r}`),u=(e,r)=>e.subscribeEvents((0,o.D)((()=>s(e).then((e=>r.setState(e,!0)))),500,!0),"repairs_issue_registry_updated"),m=(e,r)=>(0,i.B)("_repairsIssueRegistry",s,u,e,r)},52871:(e,r,t)=>{t.d(r,{w:()=>n});var i=t(47181);const o=()=>Promise.all([t.e(29563),t.e(98985),t.e(24103),t.e(59799),t.e(6294),t.e(88278),t.e(41985),t.e(85084),t.e(45507),t.e(80807),t.e(51644),t.e(68200),t.e(49842),t.e(1548),t.e(49075),t.e(81480),t.e(16238),t.e(86424),t.e(29925),t.e(12545),t.e(13701),t.e(77576),t.e(65040),t.e(68101),t.e(4940),t.e(73054),t.e(34821)]).then(t.bind(t,81585)),n=(e,r,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:o,dialogParams:{...r,flowConfig:t,dialogParentElement:e}})}},80736:(e,r,t)=>{t.a(e,(async e=>{t(24103);var r=t(37500),i=t(33310),o=t(5435),n=t(21780),s=(t(9381),t(22098),t(73366),t(52039),t(5986)),a=(t(60010),t(11254)),l=t(60904),d=t(33807),c=e([o]);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,r){["method","field"].forEach((function(t){r.forEach((function(r){r.kind===t&&"own"===r.placement&&this.defineClassElement(e,r)}),this)}),this)},initializeClassElements:function(e,r){var t=e.prototype;["method","field"].forEach((function(i){r.forEach((function(r){var o=r.placement;if(r.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:t;this.defineClassElement(n,r)}}),this)}),this)},defineClassElement:function(e,r){var t=r.descriptor;if("field"===r.kind){var i=r.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,r.key,t)},decorateClass:function(e,r){var t=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!f(e))return t.push(e);var r=this.decorateElement(e,o);t.push(r.element),t.push.apply(t,r.extras),i.push.apply(i,r.finishers)}),this),!r)return{elements:t,finishers:i};var n=this.decorateConstructor(t,r);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,r,t){var i=r[e.placement];if(!t&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,r){for(var t=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=r[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,r),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],r);t.push.apply(t,d)}}return{element:e,finishers:i,extras:t}},decorateConstructor:function(e,r){for(var t=[],i=r.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,r[i])(o)||o);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:t}},fromElementDescriptor:function(e){var r={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(r.initializer=e.initializer),r},toElementDescriptors:function(e){var r;if(void 0!==e)return(r=e,function(e){if(Array.isArray(e))return e}(r)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(r)||function(e,r){if(e){if("string"==typeof e)return v(e,r);var t=Object.prototype.toString.call(e).slice(8,-1);return"Object"===t&&e.constructor&&(t=e.constructor.name),"Map"===t||"Set"===t?Array.from(e):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?v(e,r):void 0}}(r)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var r=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),r}),this)},toElementDescriptor:function(e){var r=String(e.kind);if("method"!==r&&"field"!==r)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+r+'"');var t=w(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:r,key:t,placement:i,descriptor:Object.assign({},o)};return"field"!==r?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var r={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),r},toClassDescriptor:function(e){var r=String(e.kind);if("class"!==r)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+r+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var t=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:t}},runClassFinishers:function(e,r){for(var t=0;t<r.length;t++){var i=(0,r[t])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,r,t){if(void 0!==e[r])throw new TypeError(t+" can't have a ."+r+" property.")}};return e}function u(e){var r,t=w(e.key);"method"===e.kind?r={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?r={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?r={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(r={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:t,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:r};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function m(e,r){void 0!==e.descriptor.get?r.descriptor.get=e.descriptor.get:r.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,r){var t=e[r];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+r+"' to be a function");return t}function w(e){var r=function(e,r){if("object"!=typeof e||null===e)return e;var t=e[Symbol.toPrimitive];if(void 0!==t){var i=t.call(e,r||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===r?String:Number)(e)}(e,"string");return"symbol"==typeof r?r:String(r)}function v(e,r){(null==r||r>e.length)&&(r=e.length);for(var t=0,i=new Array(r);t<r;t++)i[t]=e[t];return i}o=(c.then?await c:c)[0];!function(e,r,t,i){var o=p();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=r((function(e){o.initializeInstanceElements(e,a.elements)}),t),a=o.decorateClass(function(e){for(var r=[],t=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=r.find(t)))if(h(n.descriptor)||h(o.descriptor)){if(f(n)||f(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(f(n)){if(f(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}m(n,o)}else r.push(n)}return r}(s.d.map(u)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-config-repairs")],(function(e,t){return{F:class extends t{constructor(...r){super(...r),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"repairsIssues",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Number})],key:"total",value:void 0},{kind:"method",key:"render",value:function(){var e;if(null===(e=this.repairsIssues)||void 0===e||!e.length)return r.dy``;const t=this.repairsIssues;return r.dy`
      <div class="title">
        ${this.hass.localize("ui.panel.config.repairs.title",{count:this.total||this.repairsIssues.length})}
      </div>
      <mwc-list>
        ${t.map((e=>{var t;return r.dy`
            <ha-list-item
              twoline
              graphic="medium"
              .hasMeta=${!this.narrow}
              .issue=${e}
              class=${e.ignored?"ignored":""}
              @click=${this._openShowMoreDialog}
            >
              <img
                loading="lazy"
                src=${(0,a.X1)({domain:e.issue_domain||e.domain,type:"icon",useFallback:!0,darkOptimized:null===(t=this.hass.themes)||void 0===t?void 0:t.darkMode})}
                .title=${(0,s.Lh)(this.hass.localize,e.domain)}
                referrerpolicy="no-referrer"
                slot="graphic"
              />
              <span
                >${this.hass.localize(`component.${e.domain}.issues.${e.translation_key||e.issue_id}.title`,e.translation_placeholders||{})}</span
              >
              <span slot="secondary" class="secondary">
                ${"critical"===e.severity||"error"===e.severity?r.dy`<span class="error"
                      >${this.hass.localize(`ui.panel.config.repairs.${e.severity}`)}</span
                    >`:""}
                ${"critical"!==e.severity&&"error"!==e.severity||!e.created?"":" - "}
                ${e.created?(0,n.f)((0,o.G)(new Date(e.created),this.hass.locale)):""}
                ${e.ignored?` - ${this.hass.localize("ui.panel.config.repairs.dialog.ignored_in_version_short",{version:e.dismissed_version})}`:""}
              </span>
              ${this.narrow?"":r.dy`<ha-icon-next slot="meta"></ha-icon-next>`}
            </ha-list-item>
          `}))}
      </mwc-list>
    `}},{kind:"method",key:"_openShowMoreDialog",value:function(e){const r=e.currentTarget.issue;r.is_fixable?(0,l.w)(this,r):(0,d.W)(this,{issue:r})}},{kind:"field",static:!0,key:"styles",value:()=>r.iv`
    :host {
      --mdc-list-vertical-padding: 0;
    }
    .title {
      font-size: 16px;
      padding: 16px;
      padding-bottom: 0;
    }
    .ignored {
      opacity: var(--light-secondary-opacity);
    }
    ha-list-item {
      --mdc-list-item-graphic-size: 40px;
    }
    button.show-more {
      color: var(--primary-color);
      text-align: left;
      cursor: pointer;
      background: none;
      border-width: initial;
      border-style: none;
      border-color: initial;
      border-image: initial;
      padding: 16px;
      font: inherit;
    }
    button.show-more:focus {
      outline: none;
      text-decoration: underline;
    }
    ha-list-item {
      cursor: pointer;
      font-size: 16px;
    }
    .error {
      color: var(--error-color);
    }
  `}]}}),r.oi)}))},60904:(e,r,t)=>{t.d(r,{w:()=>a});var i=t(37500),o=t(5986),n=t(45339),s=t(52871);const a=(e,r,t)=>(0,s.w)(e,{startFlowHandler:r.domain,domain:r.domain,dialogClosedCallback:t},{loadDevicesAndAreas:!1,createFlow:async(e,t)=>{const[i]=await Promise.all([(0,n.F$)(e,t,r.issue_id),e.loadBackendTranslation("issues",r.domain)]);return i},fetchFlow:async(e,t)=>{const[i]=await Promise.all([(0,n.iU)(e,t),e.loadBackendTranslation("issues",r.domain)]);return i},handleFlowStep:n.eJ,deleteFlow:n.EB,renderAbortDescription(e,t){const o=e.localize(`component.${r.domain}.issues.abort.${t.reason}`,t.description_placeholders);return o?i.dy`
              <ha-markdown
                breaks
                allowsvg
                .content=${o}
              ></ha-markdown>
            `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.step.${t.step_id}.title`,t.description_placeholders)||e.localize("ui.dialogs.repair_flow.form.header"),renderShowFormStepDescription(e,t){const o=e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.step.${t.step_id}.description`,t.description_placeholders);return o?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${o}
              ></ha-markdown>
            `:""},renderShowFormStepFieldLabel:(e,t,i)=>e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.step.${t.step_id}.data.${i.name}`),renderShowFormStepFieldHelper(e,t,o){const n=e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.step.${t.step_id}.data_description.${o.name}`,t.description_placeholders);return n?i.dy`<ha-markdown breaks .content=${n}></ha-markdown>`:""},renderShowFormStepFieldError:(e,t,i)=>e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.error.${i}`,t.description_placeholders),renderExternalStepHeader:(e,r)=>"",renderExternalStepDescription:(e,r)=>"",renderCreateEntryDescription:(e,r)=>i.dy`
          <p>${e.localize("ui.dialogs.repair_flow.success.description")}</p>
        `,renderShowFormProgressHeader:(e,t)=>e.localize(`component.${r.domain}.issues.step.${r.translation_key||r.issue_id}.fix_flow.${t.step_id}.title`)||e.localize(`component.${r.domain}.title`),renderShowFormProgressDescription(e,t){const o=e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.progress.${t.progress_action}`,t.description_placeholders);return o?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${o}
              ></ha-markdown>
            `:""},renderMenuHeader:(e,t)=>e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.step.${t.step_id}.title`)||e.localize(`component.${r.domain}.title`),renderMenuDescription(e,t){const o=e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.step.${t.step_id}.description`,t.description_placeholders);return o?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${o}
              ></ha-markdown>
            `:""},renderMenuOption:(e,t,i)=>e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.step.${t.step_id}.menu_issues.${i}`,t.description_placeholders),renderLoadingDescription:(e,t)=>e.localize(`component.${r.domain}.issues.${r.translation_key||r.issue_id}.fix_flow.loading`)||e.localize(`ui.dialogs.repair_flow.loading.${t}`,{integration:(0,o.Lh)(e.localize,r.domain)})})},33807:(e,r,t)=>{t.d(r,{W:()=>n});var i=t(47181);const o=()=>Promise.all([t.e(85084),t.e(86603),t.e(29925),t.e(4940),t.e(14921)]).then(t.bind(t,14921)),n=(e,r)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-repairs-issue",dialogImport:o,dialogParams:r})}},11254:(e,r,t)=>{t.d(r,{X1:()=>i,RU:()=>o,u4:()=>n,zC:()=>s});const i=e=>e.domain.startsWith("ais_")?`https://ai-speaker.com/images/brands/${e.domain}/${e.type}.png`:`https://brands.home-assistant.io/${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,o=e=>`https://brands.home-assistant.io/hardware/${e.category}/${e.darkOptimized?"dark_":""}${e.manufacturer}${e.model?`_${e.model}`:""}.png`,n=e=>e.split("/")[4],s=e=>e.startsWith("https://brands.home-assistant.io/")}}]);
//# sourceMappingURL=6e4d4500.js.map