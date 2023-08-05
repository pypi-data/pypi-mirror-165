"use strict";(self.webpackChunk_dagster_io_dagit_app=self.webpackChunk_dagster_io_dagit_app||[]).push([[433],{83433:function(e,n,t){t.r(n),t.d(n,{default:function(){return _}});var o=t(59019),r=t(19065),i=t(60652),a=t(31112),s=t(12745),l=t(32030),u=t(57753),c=t(50346),d=t(7838),p=t(325),f=t(82348),v=t(76314),h=t(81745),m=t(27719),g=t(78093),x=t(42849),y=t(8412),w=t(55690),b=t.n(w),P=t(37971),k=t(7489),j=t(32289),C=function(e){var n=Math.abs(e);return"".concat(e<0?"+":"-").concat(Math.floor(n/60),":").concat(n%60<10?"0":"").concat(n%60)},Z=b().tz.names().map((function(e){var n,t=(null===(n=b().tz.zone(e))||void 0===n?void 0:n.utcOffset(Date.now()))||0;return{offsetLabel:"".concat(C(t)),offset:t,key:e}})).sort((function(e,n){return e.offset-n.offset})),I=["UTC","US/Pacific","US/Mountain","US/Central","US/Eastern"],L=[{key:"Automatic",offsetLabel:function(){var e;return"".concat((0,k.AM)()," ").concat(C((null===(e=b().tz.zone((0,k.cw)()))||void 0===e?void 0:e.utcOffset(Date.now()))||0))}(),offset:0},{key:"divider-1",offsetLabel:"",offset:0}].concat((0,o.Z)(Z.filter((function(e){return I.includes(e.key)}))),[{key:"divider-2",offsetLabel:"",offset:0}],(0,o.Z)(Z.filter((function(e){return!I.includes(e.key)})))),T=function(e){var n=e.trigger,t=p.useContext(P.j),o=(0,r.Z)(t,2),i=o[0],a=o[1];return(0,j.jsx)(x.P,{popoverProps:{position:"bottom-left",modifiers:{offset:{enabled:!0,offset:"-12px, 8px"}}},activeItem:L.find((function(e){return e.key===i})),inputProps:{style:{width:"300px"}},items:L,itemPredicate:function(e,n){return n.key.toLowerCase().includes(e.toLowerCase())},itemRenderer:function(e,n){return e.key.startsWith("divider")?(0,j.jsx)(y.R,{},e.key):(0,j.jsx)(y.sN,{active:n.modifiers.active,onClick:n.handleClick,label:e.offsetLabel,text:e.key},e.key)},itemListRenderer:function(e){var n=e.renderItem,t=e.filteredItems.map(n).filter(Boolean);return(0,j.jsx)(y.v2,{children:t})},noResults:(0,j.jsx)(y.sN,{disabled:!0,text:"No results."}),onItemSelect:function(e){return a(e.key)},children:n(i)})},_=function(e){var n=e.tabs;(0,g.Px)(),(0,f.j)("User settings");var t=p.useState((function(){return(0,h.BZ)()})),x=(0,r.Z)(t,2),y=x[0],w=x[1],b=(0,v.U)(m.n,(function(e){return"boolean"!==typeof e||e})),P=(0,r.Z)(b,2),C=P[0],Z=P[1];p.useEffect((function(){(0,h.zt)(y)}));var I=function(e){w(y.includes(e)?y.filter((function(n){return n!==e})):[].concat((0,o.Z)(y),[e])),window.location.reload()},L=p.useCallback((function(e){return(0,j.jsx)(i.Z,{children:"Automatic"===e?(0,k.aA)():e})}),[]);return(0,j.jsxs)("div",{style:{height:"100vh",overflowY:"auto"},children:[(0,j.jsx)(a.m,{title:(0,j.jsx)(s.X6,{children:"User settings"}),tabs:n}),(0,j.jsxs)(l.x,{padding:{vertical:16,horizontal:24},children:[(0,j.jsx)(l.x,{padding:{bottom:8},children:(0,j.jsx)(s.pm,{children:"Preferences"})}),(0,j.jsx)(u.nZ,{rows:[{key:"Timezone",value:(0,j.jsx)(l.x,{margin:{bottom:4},children:(0,j.jsx)(T,{trigger:L})})},{key:"Enable keyboard shortcuts",value:(0,j.jsx)(c.X,{checked:C,format:"switch",onChange:function(e){var n=e.target.checked;Z(n),setTimeout((function(){window.location.reload()}),1e3)}})}]})]}),(0,j.jsxs)(l.x,{padding:{vertical:16,horizontal:24},border:{side:"top",width:1,color:d.w.KeylineGray},children:[(0,j.jsx)(l.x,{padding:{bottom:8},children:(0,j.jsx)(s.pm,{children:"Experimental features"})}),(0,j.jsx)(u.nZ,{rows:[{key:"Debug console logging",value:(0,j.jsx)(c.X,{format:"switch",checked:y.includes(h.TT.flagDebugConsoleLogging),onChange:function(){return I(h.TT.flagDebugConsoleLogging)}})},{key:"Disable WebSockets",value:(0,j.jsx)(c.X,{format:"switch",checked:y.includes(h.TT.flagDisableWebsockets),onChange:function(){return I(h.TT.flagDisableWebsockets)}})}]})]})]})}},82348:function(e,n,t){t.d(n,{j:function(){return r}});var o=t(325),r=function(e){o.useEffect((function(){var n=document.title;return document.title=e,function(){document.title=n}}),[e])}},8412:function(e,n,t){t.d(n,{v2:function(){return p},cR:function(){return h},sN:function(){return m},AL:function(){return g},R:function(){return x}});var o=t(81034),r=t(95764),i=t(922),a=t(33918),s=(t(325),t(7838)),l=t(42658),u=t(32289),c=["icon","intent"],d=["icon","intent"],p=function(e){return(0,u.jsx)(y,(0,r.Z)({},e))},f=function(e){switch(e){case"primary":return s.w.Blue500;case"danger":return s.w.Red500;case"success":return s.w.Green500;case"warning":return s.w.Yellow500;default:return s.w.Gray900}},v=function(e){switch(e){case"primary":return s.w.Blue500;case"danger":return s.w.Red500;case"success":return s.w.Green500;case"warning":return s.w.Yellow500;default:return s.w.Gray900}},h=function(e,n){return e?"string"===typeof e?(0,u.jsx)(l.JO,{name:e,color:v(n)}):e:null},m=function(e){var n=e.icon,t=e.intent,i=(0,o.Z)(e,c);return(0,u.jsx)(w,(0,r.Z)((0,r.Z)({},i),{},{$textColor:f(t),icon:h(n,t)}))},g=function(e){var n=e.icon,t=e.intent,i=(0,o.Z)(e,d);return(0,u.jsx)(w,(0,r.Z)((0,r.Z)({},i),{},{target:"_blank",rel:"noreferrer nofollow",$textColor:f(t),icon:h(n,t)}))},x=(0,i.ZP)(a.R).withConfig({displayName:"Menu__MenuDivider",componentId:"qkix8g-0"})(["border-top:1px solid ",";margin:2px 0;"],s.w.Gray100),y=(0,i.ZP)(a.v2).withConfig({displayName:"Menu__StyledMenu",componentId:"qkix8g-1"})(["border-radius:4px;padding:8px 4px;"]),w=(0,i.ZP)(a.sN).withConfig({displayName:"Menu__StyledMenuItem",componentId:"qkix8g-2"})(["border-radius:4px;color:",";line-height:20px;padding:6px 8px 6px 12px;transition:background-color 50ms,box-shadow 150ms;align-items:flex-start;","{margin-top:2px;}&.bp3-intent-primary.bp3-active{background-color:",";","{background-color:",";}}&.bp3-disabled ","{opacity:0.5;}&.bp3-active ","{color:",";}",":first-child{margin-left:-4px;}&:hover{background:",";color:",";}&:focus{color:",";box-shadow:rgba(58,151,212,0.6) 0 0 0 2px;outline:none;}"],(function(e){return e.$textColor}),l.a1,s.w.Blue500,l.a1,s.w.White,l.a1,l.a1,s.w.White,l.a1,s.w.Gray100,(function(e){return e.$textColor}),(function(e){return e.$textColor}))},57753:function(e,n,t){t.d(n,{nZ:function(){return l},k6:function(){return u},fJ:function(){return d}});var o=t(922),r=(t(325),t(32030)),i=t(7838),a=t(55113),s=t(32289),l=function(e){var n=e.rows,t=e.spacing;return(0,s.jsx)(u,{children:(0,s.jsx)("tbody",{children:n.map((function(e){if(!e)return null;var n=e.key,o=e.value;return(0,s.jsxs)("tr",{children:[(0,s.jsx)("td",{children:(0,s.jsx)(r.x,{padding:{vertical:t,right:32},children:(0,s.jsx)(c,{children:n})})}),(0,s.jsx)("td",{children:(0,s.jsx)(r.x,{padding:{vertical:t},children:o})})]},n)}))})})};l.defaultProps={spacing:4};var u=o.ZP.table.withConfig({displayName:"MetadataTable__StyledTable",componentId:"sc-1x7ta8n-0"})(["border-spacing:0;td{vertical-align:top;}td .bp3-control{margin-bottom:0;}"]),c=o.ZP.div.withConfig({displayName:"MetadataTable__MetadataKey",componentId:"sc-1x7ta8n-1"})(["color:",";font-weight:400;"],i.w.Gray600),d=(0,o.ZP)(a.i).withConfig({displayName:"MetadataTable__MetadataTableWIP",componentId:"sc-1x7ta8n-2"})(["td:first-child{white-space:nowrap;width:1px;max-width:400px;word-break:break-word;overflow:hidden;padding-right:24px;text-overflow:ellipsis;}"])},31112:function(e,n,t){t.d(n,{m:function(){return s}});var o=t(922),r=(t(325),t(32030)),i=t(7838),a=t(32289),s=function(e){var n=e.title,t=e.tags,o=e.right,s=e.tabs;return(0,a.jsxs)(l,{background:i.w.Gray50,padding:{top:16,left:24,right:12},border:{side:"bottom",width:1,color:i.w.KeylineGray},children:[(0,a.jsxs)(r.x,{flex:{direction:"row",justifyContent:"space-between"},padding:{bottom:16},children:[(0,a.jsxs)(r.x,{flex:{direction:"row",alignItems:"flex-start",gap:12,wrap:"wrap"},children:[n,t]}),o]}),s]})},l=(0,o.ZP)(r.x).withConfig({displayName:"PageHeader__PageHeaderContainer",componentId:"sc-1u8zksn-0"})(["width:100%;.bp3-breadcrumbs{height:auto;}"])},42849:function(e,n,t){t.d(n,{P:function(){return l}});var o=t(95764),r=t(1492),i=t(3810),a=t.n(i),s=(t(325),t(32289)),l=function(e){var n,t,i=(0,o.Z)((0,o.Z)({},e.popoverProps),{},{minimal:!0,modifiers:a()({offset:{enabled:!0,offset:"0, 8px"}},(null===(n=e.popoverProps)||void 0===n?void 0:n.modifiers)||{}),popoverClassName:"dagit-popover ".concat((null===(t=e.popoverProps)||void 0===t?void 0:t.className)||"")});return(0,s.jsx)(r.P,(0,o.Z)((0,o.Z)({},e),{},{popoverProps:i}))}},1492:function(e,n,t){t.d(n,{P:function(){return h}});var o=t(14664),r=t(84410),i=t.n(r),a=t(325),s=t(71364),l=t(33918),u=t(83536),c=t(28642),d=t(77592),p=t(23095),f=t(6683),v=t(85756),h=function(e){function n(){var n,t=e.apply(this,arguments)||this;return t.state={isOpen:!1},t.TypedQueryList=v.n.ofType(),t.inputElement=null,t.queryList=null,t.handleInputRef=(0,s.Km)(t,"inputElement",null===(n=t.props.inputProps)||void 0===n?void 0:n.inputRef),t.handleQueryListRef=function(e){return t.queryList=e},t.renderQueryList=function(e){var n=t.props,r=n.filterable,s=void 0===r||r,c=n.disabled,d=void 0!==c&&c,p=n.inputProps,v=void 0===p?{}:p,h=n.popoverProps,m=void 0===h?{}:h,g=a.createElement(l.BZ,(0,o.pi)({leftIcon:"search",placeholder:"Filter...",rightElement:t.maybeRenderClearButton(e.query)},v,{inputRef:t.handleInputRef,onChange:e.handleQueryChange,value:e.query})),x=e.handleKeyDown,y=e.handleKeyUp;return a.createElement(l.J2,(0,o.pi)({autoFocus:!1,enforceFocus:!1,isOpen:t.state.isOpen,disabled:d,position:u.Ly.BOTTOM_LEFT},m,{className:i()(e.className,m.className),onInteraction:t.handlePopoverInteraction,popoverClassName:i()(f.x8,m.popoverClassName),onOpening:t.handlePopoverOpening,onOpened:t.handlePopoverOpened,onClosing:t.handlePopoverClosing}),a.createElement("div",{onKeyDown:t.state.isOpen?x:t.handleTargetKeyDown,onKeyUp:t.state.isOpen?y:void 0},t.props.children),a.createElement("div",{onKeyDown:x,onKeyUp:y},s?g:void 0,e.itemList))},t.handleTargetKeyDown=function(e){e.which!==c.NF&&e.which!==c.qN||(e.preventDefault(),t.setState({isOpen:!0}))},t.handleItemSelect=function(e,n){var o,r;t.setState({isOpen:!1}),null===(r=(o=t.props).onItemSelect)||void 0===r||r.call(o,e,n)},t.handlePopoverInteraction=function(e){var n,o;t.setState({isOpen:e}),null===(o=null===(n=t.props.popoverProps)||void 0===n?void 0:n.onInteraction)||void 0===o||o.call(n,e)},t.handlePopoverOpening=function(e){var n,o;t.previousFocusedElement=document.activeElement,t.props.resetOnClose&&t.resetQuery(),null===(o=null===(n=t.props.popoverProps)||void 0===n?void 0:n.onOpening)||void 0===o||o.call(n,e)},t.handlePopoverOpened=function(e){var n,o;null!=t.queryList&&t.queryList.scrollActiveItemIntoView(),t.requestAnimationFrame((function(){var e,n=t.props.inputProps;!1!==(void 0===n?{}:n).autoFocus&&(null===(e=t.inputElement)||void 0===e||e.focus())})),null===(o=null===(n=t.props.popoverProps)||void 0===n?void 0:n.onOpened)||void 0===o||o.call(n,e)},t.handlePopoverClosing=function(e){var n,o;t.requestAnimationFrame((function(){void 0!==t.previousFocusedElement&&(t.previousFocusedElement.focus(),t.previousFocusedElement=void 0)})),null===(o=null===(n=t.props.popoverProps)||void 0===n?void 0:n.onClosing)||void 0===o||o.call(n,e)},t.resetQuery=function(){return t.queryList&&t.queryList.setQuery("",!0)},t}return(0,o.ZT)(n,e),n.ofType=function(){return n},n.prototype.render=function(){var e=this.props,n=(e.filterable,e.inputProps,e.popoverProps,(0,o._T)(e,["filterable","inputProps","popoverProps"]));return a.createElement(this.TypedQueryList,(0,o.pi)({},n,{onItemSelect:this.handleItemSelect,ref:this.handleQueryListRef,renderer:this.renderQueryList}))},n.prototype.componentDidUpdate=function(e,n){var t,o,r,i,a;(null===(t=e.inputProps)||void 0===t?void 0:t.inputRef)!==(null===(o=this.props.inputProps)||void 0===o?void 0:o.inputRef)&&((0,s.k$)(null===(r=e.inputProps)||void 0===r?void 0:r.inputRef,null),this.handleInputRef=(0,s.Km)(this,"inputElement",null===(i=this.props.inputProps)||void 0===i?void 0:i.inputRef),(0,s.k$)(null===(a=this.props.inputProps)||void 0===a?void 0:a.inputRef,this.inputElement)),this.state.isOpen&&!n.isOpen&&null!=this.queryList&&this.queryList.scrollActiveItemIntoView()},n.prototype.maybeRenderClearButton=function(e){return e.length>0?a.createElement(l.zx,{icon:"cross",minimal:!0,onClick:this.resetQuery}):void 0},n.displayName=d.g+".Select",n}(p.U)}}]);
//# sourceMappingURL=433.9bf7774a.chunk.js.map