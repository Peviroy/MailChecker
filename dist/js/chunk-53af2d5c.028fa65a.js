(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-53af2d5c"],{"3da0":function(e,t,n){"use strict";n.r(t);var o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-container",{attrs:{id:"Dash",fluid:"",tag:"section"}},[n("v-row",{attrs:{id:"checker"}},[n("div",{attrs:{id:"main"}},[n("div",{staticClass:"container1"},[n("h2",[e._v("MailChecker")]),n("form",[n("div",{staticClass:"input-field"},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.mailcontent_input,expression:"mailcontent_input"}],attrs:{required:"required",name:"query",autofocus:""},domProps:{value:e.mailcontent_input},on:{input:function(t){t.target.composing||(e.mailcontent_input=t.target.value)}}}),n("label",{attrs:{for:""}},[e._v("Type in mail text for identify")]),n("span")]),n("v-container",{attrs:{id:"model-example-2"}},[n("v-overflow-btn",{staticClass:"my-2",attrs:{items:e.dropdown_selector,label:"Choose a model",target:"#model_example_2",dense:"",loading:"","menu-props":"top"},model:{value:e.selected_model,callback:function(t){e.selected_model=t},expression:"selected_model"}})],1),n("input",{staticClass:"btn",attrs:{type:"submit",value:"Show Result"},on:{click:e.getContent}})],1)]),n("div",{attrs:{id:"output"}},[n("h3",[e._v("Generate")]),n("div",[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.serverResponse,expression:"serverResponse"}],attrs:{id:"content",readonly:""},domProps:{value:e.serverResponse},on:{input:function(t){t.target.composing||(e.serverResponse=t.target.value)}}})])])])])],1)},a=[],s=n("bc3a"),i=n.n(s),r={name:"DashboardIcons",data:function(){return{serverResponse:"Click to get prediction",dropdown_selector:["Ham","Spam"],mailcontent_input:"",selected_model:null}},methods:{getRadioVal:function(){console.log(this.radioVal)},TextAreagoEnd:function(){var e=document.getElementById("content");e.scrollTop=e.scrollHeight},getContent:function(e){var t=this;e.preventDefault();var n="http://127.0.0.1:5000/getContent";i.a.post(n,{content:this.mailcontent_input,type:this.selected_model}).then((function(e){var n=e.data.msg;t.serverResponse=n})).catch((function(e){console.log(e)}))}}},l=r,c=(n("bbb4"),n("0c7c")),d=n("6544"),u=n.n(d),p=n("a523"),m=n("de8e"),v=n("0fd9"),f=Object(c["a"])(l,o,a,!1,null,null,null);t["default"]=f.exports;u()(f,{VContainer:p["a"],VOverflowBtn:m["a"],VRow:v["a"]})},4658:function(e,t,n){},bbb4:function(e,t,n){"use strict";var o=n("4658"),a=n.n(o);a.a}}]);
//# sourceMappingURL=chunk-53af2d5c.028fa65a.js.map