declare var GM_xmlhttpRequest:any;

abstract class ImageTransfer{
	
	static primed:boolean = false;
	static full_img:boolean = false;
	static component_img:boolean = false;
	static captcha_change_listener_active:boolean = false;
	static submision_in_progress:boolean = false;
	
	static challenge:string = "";
	static image_package:any;
	static hit_arr:boolean[];
	
	static image_dim:any = {x:0, y:0};
	
	protected static getFullImage(image, image_path=image.src){
		GM_xmlhttpRequest({
		  method: "GET",
		  url: image_path,
		  responseType : "arraybuffer",
		  onload:(response) => {

				var img = new Image();
				//https://gist.github.com/candycode/f18ae1767b2b0aba568e
				var arrayBufferView = new Uint8Array( response.response );
				var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
				var urlCreator = window.URL || (<any>window).webkitURL;
				var imageUrl = urlCreator.createObjectURL( blob );
				(<HTMLImageElement>img).src = imageUrl;
				//document.body.appendChild(img);

				img.onload = ()=>{
					var image_canvas = <HTMLCanvasElement>document.createElement('CANVAS');
					image_canvas.width = img.width;
					image_canvas.height = img.height;
					var ctx=image_canvas.getContext("2d");
					ctx.drawImage(img, 0,0);
					//document.body.appendChild(image_canvas);
					this.image_package = (<HTMLCanvasElement>image_canvas).toDataURL("image/jpeg").replace('data:image/jpeg;base64,', "");
					this.full_img = true;
				}
		  }
		});		
	}
	
	protected static getSegmentedImage(image, image_path=image.src){
		GM_xmlhttpRequest({
		  method: "GET",
		  url: image_path,
		  responseType : "arraybuffer",
		  onload:(response) => {
				var img = new Image();
				//https://gist.github.com/candycode/f18ae1767b2b0aba568e
				var arrayBufferView = new Uint8Array( response.response );
				var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
				var urlCreator = window.URL || (<any>window).webkitURL;
				var imageUrl = urlCreator.createObjectURL( blob );
				(<HTMLImageElement>img).src = imageUrl;
				//document.body.appendChild(img);


				img.onload = ()=>{
					var image_canvas = <HTMLCanvasElement>document.createElement('CANVAS');
					image_canvas.width = img.width / this.image_dim.x;
					image_canvas.height = img.height / this.image_dim.y;
					var ctx=image_canvas.getContext("2d");
					
					//divide image		
					this.image_package = [];
					for(var y = 0 ; y < this.image_dim.y ; y++){
						for(var x = 0 ; x < this.image_dim.x ; x++){
							ctx.drawImage(img, 
										(x) * 300 / this.image_dim.x,(y) * 300 / this.image_dim.y, 
										image_canvas.width, image_canvas.height,
										0,0,image_canvas.width,image_canvas.height);
							//document.body.appendChild(image_canvas);
							//console.log((x) * 300 / this.image_dim.x+ " " +(y) * 300 / this.image_dim.y + " " +(x+1) * 300 / this.image_dim.x+ " " + (y+1) * 300 / this.image_dim.y)
							this.image_package.push((<HTMLCanvasElement>image_canvas).toDataURL("image/jpeg").replace('data:image/jpeg;base64,', ""));
						}
					}
					this.component_img = true;
				}
		  }
		});
		
		

	}
	
	protected static unsetFlags(){
		//this.primed = false; causes double count
		this.full_img = false;
		this.component_img = false;
		this.captcha_change_listener_active= false;
		this.submision_in_progress = false;
		
		this.challenge = "";
		this.image_package = "";
		this.hit_arr = [];
		
		this.image_dim.x = 0;
		this.image_dim.y = 0;
	}
		
	protected static transferImage(){
		if(!this.submision_in_progress){
			this.submision_in_progress = true;
				
			var post_string = '';
			var name = encodeURIComponent((<HTMLInputElement>document.getElementById('name-input')).value.trim());
			if(name == '') name = 'Anonymous';
			if(this.full_img){
				post_string = "challenge=" + encodeURIComponent(this.challenge) + "&type=full&package=" + encodeURIComponent(this.image_package) + "&hits=";
				var first_comma = false;
				var none_hit = true;
				post_string += encodeURIComponent("(" + this.image_dim.x + '|' + this.image_dim.y +")");
				this.hit_arr.forEach((hit_bool, index) => {
					if(hit_bool){
						none_hit = false;
						var x_coord = index % this.image_dim.x;
						var y_coord = Math.floor(index / this.image_dim.x);
						if(!first_comma){
							post_string += encodeURIComponent(x_coord + "-" + y_coord);
							first_comma = true;
						}
						else{
							post_string += encodeURIComponent( ',' + x_coord + "-" + y_coord);
						}
					} 
				});
				if(none_hit) return;
			}
			else if(this.component_img){
				post_string = "challenge=" + encodeURIComponent(this.challenge) + "&type=partial&package=";
				var first_comma = false;
				var none_hit = true;
				this.hit_arr.forEach((hit_bool, index) => {
					if(hit_bool){
						none_hit = false;
						if(!first_comma){
							post_string += encodeURIComponent(this.image_package[index]);
							first_comma = true;
						}
						else{
							post_string += encodeURIComponent( ',' + this.image_package[index]);
						}
					} 
				});
				if(none_hit) return;
			}
			else{
				alert('err');
				return;
			}
			post_string += "&name=" + name;
			GM_xmlhttpRequest({
			  method: "POST",
			  url: 'https://datasets.verniy.xyz/',
			  data: post_string,
			  headers:{
				'Content-Type': 'application/x-www-form-urlencoded'
			  },
			  responseType : "text",
			  onload:(response) => { }
			});
		}
	}
}