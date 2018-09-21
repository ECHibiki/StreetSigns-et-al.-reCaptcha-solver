abstract class UserControls{
	protected static setDataTag(details_node, color='rgb(255,245,220)'){
		if(document.getElementById('data-list') == undefined){
			var site_link = document.createElement("A");
			var site_break = document.createElement("BR");
			site_link.setAttribute('href', 'https://datasets.verniy.xyz/');
			site_link.setAttribute('id', 'data-list');
			site_link.setAttribute('target', '_blank');
			site_link.setAttribute('style', 'font-weight:900;font-size: 20px;margin:0px 0px;color:' + color);
			site_link.appendChild(document.createTextNode('Click for Stats'))
			details_node.insertBefore(site_link, details_node.firstChild);
			details_node.insertBefore(site_break, details_node.childNodes[1]);
		}
	}
	
	protected static setNameBox(control_panel_node, button_node){
			if(document.getElementById('name-input') == undefined){
				var name_input  = document.createElement("Input");
				name_input.setAttribute("style", 'width:114px;margin:19px 0 6px 6px;');
				name_input.setAttribute('id', 'name-input');
				name_input.setAttribute('placeholder', 'Name: Anonymous');
				(<HTMLInputElement>name_input).value = window.localStorage.getItem('captcha-user-name');
				//insert after 0th child
				control_panel_node.insertBefore(name_input, control_panel_node.childNodes[0].nextSibling);
				button_node.addEventListener('click', function(){
				window.localStorage.setItem('captcha-user-name', (<HTMLInputElement>document.getElementById('name-input')).value);
			});
		}
	}
}