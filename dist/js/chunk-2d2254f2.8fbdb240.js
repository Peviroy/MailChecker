(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d2254f2"],{e49f:function(e,t,n){"use strict";n.r(t);var o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-container",{attrs:{id:"Dash",fluid:"",tag:"section"}},[n("inoutputer",{attrs:{serverResponse:e.serverResponse,titleOutput:e.titleOutput,dropdown_selector:e.dropdown_selector},on:{"get-result":e.getGenerated}})],1)},r=[],s=n("3e93"),a=n("bc3a"),u=n.n(a),c={name:"DashboardGenerator",components:{inoutputer:s["a"]},data:function(){return{titleOutput:"Generate",serverResponse:"Click to get prediction",dropdown_selector:["Ham","Spam"],mailcontent_input:"",selected_model:null}},methods:{getGenerated:function(e){var t=this,n="http://penguinuniverse.top:8899",o=n+"/getContent";u.a.post(o,e).then((function(e){var n=e.data.msg;t.serverResponse=n})).catch((function(e){console.log(e)}))}}},i=c,p=n("0c7c"),l=n("6544"),d=n.n(l),f=n("a523"),h=Object(p["a"])(i,o,r,!1,null,null,null);t["default"]=h.exports;d()(h,{VContainer:f["a"]})}}]);
//# sourceMappingURL=chunk-2d2254f2.8fbdb240.js.map