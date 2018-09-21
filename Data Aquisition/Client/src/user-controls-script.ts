class UserControlsScript extends UserControls{
	static setUserInterface(node){
		//console.log(window.localStorage.getItem('captcha-user-name'));
		var details_node = document.getElementsByClassName('rc-imageselect-desc-wrapper')[0];			
		var control_panel_node = document.getElementsByClassName('primary-controls')[0];		
		if(details_node != undefined && control_panel_node != undefined){
			var button_node = control_panel_node.lastChild.firstChild;
			this.setDataTag(details_node.lastChild);
			this.setNameBox(control_panel_node, button_node);
		}
	}
}