"use strict";(self.webpackChunk_dagster_io_dagit_app=self.webpackChunk_dagster_io_dagit_app||[]).push([[130],{16521:function(n,t,e){e.d(t,{R:function(){return i}});var i=function(n){return"result"!==n.solid.name?"".concat(n.solid.name,":").concat(n.definition.name):n.solid.name}},83130:function(n,t,e){e.r(t),e.d(t,{layoutOpGraph:function(){return c},layoutOp:function(){return p}});var i=e(59019),o=e(13357),a=e(16521),r=370,u=26,d=13,h=70;function f(n){var t={};return n.forEach((function(n){return n.forEach((function(n){return t[(0,a.R)(n)]=n}))})),Object.values(t)}function c(n,t){var e=new o.graphlib.Graph,i=0,a=100,r=100;t&&(a=(r=140)+(i=Math.max(t.inputs.length,t.outputs.length)*u)),e.setGraph({rankdir:"TB",marginx:r,marginy:a}),e.setDefaultEdgeLabel((function(){return{}}));var c=[],l={};n.forEach((function(n){l[n.name]=!0})),n.forEach((function(n){var t=p(n,{x:0,y:0});e.setNode(n.name,{width:t.bounds.width,height:t.bounds.height}),n.inputs.forEach((function(t){t.dependsOn.forEach((function(i){l[i.solid.name]&&l[n.name]&&(e.setEdge({v:i.solid.name,w:n.name},{weight:1}),c.push({from:{point:{x:0,y:0},opName:i.solid.name,edgeName:i.definition.name},to:{point:{x:0,y:0},opName:n.name,edgeName:t.definition.name}}))}))}))})),o.layout(e);var m={},g={};e.nodes().forEach((function(n){var t=e.node(n);t&&(g[n]=t)}));var y=0,v=0;Object.keys(g).forEach((function(t){var e=g[t],i=n.find((function(n){return n.name===t}));if(i){var o=e.x-e.width/2,a=e.y-e.height/2;m[t]=p(i,{x:o,y:a}),y=Math.max(y,o+e.width),v=Math.max(v,a+e.height)}})),e.edges().forEach((function(n){var t=c.find((function(t){return t.from.opName===n.v&&t.to.opName===n.w})),i=e.edge(n).points;t&&(t.from.point=i[0],t.to.point=i[i.length-1])}));var x={edges:c,nodes:m,width:y+r,height:v+a,parent:null};return t&&(x.parent=function(n,t,e){var i={invocationBoundingBox:{x:1,y:1,width:n.width-1,height:n.height-1},bounds:{x:h,y:h+e,width:n.width-140,height:n.height-2*(h+e)},mappingLeftEdge:50,mappingLeftSpacing:10,inputs:{},outputs:{},dependsOn:s(f(t.inputs.map((function(n){return n.dependsOn}))),-50,n.width),dependedBy:s(f(t.outputs.map((function(n){return n.dependedBy}))),n.height+50,n.width)},o=i.bounds.y+i.bounds.height;return t.inputs.forEach((function(n,t){i.inputs[n.definition.name]={layout:{x:i.bounds.x,y:i.bounds.y-t*u-u,width:0,height:u},collapsed:[],label:!0,port:{x:i.bounds.x+d,y:i.bounds.y-t*u-13}}})),t.outputs.forEach((function(n,t){i.outputs[n.definition.name]={layout:{x:i.bounds.x,y:o+t*u,width:0,height:u},collapsed:[],label:!0,port:{x:i.bounds.x+d,y:o+t*u+13}}})),i}(x,t,i)),x}function s(n,t,e){var i=e-166,o=Math.max(200,i/n.length),r=83+Math.min(0,(i-n.length*o)/2),u=o<300?20:0,d={};return n.forEach((function(n,e){var i=1-e%2*2;d[(0,a.R)(n)]={x:r+e*o,y:t+u*i}})),d}function p(n,t){var e=t.y,o=function(n,o,a){var h,f=(0,i.Z)(n).sort((function(n,t){return o(n).localeCompare(o(t))})),c=0,s=null,p={},l=Math.min(35,r/(f.length+1));f.forEach((function(n,i){var o=a(n);o!==s?(s=o,h={port:{x:t.x+c+d,y:e+13},collapsed:[],label:!1,layout:{x:t.x+c,y:e,width:35,height:u}},p[n.definition.name]=h,c+=l):(0===h.collapsed.length&&(c+=15),h.collapsed.push(n.definition.name))}));var m=(r-(c-d+35))/2;return Object.values(p).forEach((function(n){n.layout.x+=m,n.port.x+=m})),e+=u,p},a=function(n){var i={};return n.forEach((function(n){i[n.definition.name]={port:{x:t.x+d,y:e+13},label:!0,collapsed:[],layout:{x:t.x,y:e,width:0,height:u}},e+=u})),i},h=n.inputs.length>4?o(n.inputs,(function(n){return n.definition.name}),(function(n){var t;return(null===(t=n.dependsOn[0])||void 0===t?void 0:t.solid.name)||""})):a(n.inputs),f={x:t.x,y:Math.max(t.y,e-0),width:r,height:52};e+=52,n.definition.assetNodes.length&&n.definition.description&&(f.height+=22,e+=22);var c=n.outputs.length>4?o(n.outputs,(function(n){var t;return(null===(t=n.dependedBy[0])||void 0===t?void 0:t.definition.name)||""}),(function(n){var t;return(null===(t=n.dependedBy[0])||void 0===t?void 0:t.solid.name)||""})):a(n.outputs);return{bounds:{x:t.x-5,y:t.y-5,width:380,height:e-t.y+10},op:f,inputs:h,outputs:c}}},28077:function(n,t,e){function i(n){if("undefined"!==typeof Symbol&&null!=n[Symbol.iterator]||null!=n["@@iterator"])return Array.from(n)}e.d(t,{Z:function(){return i}})},59019:function(n,t,e){e.d(t,{Z:function(){return r}});var i=e(51844);var o=e(28077),a=e(5693);function r(n){return function(n){if(Array.isArray(n))return(0,i.Z)(n)}(n)||(0,o.Z)(n)||(0,a.Z)(n)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}}}]);
//# sourceMappingURL=130.abd14d8e.chunk.js.map