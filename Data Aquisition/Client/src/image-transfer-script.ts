declare var GM_xmlhttpRequest:any;

class ImageTransferScript extends ImageTransfer{
	
	static transfer_listener;
	static previous_img_src;
	
	static initialize(node){
		var image:HTMLImageElement = <HTMLImageElement> document.getElementsByTagName("IMG")[0];
		var details = document.getElementsByTagName("STRONG")[0];
		var button = document.getElementById('recaptcha-verify-button');
		if(!this.primed && button != undefined && image != undefined && details != undefined){	
			if(image.src == this.previous_img_src) return;
			var text = details.textContent;
			button.removeEventListener('click', this.transferEventHandler);
			if(!(details.nextSibling != null && details.nextSibling.textContent == "Click verify once there are none left") && 
				(true || text == "bus"|| text == "vehicles" || text == "cars" || text ==  "motorcycles" ||
					text =="taxis" || text == "boats" || text =="bicycles" || 
					text == "roads" || text == "bridges" || text =="sidewalk" || text == "crosswalks" || 
					text == "street signs" || text == "traffic lights" || text == "fire hydrant" ||
					text == "store front" || text == "statues"  ||
					text == "mountains or hills" || text == "palm trees")){
				
				this.unsetFlags();
				this.createClickGrid();	
				this.challenge = text;
				this.previous_img_src = image.src;
				//asyncronous image generation
				if(details.nextSibling != null && details.nextSibling.textContent == "If there are none, click skip" || text == "street signs"){
					this.getFullImage(image);//large		
				}
				else{
					this.getSegmentedImage(image); 	//small
				}
				
				//captcha submit
					this.transfer_listener = button.addEventListener('click', ()=>this.transferEventHandler());
				
				//captcha change
				if(!this.captcha_change_listener_active){
					var token_change = new MutationObserver(()=>{
						this.primed = false;
					});
					token_change.observe(document.getElementById("recaptcha-token"), {attributes:true});
					this.captcha_change_listener_active = true;
				}
				this.primed = true;
			
			}
		}
	}
	
	private static transferEventHandler(){
		this.transferImage();
		this.primed = false;			
	}
	
	private static createClickGrid(){
		var tr_nodes = document.body.getElementsByTagName("TR");
		this.image_dim.y = tr_nodes.length;
		this.image_dim.x = tr_nodes[0].childNodes.length;
		this.hit_arr = Array();
		for(var y = 0 ; y < this.image_dim.y ; y++){
			for(var x = 0 ; x < this.image_dim.x ; x++){
				this.hit_arr[y * this.image_dim.x + x] = false;
				var add_listener_fun = (_x,_y) =>{
					tr_nodes[_y].childNodes[_x].addEventListener("click", ()=>{
						this.hit_arr[_y * this.image_dim.x + _x] = !this.hit_arr[_y * this.image_dim.x + _x];
				
					})
				};
				add_listener_fun(x,y);
			}
		}
	}
}