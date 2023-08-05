var _JUPYTERLAB;(()=>{"use strict";var e,r,t,a,o,n,l,i,f,s,u,d,c,p,b,h,m,v,y={3846:(e,r,t)=>{var a={"./index":()=>Promise.all([t.e(472),t.e(526),t.e(991),t.e(381),t.e(321)]).then((()=>()=>t(1321))),"./extension":()=>Promise.all([t.e(472),t.e(526),t.e(991),t.e(381),t.e(321)]).then((()=>()=>t(1321)))},o=(e,r)=>(t.R=r,r=t.o(a,e)?a[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),n=(e,r)=>{if(t.S){var a="default",o=t.S[a];if(o&&o!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[a]=e,t.I(a,r)}};t.d(r,{get:()=>o,init:()=>n})}},g={};function w(e){var r=g[e];if(void 0!==r)return r.exports;var t=g[e]={id:e,loaded:!1,exports:{}};return y[e](t,t.exports,w),t.loaded=!0,t.exports}w.m=y,w.c=g,w.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return w.d(r,{a:r}),r},w.d=(e,r)=>{for(var t in r)w.o(r,t)&&!w.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},w.f={},w.e=e=>Promise.all(Object.keys(w.f).reduce(((r,t)=>(w.f[t](e,r),r)),[])),w.u=e=>(16===e?"jupyter-lsp-connection":e)+"."+{16:"79bd64bbdf23dbb3e394",44:"4734a54a6ff96b07fb72",155:"0a6883ebb36e8f755887",235:"f8695803b69cf4d65ca1",321:"0176abf53bb1a24b854d",381:"3948ab48f0563ca0f7b7",472:"b49d5d603826c26b91c5",480:"dc7e4debb1149fbd5349",484:"b84bf84fc6d386ef63b5",501:"b24040a027bc54eca722",526:"f4f11bff1cad26c9788f",637:"88b1b47bec1fcf1f16fd",676:"4df0f958ff2d37c58dc5",732:"913fecaf06a081f9f5ab",875:"22b6aa2b1ee0cb6094f2",991:"b14ff4336b5d6dc1b4e7"}[e]+".js?v="+{16:"79bd64bbdf23dbb3e394",44:"4734a54a6ff96b07fb72",155:"0a6883ebb36e8f755887",235:"f8695803b69cf4d65ca1",321:"0176abf53bb1a24b854d",381:"3948ab48f0563ca0f7b7",472:"b49d5d603826c26b91c5",480:"dc7e4debb1149fbd5349",484:"b84bf84fc6d386ef63b5",501:"b24040a027bc54eca722",526:"f4f11bff1cad26c9788f",637:"88b1b47bec1fcf1f16fd",676:"4df0f958ff2d37c58dc5",732:"913fecaf06a081f9f5ab",875:"22b6aa2b1ee0cb6094f2",991:"b14ff4336b5d6dc1b4e7"}[e],w.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),w.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@krassowski/jupyterlab-lsp:",w.l=(t,a,o,n)=>{if(e[t])e[t].push(a);else{var l,i;if(void 0!==o)for(var f=document.getElementsByTagName("script"),s=0;s<f.length;s++){var u=f[s];if(u.getAttribute("src")==t||u.getAttribute("data-webpack")==r+o){l=u;break}}l||(i=!0,(l=document.createElement("script")).charset="utf-8",l.timeout=120,w.nc&&l.setAttribute("nonce",w.nc),l.setAttribute("data-webpack",r+o),l.src=t),e[t]=[a];var d=(r,a)=>{l.onerror=l.onload=null,clearTimeout(c);var o=e[t];if(delete e[t],l.parentNode&&l.parentNode.removeChild(l),o&&o.forEach((e=>e(a))),r)return r(a)},c=setTimeout(d.bind(null,void 0,{type:"timeout",target:l}),12e4);l.onerror=d.bind(null,l.onerror),l.onload=d.bind(null,l.onload),i&&document.head.appendChild(l)}},w.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},w.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),(()=>{w.S={};var e={},r={};w.I=(t,a)=>{a||(a=[]);var o=r[t];if(o||(o=r[t]={}),!(a.indexOf(o)>=0)){if(a.push(o),e[t])return e[t];w.o(w.S,t)||(w.S[t]={});var n=w.S[t],l="@krassowski/jupyterlab-lsp",i=(e,r,t,a)=>{var o=n[e]=n[e]||{},i=o[r];(!i||!i.loaded&&(!a!=!i.eager?a:l>i.from))&&(o[r]={get:t,from:l,eager:!!a})},f=[];return"default"===t&&(i("@krassowski/code-jumpers","1.2.0",(()=>Promise.all([w.e(991),w.e(480)]).then((()=>()=>w(6480))))),i("@krassowski/completion-theme","3.3.1",(()=>Promise.all([w.e(526),w.e(991),w.e(381),w.e(44)]).then((()=>()=>w(44))))),i("@krassowski/jupyterlab-lsp","3.10.2",(()=>Promise.all([w.e(472),w.e(526),w.e(991),w.e(381),w.e(321)]).then((()=>()=>w(1321))))),i("@krassowski/theme-material","2.1.1",(()=>Promise.all([w.e(526),w.e(235)]).then((()=>()=>w(6235))))),i("@krassowski/theme-vscode","2.1.1",(()=>Promise.all([w.e(526),w.e(676),w.e(875)]).then((()=>()=>w(676))))),i("lodash.mergewith","4.6.2",(()=>w.e(637).then((()=>()=>w(3637))))),i("lsp-ws-connection","0.7.0",(()=>w.e(732).then((()=>()=>w(2732)))))),e[t]=f.length?Promise.all(f).then((()=>e[t]=1)):1}}})(),(()=>{var e;w.g.importScripts&&(e=w.g.location+"");var r=w.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),w.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),a=t[1]?r(t[1]):[];return t[2]&&(a.length++,a.push.apply(a,r(t[2]))),t[3]&&(a.push([]),a.push.apply(a,r(t[3]))),a},a=(e,r)=>{e=t(e),r=t(r);for(var a=0;;){if(a>=e.length)return a<r.length&&"u"!=(typeof r[a])[0];var o=e[a],n=(typeof o)[0];if(a>=r.length)return"u"==n;var l=r[a],i=(typeof l)[0];if(n!=i)return"o"==n&&"n"==i||"s"==i||"u"==n;if("o"!=n&&"u"!=n&&o!=l)return o<l;a++}},o=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var a=1,n=1;n<e.length;n++)a--,t+="u"==(typeof(i=e[n]))[0]?"-":(a>0?".":"")+(a=2,i);return t}var l=[];for(n=1;n<e.length;n++){var i=e[n];l.push(0===i?"not("+f()+")":1===i?"("+f()+" || "+f()+")":2===i?l.pop()+" "+l.pop():o(i))}return f();function f(){return l.pop().replace(/^\((.+)\)$/,"$1")}},n=(e,r)=>{if(0 in e){r=t(r);var a=e[0],o=a<0;o&&(a=-a-1);for(var l=0,i=1,f=!0;;i++,l++){var s,u,d=i<e.length?(typeof e[i])[0]:"";if(l>=r.length||"o"==(u=(typeof(s=r[l]))[0]))return!f||("u"==d?i>a&&!o:""==d!=o);if("u"==u){if(!f||"u"!=d)return!1}else if(f)if(d==u)if(i<=a){if(s!=e[i])return!1}else{if(o?s>e[i]:s<e[i])return!1;s!=e[i]&&(f=!1)}else if("s"!=d&&"n"!=d){if(o||i<=a)return!1;f=!1,i--}else{if(i<=a||u<d!=o)return!1;f=!1}else"s"!=d&&"n"!=d&&(f=!1,i--)}}var c=[],p=c.pop.bind(c);for(l=1;l<e.length;l++){var b=e[l];c.push(1==b?p()|p():2==b?p()&p():b?n(b,r):!p())}return!!p()},l=(e,r)=>{var t=w.S[e];if(!t||!w.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},i=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&a(e,r)?r:e),0)},f=(e,r,t,a)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+o(a)+")",s=(e,r,t,a)=>{var o=i(e,t);return n(a,o)||"undefined"!=typeof console&&console.warn&&console.warn(f(e,t,o,a)),d(e[t][o])},u=(e,r,t)=>{var o=e[r];return(r=Object.keys(o).reduce(((e,r)=>!n(t,r)||e&&!a(e,r)?e:r),0))&&o[r]},d=e=>(e.loaded=1,e.get()),p=(c=e=>function(r,t,a,o){var n=w.I(r);return n&&n.then?n.then(e.bind(e,r,w.S[r],t,a,o)):e(r,w.S[r],t,a,o)})(((e,r,t,a)=>(l(e,t),s(r,0,t,a)))),b=c(((e,r,t,a,o)=>{var n=r&&w.o(r,t)&&u(r,t,a);return n?d(n):o()})),h={},m={1526:()=>p("default","@lumino/coreutils",[1,1,11,0]),1991:()=>p("default","@jupyterlab/apputils",[1,3,4,5]),3082:()=>p("default","@jupyterlab/translation",[1,3,4,5]),6271:()=>p("default","react",[1,17,0,1]),8912:()=>p("default","@jupyterlab/ui-components",[1,3,4,5]),1256:()=>p("default","@jupyterlab/codeeditor",[1,3,4,5]),1580:()=>p("default","@jupyterlab/tooltip",[1,3,4,5]),1840:()=>p("default","@lumino/signaling",[1,1,10,0]),1921:()=>p("default","@jupyterlab/settingregistry",[1,3,4,5]),2230:()=>b("default","@krassowski/theme-material",[2,2,1,1],(()=>w.e(484).then((()=>()=>w(6235))))),3226:()=>b("default","@krassowski/code-jumpers",[2,1,2,0],(()=>w.e(155).then((()=>()=>w(6480))))),3992:()=>p("default","@lumino/widgets",[1,1,33,0]),4972:()=>p("default","@jupyterlab/notebook",[1,3,4,5]),4974:()=>p("default","@jupyterlab/rendermime",[1,3,4,5]),6484:()=>p("default","@jupyterlab/docmanager",[1,3,4,5]),6748:()=>p("default","@jupyterlab/services",[1,6,4,5]),7002:()=>p("default","@jupyterlab/logconsole",[1,3,4,5]),7019:()=>p("default","@jupyterlab/coreutils",[1,5,4,5]),7140:()=>p("default","@jupyterlab/statusbar",[1,3,4,5]),7453:()=>p("default","@jupyterlab/completer",[1,3,4,5]),7493:()=>p("default","@jupyterlab/application",[1,3,4,5]),7610:()=>b("default","@krassowski/completion-theme",[2,3,3,1],(()=>w.e(501).then((()=>()=>w(44))))),7751:()=>p("default","@jupyterlab/fileeditor",[1,3,4,5]),8077:()=>b("default","@krassowski/theme-vscode",[2,2,1,1],(()=>w.e(676).then((()=>()=>w(676))))),8644:()=>b("default","lodash.mergewith",[1,4,6,1],(()=>w.e(637).then((()=>()=>w(3637))))),8770:()=>p("default","@jupyterlab/codemirror",[1,3,4,5]),8918:()=>p("default","@lumino/algorithm",[1,1,9,0]),8888:()=>b("default","lsp-ws-connection",[2,0,7,0],(()=>w.e(732).then((()=>()=>w(2732)))))},v={16:[8888],321:[1256,1580,1840,1921,2230,3226,3992,4972,4974,6484,6748,7002,7019,7140,7453,7493,7610,7751,8077,8644,8770,8918],381:[3082,6271,8912],526:[1526],991:[1991]},w.f.consumes=(e,r)=>{w.o(v,e)&&v[e].forEach((e=>{if(w.o(h,e))return r.push(h[e]);var t=r=>{h[e]=0,w.m[e]=t=>{delete w.c[e],t.exports=r()}},a=r=>{delete h[e],w.m[e]=t=>{throw delete w.c[e],r}};try{var o=m[e]();o.then?r.push(h[e]=o.then(t).catch(a)):t(o)}catch(e){a(e)}}))},(()=>{var e={25:0};w.f.j=(r,t)=>{var a=w.o(e,r)?e[r]:void 0;if(0!==a)if(a)t.push(a[2]);else if(/^(381|526|991)$/.test(r))e[r]=0;else{var o=new Promise(((t,o)=>a=e[r]=[t,o]));t.push(a[2]=o);var n=w.p+w.u(r),l=new Error;w.l(n,(t=>{if(w.o(e,r)&&(0!==(a=e[r])&&(e[r]=void 0),a)){var o=t&&("load"===t.type?"missing":t.type),n=t&&t.target&&t.target.src;l.message="Loading chunk "+r+" failed.\n("+o+": "+n+")",l.name="ChunkLoadError",l.type=o,l.request=n,a[1](l)}}),"chunk-"+r,r)}};var r=(r,t)=>{var a,o,[n,l,i]=t,f=0;if(n.some((r=>0!==e[r]))){for(a in l)w.o(l,a)&&(w.m[a]=l[a]);i&&i(w)}for(r&&r(t);f<n.length;f++)o=n[f],w.o(e,o)&&e[o]&&e[o][0](),e[n[f]]=0},t=self.webpackChunk_krassowski_jupyterlab_lsp=self.webpackChunk_krassowski_jupyterlab_lsp||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var k=w(3846);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@krassowski/jupyterlab-lsp"]=k})();