class UserControlsNoScript extends UserControls{
	
	//private static items_removed:boolean = false;
	
	static setUserInterface(node){
		//console.log(window.localStorage.getItem('captcha-user-name'));
		var details_node = document.getElementsByClassName('fbc-header')[0];			
		var control_panel_node = document.getElementsByClassName('fbc-buttons')[0];
		var button_node = document.getElementsByClassName('fbc-button-verify')[0];
		if(details_node != undefined && control_panel_node != undefined && button_node != undefined){
			this.clearObstructions();			
			this.setDataTag(details_node.firstChild, 'rgb(157,58,73)');
			this.setNameBox(control_panel_node, button_node);
			this.setInputPositions();
		}
	}
	
	private static setInputPositions(){
		(<HTMLElement>document.getElementsByClassName('fbc-buttons')[0]).style.margin = '-32px 3px'; 
		(<HTMLInputElement>document.getElementById('name-input')).style.margin= '28px 4px 6px 1px';
		(<HTMLInputElement>document.getElementsByClassName('fbc-payload-imageselect')[0]).style.marginLeft = '10px'
	}
	
	private static clearObstructions(){
		var support_link = document.getElementsByClassName('fbc-why-fallback')[0];
		while(support_link.lastChild) support_link.removeChild(support_link.lastChild);
		var privacy_link = document.getElementsByClassName('fbc-privacy')[0];
		while(privacy_link.lastChild) privacy_link.removeChild(privacy_link.lastChild);
	}
}