declare var GM_xmlhttpRequest:any;

class ImageTransferNoScript extends ImageTransfer{
	static initialize(node){
		var image:HTMLImageElement = <HTMLImageElement> document.getElementsByTagName("IMG")[0];
		var details = document.getElementsByTagName("STRONG")[0];
		var button_head = document.getElementsByClassName('fbc-button-verify')[0];
		var inputs_head = document.getElementsByClassName('fbc-payload-imageselect')[0];
		if(image != undefined && inputs_head != undefined && button_head != undefined && details != undefined && !this.primed){
			var text = details.textContent;		
			var inputs = inputs_head.getElementsByTagName('LABEL');		
			if(inputs.length < 9) return;
			if(!(details.nextSibling != null && details.nextSibling.textContent == "Click verify once there are none left") && 
				(true || text == "bus"|| text == "vehicles" || text == "cars" || text ==  "motorcycles" ||
					text =="taxis" || text == "boats" || text =="bicycles" || 
					text == "roads" || text == "bridges" || text =="sidewalk" || text == "crosswalks" ||
					text == "street signs" ||  text == "traffic lights" || text == "fire hydrant" ||
					text == "store front" || text == "statues"  || 
					text == "mountains or hills" || text == "palm trees")){
				
				this.unsetFlags();
				this.createClickGrid(inputs);	
				this.challenge = text;
				//asyncronous image generation
				if(details.nextSibling != null && details.nextSibling.textContent == "If there are none, click skip" || text == "street signs"){ // shouldn't ever trigger in no-script
					this.getFullImage(image);//large		
				}
				else{
					this.getSegmentedImage(image); 	//small
				}
				
				//captcha submit
				button_head.firstChild.addEventListener('click', ()=>{
					this.transferImage();
					this.primed = false;	
				});
				
				//captcha change
				if(!this.captcha_change_listener_active){
					/*with no-script, captcha iframes are destroyed after use*/
					this.captcha_change_listener_active = true;
				}
				this.primed = true;	
			}
		}
	}
	
	static createClickGrid(inputs){
		this.image_dim.y = 3;
		this.image_dim.x = 3;
		this.hit_arr = Array();
		for(var y = 0 ; y < this.image_dim.y ; y++){
			for(var x = 0 ; x < this.image_dim.x ; x++){
				this.hit_arr[y * this.image_dim.x + x] = false;
				var add_listener_fun = (_x,_y) =>{
					inputs[_y * this.image_dim.x + _x].addEventListener("click", ()=>{
						this.hit_arr[_y * this.image_dim.x + _x] = !this.hit_arr[_y * this.image_dim.x + _x];				
					});
				};
				add_listener_fun(x,y);
			}
		}
	}
}