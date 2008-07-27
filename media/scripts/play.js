function set_on(selector) { 
$("#" + selector).css("background-color", selector); 
var t = setTimeout("set_off('" + selector + "')", 1000); 
} 

function set_off(selector) { 
$("#" + selector).css("background-color", "dark" + selector); 
next_color(); }  

var sequence = ["red", "blue", "green", "yellow", "green"];
function next_color() {   
	if (!sequence.length) {     
		return;   
	}   
	var next = sequence.pop();   
	console.log(next);   
	set_on(next); 
}  
next_color();

var clicked_sequence = [];
$("#game div").
	unbind("click").
	bind("click", function (event) { 
			clicked_sequence.push($(event.target).attr("id"));
		}
		);
