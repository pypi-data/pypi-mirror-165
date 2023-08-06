/*! For license information please see 1d4aab5d.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[344],{89833:(t,i,e)=>{e.d(i,{O:()=>d});var n=e(87480),a=e(86251),o=e(37500),s=e(33310),r=e(8636),l=e(51346),p=e(71260);const h={fromAttribute:t=>null!==t&&(""===t||t),toAttribute:t=>"boolean"==typeof t?t?"":null:t};class d extends a.P{constructor(){super(...arguments),this.rows=2,this.cols=20,this.charCounter=!1}render(){const t=this.charCounter&&-1!==this.maxLength,i=t&&"internal"===this.charCounter,e=t&&!i,n=!!this.helper||!!this.validationMessage||e,a={"mdc-text-field--disabled":this.disabled,"mdc-text-field--no-label":!this.label,"mdc-text-field--filled":!this.outlined,"mdc-text-field--outlined":this.outlined,"mdc-text-field--end-aligned":this.endAligned,"mdc-text-field--with-internal-counter":i};return o.dy`
      <label class="mdc-text-field mdc-text-field--textarea ${(0,r.$)(a)}">
        ${this.renderRipple()}
        ${this.outlined?this.renderOutline():this.renderLabel()}
        ${this.renderInput()}
        ${this.renderCharCounter(i)}
        ${this.renderLineRipple()}
      </label>
      ${this.renderHelperText(n,e)}
    `}renderInput(){const t=this.label?"label":void 0,i=-1===this.minLength?void 0:this.minLength,e=-1===this.maxLength?void 0:this.maxLength,n=this.autocapitalize?this.autocapitalize:void 0;return o.dy`
      <textarea
          aria-labelledby=${(0,l.o)(t)}
          class="mdc-text-field__input"
          .value="${(0,p.a)(this.value)}"
          rows="${this.rows}"
          cols="${this.cols}"
          ?disabled="${this.disabled}"
          placeholder="${this.placeholder}"
          ?required="${this.required}"
          ?readonly="${this.readOnly}"
          minlength="${(0,l.o)(i)}"
          maxlength="${(0,l.o)(e)}"
          name="${(0,l.o)(""===this.name?void 0:this.name)}"
          inputmode="${(0,l.o)(this.inputMode)}"
          autocapitalize="${(0,l.o)(n)}"
          @input="${this.handleInputChange}"
          @blur="${this.onInputBlur}">
      </textarea>`}}(0,n.__decorate)([(0,s.IO)("textarea")],d.prototype,"formElement",void 0),(0,n.__decorate)([(0,s.Cb)({type:Number})],d.prototype,"rows",void 0),(0,n.__decorate)([(0,s.Cb)({type:Number})],d.prototype,"cols",void 0),(0,n.__decorate)([(0,s.Cb)({converter:h})],d.prototype,"charCounter",void 0)},96791:(t,i,e)=>{e.d(i,{W:()=>n});const n=e(37500).iv`.mdc-text-field{height:100%}.mdc-text-field__input{resize:none}`},89194:(t,i,e)=>{e(48175),e(65660),e(70019);var n=e(9672),a=e(50856);(0,n.k)({_template:a.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},54444:(t,i,e)=>{e(48175);var n=e(9672),a=e(87156),o=e(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,a.vz)(this).parentNode,i=(0,a.vz)(this).getOwnerRoot();return this.for?(0,a.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,a.vz)(this).textContent.trim()){for(var t=!0,i=(0,a.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,n=this.offsetParent.getBoundingClientRect(),a=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),s=(a.width-o.width)/2,r=(a.height-o.height)/2,l=a.left-n.left,p=a.top-n.top;switch(this.position){case"top":i=l+s,e=p-o.height-t;break;case"bottom":i=l+s,e=p+a.height+t;break;case"left":i=l-o.width-t,e=p+r;break;case"right":i=l+a.width+t,e=p+r}this.fitToVisibleBounds?(n.left+i+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),n.top+e+o.height>window.innerHeight?(this.style.bottom=n.height-p+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},3239:(t,i,e)=>{function n(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(n);var i={};return Object.keys(t).forEach((function(e){i[e]=n(t[e])})),i}e.d(i,{Z:()=>n})},1460:(t,i,e)=>{e.d(i,{l:()=>s});var n=e(15304),a=e(38941);const o={},s=(0,a.XM)(class extends a.Xe{constructor(){super(...arguments),this.nt=o}render(t,i){return i()}update(t,[i,e]){if(Array.isArray(i)){if(Array.isArray(this.nt)&&this.nt.length===i.length&&i.every(((t,i)=>t===this.nt[i])))return n.Jb}else if(this.nt===i)return n.Jb;return this.nt=Array.isArray(i)?Array.from(i):i,this.render(i,e)}})},86230:(t,i,e)=>{e.d(i,{r:()=>r});var n=e(15304),a=e(38941),o=e(81563);const s=(t,i,e)=>{const n=new Map;for(let a=i;a<=e;a++)n.set(t[a],a);return n},r=(0,a.XM)(class extends a.Xe{constructor(t){if(super(t),t.type!==a.pX.CHILD)throw Error("repeat() can only be used in text expressions")}dt(t,i,e){let n;void 0===e?e=i:void 0!==i&&(n=i);const a=[],o=[];let s=0;for(const i of t)a[s]=n?n(i,s):s,o[s]=e(i,s),s++;return{values:o,keys:a}}render(t,i,e){return this.dt(t,i,e).values}update(t,[i,e,a]){var r;const l=(0,o.i9)(t),{values:p,keys:h}=this.dt(i,e,a);if(!Array.isArray(l))return this.at=h,p;const d=null!==(r=this.at)&&void 0!==r?r:this.at=[],m=[];let u,c,y=0,f=l.length-1,g=0,v=p.length-1;for(;y<=f&&g<=v;)if(null===l[y])y++;else if(null===l[f])f--;else if(d[y]===h[g])m[g]=(0,o.fk)(l[y],p[g]),y++,g++;else if(d[f]===h[v])m[v]=(0,o.fk)(l[f],p[v]),f--,v--;else if(d[y]===h[v])m[v]=(0,o.fk)(l[y],p[v]),(0,o._Y)(t,m[v+1],l[y]),y++,v--;else if(d[f]===h[g])m[g]=(0,o.fk)(l[f],p[g]),(0,o._Y)(t,l[y],l[f]),f--,g++;else if(void 0===u&&(u=s(h,g,v),c=s(d,y,f)),u.has(d[y]))if(u.has(d[f])){const i=c.get(h[g]),e=void 0!==i?l[i]:null;if(null===e){const i=(0,o._Y)(t,l[y]);(0,o.fk)(i,p[g]),m[g]=i}else m[g]=(0,o.fk)(e,p[g]),(0,o._Y)(t,l[y],e),l[i]=null;g++}else(0,o.ws)(l[f]),f--;else(0,o.ws)(l[y]),y++;for(;g<=v;){const i=(0,o._Y)(t,m[v+1]);(0,o.fk)(i,p[g]),m[g++]=i}for(;y<=f;){const t=l[y++];null!==t&&(0,o.ws)(t)}return this.at=h,(0,o.hl)(t,m),n.Jb}})}}]);
//# sourceMappingURL=1d4aab5d.js.map