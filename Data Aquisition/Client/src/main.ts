class main{
	constructor(){
		//js
		if(window.location.pathname.indexOf('bframe') > -1){
			var body_observer = new MutationObserver((mutations_list)=>{
				mutations_list.forEach((mutations)=>{
					[].forEach.call(mutations.addedNodes, (node, index)=>{
						UserControlsScript.setUserInterface(node);
						ImageTransferScript.initialize(node);
					})
				})
			});
			body_observer.observe(document.body, {childList:true, attributes:true, subtree:true});
		}
		//no js
		else{
			var body_observer = new MutationObserver((mutations_list)=>{
				mutations_list.forEach((mutations)=>{
					[].forEach.call(mutations.addedNodes, (node, index)=>{
						UserControlsNoScript.setUserInterface(node);
						ImageTransferNoScript.initialize(node);
					})
				})
			});
			body_observer.observe(document.body, {childList:true, attributes:true, subtree:true});			
			//force trigger
            document.body.appendChild(document.createTextNode(""));
		}
	}
}

if(window.localStorage.getItem('captcha-solve') == '0'){
    new main();
    window.localStorage.setItem('captcha-log', '1');
}
else{
	alert('Captcha Aquisition running with solver(might not be, try one more time)')
}
window.localStorage.setItem('captcha-solve', '0');